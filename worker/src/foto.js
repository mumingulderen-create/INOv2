// Foto's uit het offerteformulier: controleren op echte inhoud (niet op de
// bestandsnaam of het type dat de browser opgeeft), metadata (EXIF/GPS)
// verwijderen en een veilige, vaste bestandsnaam geven. Er wordt niets
// opgeslagen: de bytes gaan alleen als bijlage mee in de e-mail.

export const FOTO_LIMIETEN = {
  maxAantal: 5,
  maxPerFoto: 4 * 1024 * 1024,   // 4 MB
  maxTotaal: 10 * 1024 * 1024,   // 10 MB (past ruim binnen de limiet van Brevo)
};

function isJpeg(b) { return b.length > 3 && b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff; }
const PNG_SIG = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
function isPng(b) { return b.length > 8 && PNG_SIG.every((v, i) => b[i] === v); }

// JPEG: APP1 (EXIF/XMP, bevat GPS), APP13 (IPTC) en commentaar verwijderen.
export function stripJpeg(b) {
  const uit = [b.subarray(0, 2)];
  let i = 2;
  while (i < b.length) {
    if (b[i] !== 0xff) throw new Error("jpeg");
    let m = b[i + 1];
    while (m === 0xff) { i++; m = b[i + 1]; }          // opvulbytes
    if (m === 0xda) { uit.push(b.subarray(i)); break; } // start of scan: rest ongewijzigd
    if (m === 0xd9) { uit.push(b.subarray(i, i + 2)); break; }
    if (m === 0x01 || (m >= 0xd0 && m <= 0xd7)) { uit.push(b.subarray(i, i + 2)); i += 2; continue; }
    if (i + 4 > b.length) throw new Error("jpeg");
    const len = (b[i + 2] << 8) | b[i + 3];
    if (len < 2 || i + 2 + len > b.length) throw new Error("jpeg");
    if (!(m === 0xe1 || m === 0xed || m === 0xfe)) uit.push(b.subarray(i, i + 2 + len));
    i += 2 + len;
  }
  return concat(uit);
}

// PNG: tekst- en EXIF-chunks verwijderen.
const PNG_WEG = new Set(["eXIf", "tEXt", "iTXt", "zTXt", "tIME"]);
export function stripPng(b) {
  const uit = [b.subarray(0, 8)];
  let i = 8;
  while (i < b.length) {
    if (i + 12 > b.length) throw new Error("png");
    const len = ((b[i] << 24) | (b[i + 1] << 16) | (b[i + 2] << 8) | b[i + 3]) >>> 0;
    const type = String.fromCharCode(b[i + 4], b[i + 5], b[i + 6], b[i + 7]);
    const eind = i + 12 + len;
    if (eind > b.length) throw new Error("png");
    if (!PNG_WEG.has(type)) uit.push(b.subarray(i, eind));
    i = eind;
    if (type === "IEND") break;
  }
  return concat(uit);
}

function concat(delen) {
  const n = delen.reduce((s, d) => s + d.length, 0);
  const out = new Uint8Array(n);
  let o = 0;
  for (const d of delen) { out.set(d, o); o += d.length; }
  return out;
}

export function naarBase64(bytes) {
  let s = "";
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(s);
}

/**
 * @param {Array<File|string>} items  fd.getAll("photos")
 * @returns {Promise<{ok:true, bijlagen:Array<{name:string, content:string}>} | {ok:false, fout:string}>}
 */
export async function verwerkFotos(items) {
  const bestanden = items.filter((f) => typeof f === "object" && f && f.size > 0);
  if (bestanden.length > FOTO_LIMIETEN.maxAantal) return { ok: false, fout: `Maximaal ${FOTO_LIMIETEN.maxAantal} foto's.` };
  let totaal = 0;
  const bijlagen = [];
  for (const [n, f] of bestanden.entries()) {
    if (f.size > FOTO_LIMIETEN.maxPerFoto) return { ok: false, fout: "Een foto is groter dan 4 MB." };
    totaal += f.size;
    if (totaal > FOTO_LIMIETEN.maxTotaal) return { ok: false, fout: "De foto's zijn samen groter dan 10 MB." };
    const b = new Uint8Array(await f.arrayBuffer());
    let schoon, ext;
    try {
      if (isJpeg(b)) { schoon = stripJpeg(b); ext = "jpg"; }
      else if (isPng(b)) { schoon = stripPng(b); ext = "png"; }
      else return { ok: false, fout: "Alleen foto's in JPG- of PNG-formaat zijn toegestaan." };
    } catch {
      return { ok: false, fout: "Een foto is beschadigd of geen geldige afbeelding." };
    }
    bijlagen.push({ name: `foto-${n + 1}.${ext}`, content: naarBase64(schoon) });
  }
  return { ok: true, bijlagen };
}
