"""
WIJK- EN PLAATSPAGINA'S IN HET ENGELS (/en/electrician-.../)
============================================================
Per wijk (sleutel = slug uit wijken.py) de Engelse teksten. Velden die hier ontbreken
(slug, type, gemeente, buurten, aanrijtijd) komen uit wijken.py.
Prijzen als placeholder: {uur_dag}, {km_tarief} enz. Aanrijtijden: {aanrijtijd_utrecht}.
Voegt de eigenaar in wijken.py "praktijk" toe (echte klussen), vertaal die dan hier ook.
"""

WIJKEN_EN = {
    "utrecht-binnenstad": {
        "naam": "Utrecht City Centre",
        "intro": "No power in a listed building, blown fuses or want to modernise your meter cupboard in Utrecht's city centre? INO Elektra is based in Utrecht and knows the unique installations around the Oudegracht, the Neude and the Museum Quarter inside out. Direct contact with a qualified electrician, clear price agreements upfront and, within the municipality of Utrecht, we never charge a call-out fee.",
        "woningen": "Utrecht's historic city centre has many centuries-old buildings, canal houses and listed townhouses. The electrics here have often been extended bit by bit over the decades. In practice we still regularly come across fabric-insulated wiring, old steel conduits, missing earthing in living areas and overloaded fuses. Anyone switching to a modern induction hob, air conditioning or heavier appliances needs a professional upgrade and complete modernisation to RCBOs in line with NEN 1010.",
        "klussen": [
            ["Fuse box replacement & protection", "Replacing outdated fuse boxes with modern ABB or Hager boards with RCDs and surge protection."],
            ["Installing & testing earthing", "Driving earth rods or connecting equipotential bonding in historic buildings that do not yet have a safe earth."],
            ["Cooking circuit / Perilex for induction", "Safely connecting modern induction hobs via a two-phase or three-phase cooking circuit without damaging the building's historic character."],
            ["24/7 emergency service for power cuts", "Fast tracing of short circuits, RCD faults or overloading in city-centre homes and restaurants."],
        ],
        "lokaal": "In Utrecht's city centre, parking and pedestrian zones can sometimes be a challenge. We are well equipped to get there quickly. For a general outage on the grid, report it straight away to Stedin on 0800-9009.",
        "faq": [
            ["Can a modern fuse box simply be fitted in a listed canal house?", "Certainly. We fit compact, modern units from top brands that fit exactly within the existing meter cupboard space, while preserving the historic structure."],
            ["What about call-out charges in the city centre?", "Within the whole municipality of Utrecht, including the centre and the Museum Quarter, our call-out charge is € {voorrijkosten_utrecht}."],
        ],
    },
    "utrecht-oost": {
        "naam": "Utrecht East",
        "intro": "Need an electrician in Utrecht East? From a characterful townhouse by the Wilhelminapark to an attractive 1930s home in Oudwijk: INO Elektra carries out all electrical work safely and professionally. Call our electrician directly for emergencies, advice or a fixed quote.",
        "woningen": "Utrecht East is known for its stately early 20th-century buildings and fine 1930s architecture. Many homes are being thoroughly renovated or made more sustainable with a hybrid heat pump, solar panels or a luxury kitchen-diner. The existing single-phase connection is then often not enough. We take care of the complete conversion of the meter cupboard to three-phase power, recessing extra sockets and neat cable routes.",
        "klussen": [
            ["Preparing a three-phase fuse box", "Extending the meter cupboard for induction, heat pumps and charging points while keeping a neat finish."],
            ["Wall chasing & moving sockets", "Low-dust recessing of new electrical points in high ceilings and original plaster walls."],
            ["Garden lighting & outdoor sockets", "Installing watertight underground cables and designer lighting for long city gardens."],
            ["Emergency help with RCD faults", "Fast testing of circuits and damp problems in old basements and cellars."],
        ],
        "lokaal": "In Oudwijk and Abstede street parking is often regulated. We don't charge a call-out fee anywhere in Utrecht East and always work with fixed rates agreed upfront.",
        "faq": [
            ["Is a three-phase upgrade necessary for a hob in Utrecht East?", "For most modern induction hobs above 7.4 kW, or a combination with an oven and a Quooker, a three-phase connection is strongly recommended to prevent overloading."],
            ["Can cables be chased in with low dust in an occupied home?", "Yes, we work with professional wall chasers fitted with industrial M-class dust extraction, so your interior stays neat and clean."],
        ],
    },
    "leidsche-rijn": {
        "naam": "Leidsche Rijn",
        "intro": "EV charger installation, extending your fuse box or a fault in your new-build home in Leidsche Rijn? INO works in Parkwijk, Terwijde, Langerak, Het Zand and the rest of Leidsche Rijn. Fixed price upfront, no call-out charge within the municipality of Utrecht.",
        "woningen": "Leidsche Rijn has been built since the late 1990s, so the installations are relatively new and safe. The questions here are less about ageing and more about extending: an EV charger on the driveway, a heat pump, solar panels, an electrically heated extension or a summer house with power. A fuse box that was exactly big enough at handover then soon fills up. Often extending with an extra RCBO is enough; sometimes a three-phase connection is the smarter choice.",
        "klussen": [
            ["EV charger installation", "A wallbox on the front of the house or on the driveway, with its own circuit and smart load balancing where needed."],
            ["Extending the fuse box", "Extra circuits for a heat pump, induction or an extension, without replacing the whole fuse box if that isn't necessary."],
            ["Three-phase power (400V)", "For a heat pump, sauna or heavy workshop we install a three-phase circuit."],
            ["Garden lighting and outdoor socket", "Underground cable, watertight connections and an outdoor socket on a separate circuit."],
        ],
        "lokaal": "In Leidsche Rijn we are usually with you within {aanrijtijd_utrecht} minutes in an emergency, depending on traffic. For EV chargers we are happy to come and look first, or you can send photos of your meter cupboard and the spot for the charger.",
        "faq": [
            ["Can my fuse box handle an EV charger?", "Often, yes, but it depends on your connection (single-phase or three-phase) and the space in the fuse box. Send a photo of your meter cupboard and rating plate and we will tell you straight away."],
            ["Do I need a three-phase connection for an EV charger?", "No, you can also charge on single-phase, just more slowly. If you already have three-phase, your car charges faster. We give you honest advice on what suits your car and how you use it."],
            ["Do you also work in Vleuten and De Meern?", "Yes. Vleuten, De Meern and Vleuterweide are part of the municipality of Utrecht, so there is no call-out charge there either."],
        ],
    },
    "vleuten-de-meern": {
        "naam": "Vleuten-De Meern",
        "intro": "Looking for a reliable electrician in Vleuten, De Meern or Haarzuilens? INO Elektra is ready for fuse box replacements, EV chargers, three-phase power and 24/7 emergency help. No call-out charge within Utrecht, fixed prices and all work in line with NEN 1010.",
        "woningen": "Vleuten-De Meern has a varied mix of authentic village centres, spacious family homes and modern new builds such as in Haarzicht and Veldhuizen. Many homes have their own driveway and a large garden. Popular jobs therefore include installing three-phase power to the garage or shed, fitting an EV charger, and running underground cables for garden lighting.",
        "klussen": [
            ["Installing 400V three-phase power", "Running three-phase cabling to garages, workshops or heat pumps."],
            ["EV charger on your own driveway", "Professional installation of EV chargers including load balancing and groundwork."],
            ["Modernising the fuse box", "Upgrading older boards with modern RCBOs and main switches."],
            ["Garden electrics & outdoor lighting", "Installing watertight switches, ground spotlights and splash-proof sockets."],
        ],
        "lokaal": "Vleuten and De Meern are fully part of the municipality of Utrecht, so you benefit from a € {voorrijkosten_utrecht} call-out charge. For urgent power cuts we get there quickly via the A2/A12 and ring road.",
        "faq": [
            ["Can a cable be run to my detached garage?", "Yes, we professionally lay underground cables (YMvK-as) with an earth screen and, if you wish, fit a sub-distribution board in the garage."],
            ["How quickly can you be there for a fault in Vleuten?", "For urgent emergency calls we are usually at your door within {aanrijtijd_utrecht} minutes."],
        ],
    },
    "utrecht-west": {
        "naam": "Utrecht West & Lombok",
        "intro": "Need an electrician in Utrecht West, Lombok or Oog in Al? INO Elektra helps you quickly and professionally. Whether it is safely connecting a new kitchen, replacing a fuse box or an urgent emergency call-out: you speak directly to the electrician. No call-out charge within Utrecht and always a fixed price upfront.",
        "woningen": "Utrecht West has a characterful mix of cosy pre-war workers' houses in Lombok and Nieuw Engeland, and stately 1930s villas and townhouses in Oog in Al. During renovations, residents regularly run into outdated meter cupboards, wiring with too little capacity or missing earthing. We bring the installation fully up to the current NEN 1010 safety standards.",
        "klussen": [
            ["Modernising the fuse box", "Replacing old fuses with safe circuit breakers and RCDs."],
            ["Installing a Perilex cooking circuit", "From gas to induction: running safe cabling from the meter cupboard to the hob."],
            ["Wall chasing for flush switches and sockets", "Neatly hiding cables in brick and plaster without visible trunking."],
            ["Emergency service for short circuits", "Quickly locating and fixing outages in older circuits."],
        ],
        "lokaal": "In Lombok and Nieuw Engeland parking is often tight. We plan our trips carefully and make sure we have materials to hand. No call-out charge anywhere in Utrecht West.",
        "faq": [
            ["Can I keep my old fuse box in Lombok if I switch to electric cooking?", "No. Under NEN 1010, an induction hob needs a separate cooking circuit or three-phase circuit with a main switch and RCD. An old fuse box with screw-in fuses does not meet this."],
            ["What does replacing a fuse box cost in Utrecht West?", "Replacing a complete single-phase fuse box, including installation, premium-brand components and VAT, starts at € {groepenkast_1f}. For three-phase it starts at € {groepenkast_3f}."],
        ],
    },
    "zuilen": {
        "naam": "Zuilen & Ondiep (Northwest)",
        "intro": "Do you live in Zuilen, Ondiep or Pijlsweerd and are you looking for a reliable electrician? INO Elektra is your local installer in Utrecht Northwest. For fuse boxes, Perilex connections, electrical extensions and emergency service. Always a clear price upfront, 100% transparent and no call-out charge.",
        "woningen": "Zuilen and Ondiep have many characterful early 20th-century workers' and railway houses (such as in Elinkwijk) next to renovated walk-up flats and contemporary new builds along the Vecht. Many residents are renovating their homes and switching from gas to induction. This often needs a meter cupboard upgrade, new wiring and earthing in wet rooms.",
        "klussen": [
            ["Fuse box replacement", "Replacing outdated meter cupboards with compact single-phase or three-phase premium-brand units."],
            ["Fitting a Perilex connection", "Installing a two-phase cooking circuit for worry-free induction cooking."],
            ["Earthing in the bathroom & kitchen", "Fitting equipotential bonding and earthing to prevent electric shocks or leakage currents."],
            ["Emergency service for RCD trips", "Targeted fault diagnosis with professional insulation resistance testers."],
        ],
        "lokaal": "Zuilen and Ondiep are easy to reach from the Amsterdamsestraatweg and the Vleutenseweg. Within the municipality of Utrecht the call-out charge is € {voorrijkosten_utrecht}.",
        "faq": [
            ["My RCD keeps tripping in Ondiep, what should I do?", "Switch off all circuits behind that RCD, switch the RCD back up and switch the circuits back on one by one. Does it keep tripping? Call us straight away for emergency help."],
            ["How long does replacing a fuse box take?", "A standard replacement takes 2 to 3.5 hours on average. The power is temporarily switched off during the work."],
        ],
    },
    "overvecht": {
        "naam": "Overvecht",
        "intro": "Power gone, an RCD that keeps tripping or ready for a new fuse box in Overvecht? INO is an electrician from Utrecht who works in Overvecht-Noord and -Zuid every day. You call the electrician directly, get a fixed price upfront and pay no call-out charge within the municipality of Utrecht.",
        "woningen": "Overvecht was mostly built in the 1960s and 1970s: many walk-up and gallery flats along the 'dreven', plus family homes and newer buildings after the renovations of recent years. In homes that have never been updated we often see a fuse box with few circuits, not all circuits behind an RCD and, in bedrooms, sometimes still sockets without an earth. Because more and more residents are switching to electric cooking, an extra cooking circuit or Perilex connection is one of our most requested jobs here.",
        "klussen": [
            ["Fuse box replacement in a flat", "An old fuse box with screw-in fuses or too few RCDs? We fit a new fuse box that meets NEN 1010, usually within one working day."],
            ["Cooking circuit for induction", "Switching from gas to induction? We run a separate cooking circuit with a Perilex connection from the meter cupboard."],
            ["RCD keeps tripping", "Often an appliance or moisture in an outdoor socket or bathroom. We test each circuit and fix the cause."],
            ["Earthed sockets", "Replacing old sockets without an earth or adding extra sockets, neatly finished."],
        ],
        "lokaal": "Parking is usually not a problem in Overvecht, so we are quickly at your door. Is it not just you but the whole block of flats or street without power? Then the fault is probably with the grid operator: first call the free national outage number 0800-9009.",
        "faq": [
            ["Do you charge a call-out fee in Overvecht?", "No. Overvecht is within the municipality of Utrecht, so there is no call-out charge. You only pay the fixed rate we agree upfront."],
            ["Can I have the fuse box replaced in my rented home?", "In a rented home the fuse box usually belongs to the landlord or housing association. Check with your landlord first; we can provide a quote and photos so they can decide quickly."],
            ["How quickly can you be there in an emergency in Overvecht?", "For an urgent fault we are usually on site within {aanrijtijd_utrecht} minutes, depending on traffic. Call us straight away and you will hear what time we can be there."],
        ],
    },
    "hoograven": {
        "naam": "Hoograven, Lunetten & Tolsteeg",
        "intro": "Looking for an electrician in Hoograven, Lunetten or Tolsteeg? INO Elektra is based in Utrecht and stands for craftsmanship, safety and transparent prices. From replacing your meter cupboard to kitchen electrics and emergency help: we help you quickly and without a call-out charge.",
        "woningen": "Hoograven and Tolsteeg offer a rich variety, from 1930s and 1950s homes to the typical 1970s cul-de-sac layout of Lunetten and new lofts at Rotsoord. Many kitchens and bathrooms are being renovated, which needs extra earthed circuits for dishwashers, induction hobs and ovens. We make sure the load is safely spread across the phases and RCDs.",
        "klussen": [
            ["Kitchen electrics & cooking circuits", "Separate circuits for Quookers, dishwashers, ovens and induction hobs."],
            ["Fuse box replacement", "Installing modern, fire-safe units from ABB or Hager."],
            ["Adding RCDs", "Meeting the standard: a maximum of 4 circuits per RCD for optimal safety."],
            ["Tracing RCD faults", "Testing leakage currents in damp crawl spaces and outdoor cabling."],
        ],
        "lokaal": "Thanks to the location near the Waterlinieweg and the Utrecht Zuid ring road, we reach Hoograven and Lunetten very quickly. No call-out charge.",
        "faq": [
            ["How many circuits are allowed behind one RCD?", "Under the NEN 1010 standard, a maximum of 4 circuits may be connected behind one RCD, to prevent unnecessary tripping from small leakage currents."],
            ["Can you also help with moving sockets in Lunetten?", "Certainly. We neatly chase in the cables and fit double or single flush sockets at any height you want."],
        ],
    },
    "kanaleneiland": {
        "naam": "Kanaleneiland",
        "intro": "Need an electrician in Kanaleneiland? INO helps residents between the Merwede Canal and the Amsterdam-Rhine Canal with faults, new circuits and complete fuse boxes. Fixed price upfront, no call-out charge within Utrecht and available 24/7 for emergencies.",
        "woningen": "Kanaleneiland is a typical post-war reconstruction neighbourhood from the late 1950s and early 1960s, with many walk-up flats and long blocks. The original electrical installation there was often designed for a few lights and a washing machine, not for the appliances we use today. You notice it when circuits trip as soon as the kettle, microwave and air fryer are on at the same time. An extra circuit or a new fuse box solves this for good.",
        "klussen": [
            ["Circuit trips when cooking", "Kitchen appliances on one circuit overload the installation. We spread them over extra circuits so it no longer trips."],
            ["Upgrading the fuse box", "We replace old fuse boxes with porcelain fuses with a modern board with RCBOs."],
            ["Washing machine and dryer separately", "A separate circuit for the washing machine and dryer stops the RCD tripping during a wash."],
            ["Fault finding", "Does the power go off now and then for no clear reason? We test insulation resistance and connections until we find the cause."],
        ],
        "lokaal": "Kanaleneiland is close to the ring road and the Jaarbeurs, so we are usually there quickly in an emergency. In walk-up flats the meter cupboard is sometimes in the stairwell or hallway; feel free to send a photo via WhatsApp and we can assess a lot in advance.",
        "faq": [
            ["What does an extra circuit cost in Kanaleneiland?", "Adding an extra circuit costs from € {extra_groep}, depending on your current fuse box and the space. Send a photo of your meter cupboard and you will get a fixed price straight away."],
            ["Why does my power go off when I cook?", "Usually too many heavy appliances are on one circuit. That is not a defect but overloading. The solution is an extra circuit or a separate cooking circuit."],
            ["Is there a call-out charge in Kanaleneiland?", "No, Kanaleneiland is within the municipality of Utrecht. You pay no call-out charge."],
        ],
    },
    "transwijk": {
        "naam": "Transwijk",
        "intro": "INO is your electrician in Transwijk, from the flats around Park Transwijk to the family homes towards the Merwede Canal. Whether it is a fault, a new fuse box or extra sockets: you get a fixed price upfront and pay no call-out charge within Utrecht.",
        "woningen": "Like neighbouring Kanaleneiland, Transwijk was built after the war, with a mix of flats and terraced houses. Many homes have since been renovated: an open-plan kitchen, an extension or a loft room. That is often exactly where things go wrong, because the installation hasn't grown with the house. We regularly see extended cables, too many sockets on one circuit and a full fuse box. In the older pre-war houses of the adjoining Dichterswijk we also sometimes come across old wiring.",
        "klussen": [
            ["Electrics for a renovation", "New kitchen or extension? We install the circuits, sockets and lighting in line with NEN 1010."],
            ["Extending the fuse box", "Fuse box full? We extend it or replace it with a unit that has room for an EV charger or heat pump later."],
            ["Moving sockets", "Low-dust chasing and moving sockets, so your interior works the way you want."],
            ["Checking old wiring", "Unsure about the condition of your wiring? We test the installation and advise what is really needed."],
        ],
        "lokaal": "Have a fault and not sure whether it is your own home? Check whether the neighbours and street lights still have power. If they do, the problem is in your own installation and we can help. If not, call the national outage number 0800-9009.",
        "faq": [
            ["Can you install the electrics for my new kitchen?", "Yes. We make a plan for circuits, the cooking circuit and sockets in advance and work with a fixed price. Send your kitchen drawing and we will work it out straight away."],
            ["Do you also work in Dichterswijk and Rivierenwijk?", "Yes, we work throughout Utrecht Southwest and South. The same fixed price without a call-out charge applies everywhere."],
            ["How long does replacing a fuse box take?", "Usually half a day to a full working day. You are briefly without power during that time; we agree beforehand when suits you best."],
        ],
    },
    "utrecht-noordoost": {
        "naam": "Utrecht Northeast & Wittevrouwen",
        "intro": "Looking for an electrician in Utrecht Northeast, Wittevrouwen or Tuindorp? INO Elektra specialises in professionally adapting and upgrading electrical installations in historic and pre-war homes. Reliable, in line with NEN 1010 and with no call-out charge within Utrecht.",
        "woningen": "Wittevrouwen and Tuinwijk are among Utrecht's most sought-after neighbourhoods, with beautiful facades from the late 19th and early 20th century. Tuindorp is known for high-quality 1930s homes. The electrical installations here need real craftsmanship: original plaster and cornice ceilings must be preserved while the capacity is doubled for induction cooking, solar panels and Quookers.",
        "klussen": [
            ["Enlarging & modernising the fuse box", "Upgrading to 8 to 12 circuits with RCBOs for optimal reliability."],
            ["Installing a Perilex induction cooking circuit", "Discreet cabling to the kitchen without breaking into historic plasterwork."],
            ["Restoring & improving earthing", "Testing and driving earth electrodes for maximum safety."],
            ["Outdoor lighting and garden sockets", "Atmospheric lighting in city gardens with safe, splash-proof IP65 connections."],
        ],
        "lokaal": "In Wittevrouwen and Tuinwijk parking can be challenging. We take this into account in our planning. No call-out charge anywhere in the Northeast.",
        "faq": [
            ["Can you add extra circuits without replacing the whole meter cupboard?", "If the current fuse box is from a solid premium brand and has enough free module space, we can add separate RCBOs. If the fuse box is outdated, a complete replacement is safer and often better value."],
            ["Do you give a guarantee on the work?", "Yes, as standard we offer a full 12-month installation guarantee and a 2-year manufacturer's warranty on all premium-brand materials supplied."],
        ],
    },
    "nieuwegein": {
        "naam": "Nieuwegein",
        "intro": "INO is an electrician for Nieuwegein: from Batau and Galecop to Zuilenstein and old Vreeswijk. We help with power cuts, replace fuse boxes and install cooking circuits and EV chargers. Always with a fixed price upfront.",
        "woningen": "Nieuwegein was largely built as a growth town in the 1970s and 1980s. Many of those homes still have the original fuse box, sometimes with screw-in fuses and often with only one or two RCDs for the whole house. If one circuit trips, a large part of the house goes dark. A modern fuse box with an RCBO per circuit is safer and prevents this. In historic Vreeswijk and in new builds such as Blokhoeve the questions are different again, from old wiring to EV chargers.",
        "klussen": [
            ["Replacing a fuse box with screw-in fuses", "Screw-in fuses and one old RCD? We fit a safe, modern fuse box."],
            ["An RCBO per circuit", "That way only that one circuit trips in a fault, not half your house."],
            ["Cooking circuit and Perilex", "Ready for induction with a separate cooking circuit from the meter cupboard."],
            ["EV charger and three-phase power", "EV charger or heat pump? We check whether your current connection is enough."],
        ],
        "lokaal": "Nieuwegein is outside the municipality of Utrecht; we charge € {km_tarief} per km and tell you upfront. Via the A12 and A2 we get there quickly in an emergency. The whole neighbourhood without power? Then first call 0800-9009 (grid operator).",
        "faq": [
            ["My 1970s house still has screw-in fuses. Is that dangerous?", "Not immediately dangerous as long as everything works, but it no longer meets current standards and offers less protection against electrocution and fire. Replacing it is a sensible investment, especially if you are going to use more electricity."],
            ["What does a new fuse box cost in Nieuwegein?", "A single-phase fuse box starts at € {groepenkast_1f} all-in, a three-phase unit at € {groepenkast_3f}. The mileage charge comes on top, and you hear it upfront."],
            ["Do you also work in Vreeswijk?", "Yes, throughout Nieuwegein, including Vreeswijk and the new builds in Blokhoeve."],
        ],
    },
    "maarssen": {
        "naam": "Maarssen",
        "intro": "Need an electrician in Maarssen? INO comes from Utrecht to Maarssen-Dorp and Maarssenbroek for faults, fuse boxes, Perilex connections and EV chargers. You speak directly to the electrician and know the cost upfront.",
        "woningen": "Maarssen has two faces. In Maarssen-Dorp along the Vecht there are old, sometimes listed buildings where the wiring has been adapted bit by bit over the years. Careful work and a neat finish are important there. Maarssenbroek was mainly built in the 1970s and 1980s; the installations there are often still original, with a fuse box that is due for replacement or too small for induction, a heat pump or an EV charger.",
        "klussen": [
            ["Fuse box replacement", "Original fuse box from the 1970s/80s? We replace it with a modern unit with RCBOs."],
            ["Perilex and induction", "A separate cooking circuit with a Perilex connection for your new induction hob."],
            ["Working in older buildings", "Carefully adapting existing wiring, with respect for the character of the building."],
            ["EV charger on your own property", "Installing an EV charger with its own circuit and a safe connection."],
        ],
        "lokaal": "Maarssen is outside the municipality of Utrecht. That is why we charge a fixed mileage rate of € {km_tarief} per km, and you always hear the amount upfront. Via the A2 we get there quickly from Utrecht.",
        "faq": [
            ["What does travel to Maarssen cost?", "For Maarssen we charge € {km_tarief} per km. You always hear the exact amount upfront, together with the price of the job."],
            ["Do you also work in older buildings in Maarssen-Dorp?", "Yes. We work carefully, discuss where cables will go and finish everything neatly. For listed buildings we agree beforehand what is and isn't allowed."],
            ["Do you also come to Maarssen for emergencies?", "Yes, also outside office hours. Call us straight away and you will hear when we can be there."],
        ],
    },
    "houten": {
        "naam": "Houten",
        "intro": "Looking for an electrician in Houten? INO Elektra carries out complete installations in Houten-Noord and Houten-Zuid. Specialists in fuse boxes, EV chargers with load balancing, three-phase power and kitchen electrics. A clear all-in price upfront and quality work in line with NEN 1010.",
        "woningen": "Houten is a modern municipality with mainly post-war and recent family homes around its two railway centres (Het Rond and Castellum). Car ownership and the use of electric vehicles and solar panels are very high here. We see a lot of demand for EV charger installations with dynamic load balancing, three-phase power for heat pumps and extending meter cupboards with extra PV circuits.",
        "klussen": [
            ["EV charger installation", "Fitting smart charging points on your own driveway, including the cable route and load balancing."],
            ["Extending the fuse box for PV & heat pump", "Fitting separate RCBOs for solar panels and hybrid heat pumps."],
            ["Installing three-phase power", "Professional meter cupboard preparation for heavy equipment."],
            ["Electrical fit-out & kitchen preparation", "Moving sockets and cables for new kitchens."],
        ],
        "lokaal": "From the A27 and De Rondweg Houten all neighbourhoods are quickly reached. For Houten we only charge € {km_tarief}/km travel.",
        "faq": [
            ["Can my existing fuse box in Houten be extended for a heat pump?", "Often, yes, as long as there is enough free module space on the DIN rail and the main switch is heavy enough. We are happy to check this beforehand from a photo."],
            ["Do you also supply the EV charger itself?", "We can supply the complete package (such as Alfen or Easee) or just install and connect a charger you have bought yourself."],
        ],
    },
    "zeist": {
        "naam": "Zeist",
        "intro": "Need an electrician in Zeist? INO Elektra helps homeowners and businesses in Zeist, Kerckebosch and Zeist-West. From fuse boxes and three-phase power to garden lighting and an emergency service. A qualified professional, clear rates and reliable service in line with NEN 1010.",
        "woningen": "Zeist is known for its beautiful wooded villa areas, characterful 1930s buildings and post-war residential neighbourhoods. In many homes with large plots we install extensive outdoor lighting with underground cables and dusk sensors. We also regularly carry out three-phase upgrades for induction cooking, saunas and heat pumps.",
        "klussen": [
            ["Garden lighting & underground cables", "Installing watertight underground cable networks, spotlights and dusk sensors."],
            ["Three-phase power & heavy-duty connections", "Three-phase installation for saunas, EV chargers and heat pumps."],
            ["Upgrading the fuse box", "Replacing old fuse boxes with safe premium-brand installations."],
            ["24/7 emergency service", "Quickly tracing leakage current faults in outdoor cables and indoor circuits."],
        ],
        "lokaal": "Via the Utrechtseweg and the A28 we are in Zeist within {aanrijtijd_regio} minutes in an emergency. Fixed prices upfront and clear agreements.",
        "faq": [
            ["My garden lighting makes the RCD trip, can you fix this?", "Certainly. Moisture in cable joints or damaged underground cables are a common cause. We trace the exact location and make the connection watertight."],
            ["What does a site visit cost in Zeist?", "A site visit costs € {schouw} incl. VAT, and we deduct this amount in full from the invoice as soon as you have us carry out the job."],
        ],
    },
    "ijsselstein": {
        "naam": "IJsselstein",
        "intro": "Need a reliable electrician in IJsselstein? INO Elektra is ready for you in Zenderpark, Achterveld and the historic town centre. Fuse box replacement, connecting a cooking circuit or urgently fixing a fault. Always a fixed price upfront, premium-brand materials and a 12-month guarantee.",
        "woningen": "IJsselstein has an attractive historic centre and spacious residential areas such as Achterveld and Zenderpark. Many households are switching to electric cooking or buying an electric car. We take care of safe meter cupboard extensions, running Perilex cables and installing EV chargers.",
        "klussen": [
            ["Fuse box replacement", "Fitting complete single-phase or three-phase units with a 2-year manufacturer's warranty."],
            ["Fitting a Perilex cooking circuit", "Neatly hidden cabling to the hob."],
            ["EV charger at home", "Safe installation with dynamic load balancing on the driveway."],
            ["24/7 emergency service", "Fast repair when the power goes off."],
        ],
        "lokaal": "Via the A2 and the N210 we are in IJsselstein within {aanrijtijd_regio} minutes in an emergency. A transparent mileage rate of € {km_tarief}/km outside Utrecht.",
        "faq": [
            ["Can I get a quote via WhatsApp for IJsselstein?", "Certainly! Send a photo of your meter cupboard via WhatsApp to 06 28 76 37 75 and you will quickly receive a fixed all-in price."],
            ["Are you also available in the evening for urgent jobs?", "Yes, our emergency electrician is on call 24/7 for urgent incidents."],
        ],
    },
    "vianen": {
        "naam": "Vianen",
        "intro": "An electrician in Vianen, just across the Lek bridge? INO comes from Utrecht to Vianen's historic town centre, its residential areas and new builds such as Hoef en Haag. For faults, fuse boxes, cooking circuits and EV chargers, always with a fixed price upfront.",
        "woningen": "In the old fortified town around the Voorstraat there are buildings that are sometimes hundreds of years old. The electrical installation there has often been adapted in stages, with different types of cabling mixed together. Testing and careful renewal is the most important work there. In the post-war neighbourhoods we mainly replace outdated fuse boxes, and in the new builds of Hoef en Haag it is usually about extending: an EV charger, solar panels or an extra circuit.",
        "klussen": [
            ["Testing the installation", "Doubts about old wiring? We test the insulation and earthing and give you honest advice."],
            ["Fuse box replacement", "Replacing an outdated fuse box with a modern, safe unit with RCBOs."],
            ["EV charger in a new build", "Installing an EV charger with its own circuit, even if you already have solar panels."],
            ["Fixing faults", "An RCD that trips or a circuit that cuts out: we find the cause and fix it."],
        ],
        "lokaal": "Vianen is outside the municipality of Utrecht. We charge € {km_tarief} per km and always tell you upfront. In an emergency, call us straight away and you will hear when we can be there.",
        "faq": [
            ["Do you also come to Vianen?", "Yes. Vianen is directly south of Utrecht, across the Lek. We charge € {km_tarief} per km for travel and you hear the amount upfront."],
            ["Can you work in an old building in the town centre?", "Yes. We work carefully and agree beforehand where cables will run. For a listed building we check what is and isn't allowed."],
            ["Do you also work in Hagestein and Everdingen?", "Yes, also in the villages around Vianen. Feel free to check your address with us."],
        ],
    },
    "breukelen": {
        "naam": "Breukelen",
        "intro": "INO is also your electrician in Breukelen. From the old village centre and the buildings along the Vecht to the residential areas around the station: we help with faults, fuse boxes, cooking circuits, EV chargers and outdoor lighting. A fixed price upfront, no surprises afterwards.",
        "woningen": "Breukelen combines a historic centre with post-war and newer residential areas. In the older buildings you often find installations that have been extended over the years without the fuse box growing with them. Outside the centre, with larger gardens and detached houses, garden lighting, power to the summer house and an EV charger on your own property are popular jobs.",
        "klussen": [
            ["Power to a summer house or shed", "Underground cable, its own circuit and a watertight connection, installed safely."],
            ["Garden lighting", "Atmospheric outdoor lighting with IP-rated fittings and neat cable trunking."],
            ["Extending or replacing the fuse box", "More circuits or a complete new fuse box if the old one is too small or outdated."],
            ["EV charger on your own property", "An EV charger with its own circuit and, where needed, load balancing."],
        ],
        "lokaal": "Breukelen is outside the municipality of Utrecht. We charge € {km_tarief} per km and tell you upfront. Via the A2 we get there quickly from Utrecht.",
        "faq": [
            ["What does power to my summer house cost?", "That depends on the distance and the ground. Send photos of your meter cupboard and the route to the summer house and you will get a fixed price upfront."],
            ["Do you also come to Kockengen and Nieuwer Ter Aa?", "Yes. Feel free to check your address with us; we charge € {km_tarief} per km and tell you upfront."],
            ["Can I also book an appointment at the weekend?", "For faults we are available 24/7. Planned jobs at the weekend are possible by agreement; the evening and weekend rates then apply."],
        ],
    },
}
