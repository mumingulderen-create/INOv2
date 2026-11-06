"""
STORINGSPAGINA'S IN HET ENGELS (/en/...)
=======================================
Per storing (sleutel = slug uit storingen.py) de Engelse teksten. Velden die hier
ontbreken (slug, gerelateerd) komen uit storingen.py.

Veiligheid: dezelfde regels als storingen.py. Geef bezoekers NOOIT instructies om zelf
iets open te schroeven of aan leidingen te werken; geen extra doe-het-zelfstappen.
{uur_dag}, {km_tarief} enz. worden automatisch ingevuld (Engelse notatie).
"""

STORINGEN_EN = {
    "stroomstoring-utrecht": {
        "kort": "No power at home",
        "title": "Power outage Utrecht? No power at home | 24/7 | INO",
        "description": "Power outage in Utrecht today? Check in 1 minute whether it is your meter cupboard or the grid. Fault in your home: 24/7 electrician, fixed price upfront.",
        "h1": "No power at home? Find out within a minute where the problem is",
        "intro": "Suddenly everything is dark. Before you call anyone: two quick checks tell you whether the problem is in your own home or in the street's power grid. That saves time and avoids unnecessary costs.",
        "stappen_titel": "Do these checks, in this order",
        "stappen": [
            ["Look outside", "Are the street lights on and do the neighbours have power? If the whole street is without power, it is a grid outage. Call the free national outage number 0800-9009. An electrician cannot do anything about it."],
            ["Open your meter cupboard", "Is the main switch down, or one or more RCDs or circuit breakers? First switch off everything that uses a lot of power and then switch the switch back up once, calmly."],
            ["Does it trip again straight away?", "Don't keep trying and never hold the switch up or tape it in place. There is a real fault, such as a faulty appliance, moisture or a damaged cable. Call us and we will safely find the cause."],
            ["Everything is up but still no power?", "Then the problem may be in the connection before your meter (the main fuse). That belongs to the grid operator and you must not replace it yourself. Call us: we check whether it is in your installation. If it is the connection, we tell you honestly and you contact the grid operator."],
        ],
        "gevaar": "Can you smell burning, see smoke or sparks, or does the meter cupboard feel warm? Switch off the main switch if it is safe to do so, keep your distance and call 112 straight away if there is smoke or fire. Then call us for a safe repair.",
        "oorzaken_titel": "Common causes of a power cut at home",
        "oorzaken": [
            ["A faulty appliance", "A kettle, washing machine, oven or fridge with an internal fault makes the RCD trip."],
            ["Moisture", "An outdoor socket, garden lighting or bathroom where water gets in."],
            ["Overloading", "Too many heavy appliances at the same time on one circuit."],
            ["Damaged cable", "After drilling or hammering into the wall, or due to old wiring."],
        ],
        "faq": [
            ["Who should I call if the whole street has no power?", "Call the free national outage number 0800-9009. They pass the report on to the grid operator, which in Utrecht is Stedin. An electrician cannot fix outages in the public grid."],
            ["What does it cost if you come out for a power cut?", "During the day (08:00–18:00) you pay € {uur_dag} for the first hour, including VAT and diagnosis. In the evening (18:00–22:00) € {uur_avond}. At night (22:00–08:00) and all day on Saturdays, Sundays and public holidays € {uur_nacht}. Within the municipality of Utrecht there is no call-out charge."],
            ["Can I replace a fuse myself?", "You can switch a circuit breaker or RCD back up yourself. Unscrewing or replacing anything, no: leave that to an electrician. The main fuse before the meter belongs to the grid operator and may only be replaced by them."],
            ["How quickly can you be there?", "In the municipality of Utrecht usually within {aanrijtijd_utrecht} minutes, in the surrounding towns within {aanrijtijd_regio} minutes. Call us and you will hear a time straight away."],
        ],
    },
    "aardlekschakelaar-springt-eruit": {
        "kort": "RCD keeps tripping",
        "title": "RCD keeps tripping? Cause & help | INO Utrecht",
        "description": "Does your RCD keep tripping? This is how to find the appliance causing the fault. Can't find it? 24/7 electrician in Utrecht, fixed price upfront.",
        "h1": "RCD keeps tripping: how to find the cause",
        "intro": "An RCD (residual current device, in Dutch: aardlekschakelaar) switches off as soon as current 'leaks' away, for example through a faulty appliance or moisture. That is exactly its job: it protects you against an electric shock. The trick is to find where the leak is. You can often do that yourself in a few minutes.",
        "stappen_titel": "How to find the appliance",
        "stappen": [
            ["Unplug everything", "On the circuits behind that RCD (often the kitchen, bathroom or utility room). Also switch off fixed appliances such as a close-in water heater or hob if possible."],
            ["Switch the RCD up once", "Does it stay up now? Then the fault is in an appliance. Does it trip even without appliances? Then go to step 4."],
            ["Plug the appliances back in one by one", "Wait a moment each time. If the RCD trips with a particular appliance, you have found the culprit. Don't use that appliance again until it has been checked or replaced."],
            ["Does it trip without any appliances?", "Then the fault is in the installation itself: moisture in an (outdoor) socket or junction box, a damaged cable or a worn RCD. Don't keep switching it back on, call us. We test each circuit to find where the leak is."],
        ],
        "gevaar": "Never hold an RCD up by hand and never tape it in place. Then your protection no longer works and you risk an electric shock or fire.",
        "oorzaken_titel": "The most common culprits",
        "oorzaken": [
            ["Kettle, oven or dishwasher", "Heating elements start to leak after years of use. A classic cause."],
            ["Washing machine and dryer", "Especially if the RCD trips while washing or spinning."],
            ["Outdoor socket or garden lighting", "Moisture after rain. Does the RCD mainly trip in wet weather? Then this is often the cause."],
            ["An old RCD", "RCDs wear out too. Old ones sometimes trip for no reason."],
        ],
        "faq": [
            ["Is it dangerous if my RCD trips often?", "The RCD is doing its job: it protects you. But it does mean current is leaking away somewhere. Don't keep switching it back on if it trips again straight away, and have the cause found."],
            ["Why does the RCD trip when it rains?", "Almost always because of moisture in an outdoor socket, outdoor light, garden lighting or a cable to the shed. We fix that with watertight connections and the right IP rating."],
            ["What does it cost to have an RCD fault fixed?", "We work with a fixed hourly rate: € {uur_dag} for the first hour during the day, including VAT and diagnosis, with no call-out charge in Utrecht. In most cases the cause is found within that hour. If a part is needed, you hear the price first."],
            ["Why does the RCD trip at night?", "At night the appliances that switch on by themselves are running: fridge, freezer, water heater, or a dishwasher or washing machine with a delayed start. If one of those appliances has a leak, the RCD trips at the moment the appliance switches on. Moisture from dew or rain in an outdoor socket or garden lighting can also cause a fault at night. Does it happen more often? Call us and we will find the cause."],
            ["Can overloading make the RCD trip?", "Usually not. With too many appliances on one circuit, the circuit breaker of that circuit trips, not the RCD. Does the RCD trip when many appliances are on at the same time? Then together they are often leaking just a little too much current, or one of the appliances is faulty."],
            ["My RCD won't switch back on. What now?", "If it won't switch back on, or trips again immediately, there is a fault in an appliance or in the installation. Don't keep trying and never hold it up. Call us: we test to find where the leak is and replace the RCD if needed. You hear the price upfront."],
            ["How often should I use the test button?", "Press the test button (T) on each RCD a few times a year. It should switch off immediately. If it doesn't, have it replaced."],
        ],
    },
    "kortsluiting-utrecht": {
        "kort": "Short circuit / circuit trips",
        "title": "Short circuit or circuit tripping? Electrician Utrecht | INO",
        "description": "Does a circuit keep tripping or did you hear a bang? How to tell overloading from a short circuit. 24/7 electrician in Utrecht, fixed price upfront.",
        "h1": "Short circuit or a circuit that keeps tripping? How to tell the difference",
        "intro": "A circuit that trips can mean two things: overloading (too many appliances at once) or a short circuit (a real fault in an appliance or cable). You can tell the difference by when and how it trips.",
        "stappen_titel": "What to do now",
        "stappen": [
            ["Does it trip after a while, when a lot is switched on?", "That is usually overloading. Switch off a few heavy appliances (kettle, microwave, heater, air fryer) and switch the circuit breaker back up. Does it happen often? Then you need an extra circuit."],
            ["Does it trip as soon as you switch it on?", "That points to a short circuit. Unplug everything on that circuit and switch the circuit breaker up once."],
            ["Does it stay up without appliances?", "Plug the appliances back in one by one. The appliance that makes the circuit trip is faulty: stop using it."],
            ["Does it trip even without appliances?", "Then the short circuit is in the cable, a socket or a switch. Leave the circuit off and call us. Switching it back on repeatedly can cause damage and a fire risk."],
        ],
        "gevaar": "Do you see a black or melted spot at a socket, can you smell burning or did you hear a bang? Leave that circuit off, stop using the socket and call us. If there is smoke or fire: 112.",
        "oorzaken_titel": "Typical causes",
        "oorzaken": [
            ["Faulty lead or plug", "A damaged, kinked or old lead. Often visible as discolouration."],
            ["Loose connection in a socket", "A connection that gets hot and eventually short-circuits."],
            ["Drilling through a cable", "After putting up a shelf or a picture: a classic."],
            ["Too much on one circuit", "Lots of kitchen appliances or an electric heater on the same circuit."],
        ],
        "faq": [
            ["What is the difference between an RCD and a circuit breaker?", "A circuit breaker (MCB) protects against overloading and short circuits. An RCD protects against leaking current, such as in an electric shock. In modern fuse boxes they are often combined in one RCBO."],
            ["Can I have an extra circuit installed to prevent overloading?", "Yes. Adding an extra circuit costs from € {extra_groep}, depending on your fuse box. Send a photo of your meter cupboard and you will get a fixed price."],
            ["Do you also come out at night for a short circuit?", "Yes, we are available 24/7. At night, on Sundays and on public holidays the rate is € {uur_nacht} for the first hour, including VAT and diagnosis."],
        ],
    },
    "stopcontact-werkt-niet": {
        "kort": "Socket not working or getting hot",
        "title": "Socket not working or getting hot? | INO Utrecht",
        "description": "Socket not working, getting hot, discoloured or sparking? Check these points and know when it is dangerous. Electrician in Utrecht, fixed price upfront.",
        "h1": "Socket not working, getting hot or sparking? What you need to know",
        "intro": "A socket that doesn't work is often easy to explain. A socket that gets hot, crackles, sparks or discolours is a different story: that is a warning you should take seriously.",
        "stappen_titel": "Socket not working? Check this first",
        "stappen": [
            ["Test the appliance somewhere else", "Does the appliance work in another socket? Then the problem is in this socket or its circuit."],
            ["Look in the meter cupboard", "Is a circuit breaker or RCD down? Switch it up once. If it trips again, read our page about the RCD or short circuits."],
            ["Is it a switched socket?", "Some sockets switch on and off with a light switch. Try the switches in the room."],
            ["Still nothing?", "Then a connection has often come loose in the socket or a junction box. Don't open it yourself: call us and we will find it quickly and safely."],
        ],
        "gevaar": "Is a socket or plug getting hot, can you smell burning, do you hear crackling or see discolouration or sparks? Stop using it immediately, switch off the circuit in the meter cupboard and have it checked. Loose connections are a known cause of house fires.",
        "oorzaken_titel": "What we usually find",
        "oorzaken": [
            ["Loose wire", "From years of plugging in and out, or a connection that was never properly tightened."],
            ["Worn socket", "Old sockets with slack contacts where plugs sit loosely."],
            ["Overloading via power strips", "Several heavy appliances on one socket via a multi-plug."],
            ["No earth", "Old sockets without an earth, not suitable for appliances with an earthed plug."],
        ],
        "faq": [
            ["What does replacing a socket cost?", "Replacing an existing socket is usually well within the first hour (€ {uur_dag} during the day, incl. VAT, materials on request). Moving it to a new place costs from € {stopcontact_verleggen} per point."],
            ["Is a hot socket dangerous?", "Yes. A socket should not get hot. Heat usually means a poor connection or overloading, and that can cause a fire. Stop using it and have it checked."],
            ["Can you replace old sockets with earthed sockets?", "Often, yes, if there is an earth wire or one can be installed. We look on site and give you a fixed price upfront."],
        ],
    },
}
