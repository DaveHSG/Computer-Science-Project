# parts of the below city data was generated using ChatGPT, and has been manually verified
# this import function initialises the connection with SQLite 
import sqlite3
# this defines the list of activity types
activity_names = ["Culture & Historical Exploration", "Urban Entertainment & Nightlife", "Nature & Outdoor Adventure", "Relaxation & Wellness"]
# the following represents the list of city IDs, geolocation and country where it is
raw_city_data = {
    "Istanbul": (41.0082, 28.9784, "Turkey"),
    "Moscow": (55.7558, 37.6173, "Russia"),
    "London": (51.5074, -0.1278, "United Kingdom"),
    "Saint Petersburg": (59.9343, 30.3351, "Russia"),
    "Berlin": (52.52, 13.405, "Germany"),
    "Madrid": (40.4168, -3.7038, "Spain"),
    "Rome": (41.9028, 12.4964, "Italy"),
    "Kyiv": (50.4501, 30.5236, "Ukraine"),
    "Bucharest": (44.4268, 26.1025, "Romania"),
    "Paris": (48.8566, 2.3522, "France"),
    "Belgrade": (44.8176, 20.4633, "Serbia"),
    "Hamburg": (53.5511, 9.9937, "Germany"),
    "Basel": (47.5596, 7.5886, "Switzerland"),
    "Geneva": (46.2044, 6.1432, "Switzerland"),
    "Warsaw": (52.2298, 21.0118, "Poland"),
    "Budapest": (47.4979, 19.0402, "Hungary"),
    "Vienna": (48.2082, 16.3738, "Austria"),
    "Munich": (48.1351, 11.582, "Germany"),
    "Milan": (45.4642, 9.19, "Italy"),
    "Prague": (50.0755, 14.4378, "Czech Republic"),
    "Sofia": (42.6977, 23.3219, "Bulgaria"),
    "Amsterdam": (52.3676, 4.9041, "Netherlands"),
    "Stuttgart": (48.7758, 9.1829, "Germany"),
    "Stockholm": (59.3293, 18.0686, "Sweden"),
    "Lisbon": (38.7169, -9.1395, "Portugal"),
    "Oslo": (59.9139, 10.7522, "Norway"),
    "Athens": (37.9838, 23.7275, "Greece"),
    "Copenhagen": (55.6761, 12.5683, "Denmark"),
    "Zürich": (47.3769, 8.5417, "Switzerland"),
    "Antwerp": (51.2194, 4.4025, "Belgium"),
    "Kraków": (50.0647, 19.945, "Poland"),
    "Minsk": (53.9, 27.5667, "Belarus"),
    "Tallinn": (59.437, 24.7535, "Estonia"),
    "Helsinki": (60.1699, 24.9384, "Finland"),
    "Chisinau": (47.0105, 28.8638, "Moldova"),
    "Belfast": (54.5973, -5.9301, "United Kingdom"),
    "Vilnius": (54.6892, 25.2798, "Lithuania"),
    "Riga": (56.946, 24.1059, "Latvia"),
    "Zagreb": (45.8131, 15.978, "Croatia"),
    "Sarajevo": (43.8486, 18.3564, "Bosnia and Herzegovina"),
    "Skopje": (41.9981, 21.4254, "North Macedonia"),
    "Tbilisi": (41.7151, 44.8271, "Georgia"),
    "Baku": (40.4093, 49.8671, "Azerbaijan"),
    "Dublin": (53.3498, -6.2603, "Ireland"),
    "Bristol": (51.4545, -2.5879, "United Kingdom"),
    "Cardiff": (51.4816, -3.1791, "United Kingdom"),
    "Manchester": (53.4808, -2.2426, "United Kingdom"),
    "Leeds": (53.8, -1.5491, "United Kingdom"),
    "Liverpool": (53.4084, -2.9916, "United Kingdom"),
    "Newcastle upon Tyne": (54.9783, -1.617, "United Kingdom"),
    "Sheffield": (53.3811, -1.4701, "United Kingdom"),
    "Nottingham": (52.9548, -1.1581, "United Kingdom"),
    "Leicester": (52.6369, -1.1398, "United Kingdom"),
    "Bradford": (53.7956, -1.7599, "United Kingdom"),
    "Coventry": (52.408, -1.5102, "United Kingdom"),
    "Birmingham": (52.4862, -1.8904, "United Kingdom"),
    "Glasgow": (55.8642, -4.2518, "United Kingdom"),
    "Edinburgh": (55.9533, -3.1883, "United Kingdom"),
    "Ljubljana": (46.0511, 14.5051, "Slovenia"),
    "Tirana": (41.3275, 19.8189, "Albania")
}

# the following lists 8 activites per type, for each of the above cities
custom_city_activities = {
   "Basel": {
        "Culture & Historical Exploration": [
            "Kunstmuseum Basel",
            "Basel Minster",
            "Foundation Beyeler",
            "Spalentor City Gate",
            "Museum Tinguely",
            "Pharmacy Museum",
            "Antikenmuseum (Roman Antiquities)",
            "Basel Historical Museum"
        ],
        "Urban Entertainment & Nightlife": [
            "Bar Rouge",
            "Atlantis Club",
            "Volkshaus Basel",
            "Hinterhof Bar",
            "Ufer 7 Concert Venue",
            "Les Trois Rois Hotel Bar",
            "Kaserne Basel (Live Music)",
            "Englische Botschaft Bar"
        ],
        "Nature & Outdoor Adventure": [
            "Rhine River Cruise",
            "Basel Zoo",
            "Merian Gärten",
            "Botanical Garden of the University",
            "Hike on St. Chrischona",
            "Jogging along the Rhine",
            "Flight over the Jura mountains",
            "Cycle the Drei-Länder-Route"
        ],
        "Relaxation & Wellness": [
            "Aquabasilea Spa",
            "Les Bains de Lavey (day trip)",
            "Thermalbad Brigerbad (day trip)",
            "Yoga at YogaOne Basel",
            "Massage at Malerin Spa",
            "Sauna at Sole Uno",
            "Floating session at Float Basel",
            "Wellness package at Grand Hotel Les Trois Rois"
        ]
    },

    "Geneva": {
        "Culture & Historical Exploration": [
            "Jet d’Eau",
            "Palais des Nations (UN)",
            "Musée d’Art et d’Histoire",
            "St. Pierre Cathedral",
            "Reformation Wall",
            "Patek Philippe Museum",
            "Old Town Walking Tour",
            "Maison Tavel"
        ],
        "Urban Entertainment & Nightlife": [
            "Java Club",
            "La Gravière",
            "Bains des Pâquis Bar",
            "Le Baroque",
            "Rive Gauche",
            "Mr. Pickwick Pub",
            "Bâloise Session Concert Hall",
            "Moujik Russian Bar"
        ],
        "Nature & Outdoor Adventure": [
            "Lake Geneva Boat Tour",
            "Mont Salève Hike",
            "Jet Ski on the lake",
            "Bicycle along the Rhône",
            "Paragliding from Saleve",
            "Kayaking in the Arve",
            "Winter skiing at nearby resorts",
            "Flower clock & English Garden stroll"
        ],
        "Relaxation & Wellness": [
            "Bains des Pâquis Sauna",
            "Hammam Parc des Bastions",
            "Spa at Hôtel de la Paix",
            "Floating therapy at Float4Life",
            "Yoga on the lake shore",
            "Thermal baths in Val d’Illiez (day trip)",
            "Massage at Willow Spa",
            "Wellness center at InterContinental"
        ]
    },

    "Istanbul": {
        "Culture & Historical Exploration": [
            "Hagia Sophia",
            "Topkapi Palace",
            "Blue Mosque",
            "Basilica Cistern",
            "Grand Bazaar",
            "Suleymaniye Mosque",
            "Chora Church",
            "Istanbul Archaeology Museums"
        ],
        "Urban Entertainment & Nightlife": [
            "Taksim Square bars",
            "Kadıköy pub crawl",
            "360 Istanbul (rooftop club)",
            "Sortie Dinner Cruises",
            "Babylon Bomonti",
            "Nardis Jazz Club",
            "Reina (Bosporus nightclub)",
            "Zorlu PSM concerts"
        ],
        "Nature & Outdoor Adventure": [
            "Bosphorus Cruise",
            "Princes’ Islands bike tour",
            "Çamlıca Hill lookout",
            "Belgrad Forest hike",
            "Ferry to Heybeliada",
            "Stand-up paddle on the Bosphorus",
            "Golden Horn kayak trip",
            "Sunset at Pierre Loti Hill"
        ],
        "Relaxation & Wellness": [
            "Hürrem Sultan Hammam",
            "Çemberlitaş Hamam",
            "Ayasofya Hürrem Sultan",
            "Kılıç Ali Paşa Hamam",
            "Spa at Four Seasons Sultanahmet",
            "Thermal baths in Yalova (day trip)",
            "Rooftop pool at Swissôtel",
            "Massage at House Hotel Spa"
        ]
    },
    "Moscow": {
        "Culture & Historical Exploration": [
            "Red Square",
            "The Kremlin",
            "St. Basil’s Cathedral",
            "Tretyakov Gallery",
            "Bolshoi Theatre tour",
            "Lenin’s Mausoleum",
            "Gorky Park sculpture walk",
            "Novodevichy Convent"
        ],
        "Urban Entertainment & Nightlife": [
            "Arbat Street cafés",
            "Bolotnaya Naberezhnaya clubs",
            "Kriek Bar",
            "Gipsy Bar",
            "Icon Club",
            "Mendeleev Bar (cocktails)",
            "Garage Museum late openings",
            "RAMPA jazz club"
        ],
        "Nature & Outdoor Adventure": [
            "Gorky Park bike rental",
            "Skating at VDNKh (winter)",
            "Picnic on Sparrow Hills",
            "Boat ride on the Moskva River",
            "Hiking in Losiny Ostrov",
            "Kayaking around islands",
            "Zip-lining at Ramenskoye Park",
            "Horse riding in Tsaritsyno"
        ],
        "Relaxation & Wellness": [
            "Sanduny Bathhouse",
            "Korean Spa Buzz Bar",
            "Thermae Spa at Metropol",
            "Float pod at Spa VODA",
            "Massage at Arfa Wellness",
            "Sauna at Leto Spa",
            "Yoga at PRO.YOGA",
            "Steam rooms in VODA"
        ]
    },
   "London": {
        "Culture & Historical Exploration": [
            "British Museum",
            "Tower of London",
            "National Gallery",
            "Tate Modern",
            "Westminster Abbey",
            "Victoria & Albert Museum",
            "Imperial War Museum",
            "Natural History Museum",
        ],
        "Urban Entertainment & Nightlife": [
            "Soho bars",
            "Camden Town live music",
            "Shoreditch street art crawl",
            "Covent Garden pubs",
            "Brixton Village food market",
            "Mayfair cocktail lounges",
            "Dalston clubs",
            "South Bank late-night riverside",
        ],
        "Nature & Outdoor Adventure": [
            "Thames kayak tours",
            "Hyde Park boating",
            "Regent’s Park rose garden",
            "Kew Gardens greenhouse walk",
            "Richmond Park deer spotting",
            "Hampstead Heath hilltop views",
            "Little Venice canal cruise",
            "Greenwich Park observatory hill",
        ],
        "Relaxation & Wellness": [
            "AIRE Ancient Baths",
            "ESPA Life at Corinthia",
            "Bamford Haybarn Spa",
            "Thai Square Spa",
            "Cowshed Spa Shoreditch",
            "Mandarin Oriental spa",
            "Floatworks sensory deprivation",
            "K West Spa & Gym",
        ],
    },
    "Saint Petersburg": {
        "Culture & Historical Exploration": [
            "Hermitage Museum",
            "Peter & Paul Fortress",
            "Church of the Savior on Spilled Blood",
            "Yusupov Palace",
            "State Russian Museum",
            "Kazan Cathedral",
            "Fabergé Museum",
            "St. Isaac’s Cathedral",
        ],
        "Urban Entertainment & Nightlife": [
            "Nevsky Prospect pubs",
            "Rubinstein Street bars",
            "DJs at DYadzya Club",
            "Jazz at SVoI",
            "Rooftop at Dom",
            "Underground at RED",
            "Live gigs at A2 Green Concert",
            "Kuda-go late-night theater",
        ],
        "Nature & Outdoor Adventure": [
            "Icebreaker cruise on Neva",
            "Summer Garden strolls",
            "Peterhof Park fountain tours",
            "Tsarskoye Selo palace gardens",
            "Krestovsky Island biking",
            "Kronstadt island ferry ride",
            "Kamenny Island forest walk",
            "Yelagin Island picnic",
        ],
        "Relaxation & Wellness": [
            "Sanduny historic banya",
            "Troyka Russian bath",
            "SAINT PETERSBURG Dubai SPA",
            "Corston Royal Hotel spa",
            "Spa at Kempinski",
            "Leto wellness center",
            "Panorama city spa",
            "White Nights massage",
        ],
    },
    "Berlin": {
        "Culture & Historical Exploration": [
            "Brandenburg Gate",
            "Museum Island (Pergamon)",
            "Berlin Wall Memorial",
            "Checkpoint Charlie",
            "Holocaust Memorial",
            "Reichstag Dome",
            "East Side Gallery",
            "Altes Museum",
        ],
        "Urban Entertainment & Nightlife": [
            "Berghain techno club",
            "Kreuzberg cocktail bars",
            "Friedrichshain clubs",
            "Prenzlauer Berg pubs",
            "RAW-Gelände street art",
            "Alexandraplatz late bars",
            "Multipass bar crawl",
            "Späti street beer gardens",
        ],
        "Nature & Outdoor Adventure": [
            "Spree River boat tour",
            "Tempelhofer Feld cycling",
            "Tiergarten picnics",
            "Grunewald forest hikes",
            "Wannsee lake swimming",
            "Müggelsee kayaking",
            "Treptower Park strolls",
            "Volkspark Friedrichshain",
        ],
        "Relaxation & Wellness": [
            "Vabali Spa",
            "Liquidrom saltwater float",
            "Badeschiff sauna boat",
            "Spreewelten thermal spa",
            "Carlsson Sand Spa",
            "Amphibisch Spa Lounge",
            "Schöneberg thai massage",
            "Berlin Vital Day Spa",
        ],
    },
    "Madrid": {
        "Culture & Historical Exploration": [
            "Prado Museum",
            "Royal Palace of Madrid",
            "Reina Sofía Museum",
            "Thyssen-Bornemisza",
            "Temple of Debod",
            "Almudena Cathedral",
            "Puerta del Sol",
            "Plaza Mayor",
        ],
        "Urban Entertainment & Nightlife": [
            "Gran Vía theaters",
            "Chueca bars",
            "Malasaña live music",
            "La Latina tapas crawl",
            "Huertas cocktail lounges",
            "Lavapiés flamenco shows",
            "Salamanca district clubs",
            "Rooftop at Círculo de Bellas Artes",
        ],
        "Nature & Outdoor Adventure": [
            "Retiro Park boating",
            "Casa de Campo cycling",
            "Madrid Río riverside walk",
            "Sierra de Guadarrama hike",
            "Madrid Botanical Garden",
            "El Capricho Park",
            "Parque Juan Carlos I",
            "Teleférico cable car",
        ],
        "Relaxation & Wellness": [
            "Hammam Al Ándalus",
            "Spa at Hotel Urso",
            "Club de Campo wellness",
            "Zentro Urban Spa",
            "Kinépolis screening spa",
            "Mandarin Oriental massage",
            "Yoga at Templo del Yoga",
            "Float Center Madrid",
        ],
    },
    "Rome": {
        "Culture & Historical Exploration": [
            "Colosseum",
            "Vatican Museums",
            "Pantheon",
            "Roman Forum",
            "St. Peter’s Basilica",
            "Castel Sant’Angelo",
            "Capitoline Museums",
            "Galleria Borghese",
        ],
        "Urban Entertainment & Nightlife": [
            "Trastevere piazzas",
            "Campo de’ Fiori bars",
            "Testaccio clubs",
            "Monti wine bars",
            "Pigneto street art bars",
            "Navona live music",
            "Colonna rooftop lounges",
            "San Lorenzo student bars",
        ],
        "Nature & Outdoor Adventure": [
            "Gianicolo Hill walk",
            "Appian Way cycling",
            "Villa Borghese rowing",
            "Orange Garden viewpoint",
            "Tiber River kayaking",
            "Villa Doria Pamphili",
            "Janiculum Park",
            "Aventine Keyhole peek",
        ],
        "Relaxation & Wellness": [
            "QC Terme Roma",
            "AIRE Ancient Baths Rome",
            "Caldarium at Hotel Eden",
            "St. Peter’s spa",
            "The Spa at Rome Cavalieri",
            "Hammam di Roma",
            "Terme di Caracalla (thermal ruins)",
            "Massages at Hotel de Russie",
        ],
    },
    "Kyiv": {
        "Culture & Historical Exploration": [
            "St. Sophia’s Cathedral",
            "Kiev Pechersk Lavra",
            "Maiden Square",
            "Golden Gate",
            "National Art Museum",
            "Andriyivskyy Descent",
            "Museum of The History of Ukraine",
            "St. Michael’s Golden-Domed Monastery",
        ],
        "Urban Entertainment & Nightlife": [
            "Arena City complex",
            "Podil district bars",
            "Khreshchatyk late pubs",
            "Lyalka nightclub",
            "Caribbean Club concerts",
            "Les Kurbas boulevard cafes",
            "SkyBar rooftop",
            "Time Club techno",
        ],
        "Nature & Outdoor Adventure": [
            "Dnipro River cruise",
            "Hydropark beaches",
            "Mariinsky Park stroll",
            "Pushcha-Voditsa forest",
            "Kyiv Botanic Garden",
            "Park of Eternal Glory",
            "Volodymyrska Hill views",
            "Mezhyhirya Residence grounds",
        ],
        "Relaxation & Wellness": [
            "Tsarsky City Resort spa",
            "Mandarin Oriental massages",
            "Senatoriy Hotel spa",
            "Sofiyskiy Banya",
            "Arsenal Boutique spa",
            "Float Station Kyiv",
            "Mukhtar SPA centre",
            "Kreschatik Spa",
        ],
    },
    "Bucharest": {
        "Culture & Historical Exploration": [
            "Palace of the Parliament",
            "Romanian Athenaeum",
            "Village Museum",
            "National Museum of Art",
            "Stavropoleos Monastery",
            "Revolution Square",
            "Cotroceni Palace",
            "National History Museum",
        ],
        "Urban Entertainment & Nightlife": [
            "Old Town Lipscani pubs",
            "Control Club concerts",
            "Eden Club techno",
            "Expirat live music",
            "Fratelli bars",
            "The Drunken Rat microbrewery",
            "Kristal Glam Club",
            "Piazza cafe bars",
        ],
        "Nature & Outdoor Adventure": [
            "Herăstrău Park boating",
            "Carol Park strolls",
            "Botanical Garden",
            "Vacaresti Delta birdwatching",
            "Mogosoaia Palace grounds",
            "Tineretului Park cycling",
            "Baneasa Forest trails",
            "Cerna Lake day trip",
        ],
        "Relaxation & Wellness": [
            "Therme București",
            "EMA SPA Romanian pebbles",
            "Soma Wellness Club",
            "Orhideea Gym & Spa",
            "Centru Wellness EdenLand",
            "Anahata SPA",
            "Float Zone Bucharest",
            "Senatorski Spa",
        ],
    },
    "Paris": {
        "Culture & Historical Exploration": [
            "Louvre Museum",
            "Notre-Dame Cathedral",
            "Musée d’Orsay",
            "Centre Pompidou",
            "Palace of Versailles",
            "Sainte-Chapelle",
            "Arc de Triomphe",
            "Château de Fontainebleau",
        ],
        "Urban Entertainment & Nightlife": [
            "Moulin Rouge shows",
            "Le Marais cocktail bars",
            "Latin Quarter pubs",
            "Pigalle nightclubs",
            "Rooftop at Georges",
            "Canal Saint-Martin bars",
            "Oberkampf live venues",
            "Bastille jazz clubs",
        ],
        "Nature & Outdoor Adventure": [
            "Seine river cruise",
            "Montmartre walks",
            "Luxembourg Gardens",
            "Bois de Boulogne cycling",
            "Parc des Buttes-Chaumont",
            "Île de la Cité strolls",
            "Tuileries Garden rowing",
            "Vincennes Forest",
        ],
        "Relaxation & Wellness": [
            "Hammam Pacha",
            "Spa My Blend Clarins",
            "Molitor Thermal spa",
            "Deep Nature floating pods",
            "Ban Thaï massages",
            "Nuxe Montorgueil spa",
            "Floating Buoy Zen spa",
            "Le Roch Hotel spa",
        ],
    },
    "Belgrade": {
        "Culture & Historical Exploration": [
            "Belgrade Fortress",
            "Nikola Tesla Museum",
            "St. Sava Temple",
            "National Museum",
            "House of the National Assembly",
            "Church of Saint Mark",
            "Gallery of Matica Srpska",
            "Zemun Old Town",
        ],
        "Urban Entertainment & Nightlife": [
            "Skadarlija taverns",
            "Savamala clubs",
            "River clubs on the Sava",
            "Cetinel LGBTQ+ bars",
            "Barutana events venue",
            "Jazz clubs at Black Turtle",
            "Beton Hala waterfront",
            "Blaznavac underground",
        ],
        "Nature & Outdoor Adventure": [
            "Ada Ciganlija lake",
            "Košutnjak forest trails",
            "Great War Island birdwatching",
            "Topčider Park",
            "Avalski Toranj climb",
            "Belgrade Zoo",
            "Beli dvor gardens",
            "Šumice Park boating",
        ],
        "Relaxation & Wellness": [
            "Royal Spa Belgrade",
            "Spa at Hyatt Regency",
            "Lepota Wellness center",
            "Hungarikum SPA",
            "Sauna at Mona Hotel",
            "Villa Svilara day spa",
            "Float in Belgrade pods",
            "Aqua park Yonca",
        ],
    },
    "Hamburg": {
        "Culture & Historical Exploration": [
            "Miniatur Wunderland",
            "Elbphilharmonie",
            "Hamburg Rathaus",
            "Kunsthalle Hamburg",
            "St. Michael’s Church",
            "International Maritime Museum",
            "Speicherstadt warehouses",
            "Deichtorhallen art halls",
        ],
        "Urban Entertainment & Nightlife": [
            "Reeperbahn clubs",
            "St. Pauli pubs",
            "Sternschanze bars",
            "Karolinenviertel street art venues",
            "HafenCity rooftop lounges",
            "Jazz at Cotton Club",
            "Molotow live music",
            "Night cruise on Elbe",
        ],
        "Nature & Outdoor Adventure": [
            "Harbor boat tour",
            "Planten un Blomen gardens",
            "Alster lake kayaking",
            "Wohldorfer Forest hikes",
            "Öjendorfer Park cycling",
            "Elbe beach strolls",
            "Övelgönne riverside walk",
            "Jenisch Park woods",
        ],
        "Relaxation & Wellness": [
            "Holthusenbad spa",
            "MIRAMAR Therme",
            "Sauna at Vier Jahreszeiten",
            "Floatworks Hamburg",
            "Aquadrom Bad Oldesloe",
            "You & Mee Spa Hamburg",
            "AIRE Ancient Baths Seville (in Spain) [day trip]",
            "SkySpa Hamburg airport",
        ],
    },
    "Warsaw": {
        "Culture & Historical Exploration": [
            "Royal Castle",
            "POLIN Museum",
            "Łazienki Palace",
            "Warsaw Uprising Museum",
            "National Museum",
            "Copernicus Science Centre",
            "Barbakan Barbican",
            "St. John’s Archcathedral",
        ],
        "Urban Entertainment & Nightlife": [
            "Pawilony bars",
            "Nowy Świat street cafes",
            "Praga district clubs",
            "Hala Koszyki food hall",
            "Nightlife at Plac Zbawiciela",
            "Hydrozagadka concerts",
            "Opera Club techno",
            "Bar Studio at Palace",
        ],
        "Nature & Outdoor Adventure": [
            "Vistula River kayaking",
            "Łazienki park boating",
            "Wilanów Palace gardens",
            "Saxon Gardens strolls",
            "Kampinos Forest day trip",
            "Skaryszewski Lakes Park",
            "Warsaw Zoo visit",
            "Bielany forest hiking",
        ],
        "Relaxation & Wellness": [
            "Termy Mszczonów thermal baths",
            "Holistic Spa by Sheraton",
            "Golden Tulip massage",
            "Float house Warsaw",
            "Dr Irena Eris Spa",
            "Birth Spa Hotel Bristol",
            "Sauna on a boat at Vistula",
            "Masaże Na LUZIE massage bar",
        ],
    },
    "Budapest": {
        "Culture & Historical Exploration": [
            "Buda Castle",
            "Hungarian Parliament",
            "Fisherman’s Bastion",
            "Heroes’ Square",
            "Széchenyi Chain Bridge",
            "Gellért Hill Citadel",
            "House of Terror Museum",
            "Matthias Church",
        ],
        "Urban Entertainment & Nightlife": [
            "Ruin bars in District VII",
            "Gozsdu Courtyard pubs",
            "A38 ship club",
            "Instant ruin club",
            "Szimpla Kert",
            "Corvin Club rooftop",
            "Café Csiga wine bar",
            "Boutiq’Bar cocktails",
        ],
        "Nature & Outdoor Adventure": [
            "Széchenyi Thermal Bath outdoors",
            "Danube river cruise",
            "Margaret Island cycling",
            "Normafa forest hikes",
            "Gödöllő palace grounds",
            "Buda Hills chairlift",
            "Danube Bend day trip",
            "Tabán Park strolls",
        ],
        "Relaxation & Wellness": [
            "Széchenyi Spa indoor pools",
            "Gellért Spa Art Nouveau baths",
            "Rudas Bath Ottoman pool",
            "Király thermal bath",
            "Spa at Four Seasons",
            "Float spa Budapest",
            "Mandarin Oriental massages",
            "Lake Hévíz day trip",
        ],
    },
    "Vienna": {
        "Culture & Historical Exploration": [
            "Schönbrunn Palace",
            "Hofburg Imperial Palace",
            "Belvedere Museum",
            "St. Stephen’s Cathedral",
            "Kunsthistorisches Museum",
            "Spanish Riding School",
            "Albertina",
            "Karlskirche"
        ],
        "Urban Entertainment & Nightlife": [
            "Gürtel Bars",
            "Bermuda Triangle District",
            "Pratersauna Club",
            "Flex Waterside Club",
            "Donaukanal Beer Gardens",
            "Volksgarten Disco",
            "Jazzland",
            "U4 Club"
        ],
        "Nature & Outdoor Adventure": [
            "Danube Island Cycling",
            "Donaukanal Kayaking",
            "Vienna Woods Hiking",
            "Prater Park Rides",
            "Lainzer Tiergarten Walks",
            "Danube Bike Path",
            "Kahlenberg Summit Hike",
            "Augarten Park Strolling"
        ],
        "Relaxation & Wellness": [
            "Therme Wien",
            "Rooftop Spas at Ritz-Carlton",
            "Juvavum Spa",
            "Sans Souci Spa",
            "AVITA Spa",
            "Gästehaus Klinik Spa",
            "Aire Ancient Baths",
            "Linsberg Asia Spa"
        ]
    },
    "Munich": {
        "Culture & Historical Exploration": [
            "Marienplatz & Neues Rathaus",
            "Nymphenburg Palace",
            "Deutsches Museum",
            "Munich Residenz",
            "Alte Pinakothek",
            "Asam Church",
            "Frauenkirche",
            "Viktualienmarkt"
        ],
        "Urban Entertainment & Nightlife": [
            "Glockenbachviertel Bars",
            "Schwabing District",
            "Atomic Café",
            "Harry Klein Club",
            "Pusser’s Bar",
            "Backstage",
            "Biergarten am Chinesischen Turm",
            "Muffatwerk"
        ],
        "Nature & Outdoor Adventure": [
            "Englischer Garten Surfing",
            "Isar River Kayaking",
            "Olympiapark Cycling",
            "Tegernsee Day Trip",
            "Starnberger See Boating",
            "Hirschgarten Park",
            "Partnach Gorge Hike",
            "Eibsee Excursion"
        ],
        "Relaxation & Wellness": [
            "Therme Erding",
            "Müller’sches Volksbad",
            "Watzmann Therme",
            "Königliche Kristall-Therme",
            "Hotel Bayerischer Hof Spa",
            "Mandarin Oriental Spa",
            "Rocco Forte Spa",
            "Blue Spa at Sofitel"
        ]
    },
    "Milan": {
        "Culture & Historical Exploration": [
            "Duomo di Milano",
            "Galleria Vittorio Emanuele II",
            "Sforza Castle",
            "Santa Maria delle Grazie (Last Supper)",
            "La Scala Opera House",
            "Pinacoteca di Brera",
            "Navigli Canals",
            "Castello Sforzesco Museums"
        ],
        "Urban Entertainment & Nightlife": [
            "Brera District Bars",
            "Navigli District Clubs",
            "Armani Privé",
            "Just Cavalli",
            "Hollywood Rythmoteque",
            "Mag Cafè",
            "Plastic Milan",
            "Tunnel Club"
        ],
        "Nature & Outdoor Adventure": [
            "Parco Sempione Walks",
            "Navigli Boat Tours",
            "Monte Stella Park",
            "Idroscalo Lake",
            "CityLife Park",
            "Brera Botanical Garden",
            "Civico Planetario Visit",
            "Parco Nord Milano"
        ],
        "Relaxation & Wellness": [
            "QC Termemilano",
            "Spa at Bulgari Hotel",
            "AIRE Ancient Baths",
            "Four Seasons Spa",
            "Mandarin Oriental Spa",
            "Armani/Spa",
            "Châteauform Spa",
            "Respirart Spa"
        ]
    },
    "Prague": {
        "Culture & Historical Exploration": [
            "Prague Castle",
            "Charles Bridge",
            "Old Town Square & Astronomical Clock",
            "St. Vitus Cathedral",
            "Jewish Quarter (Josefov)",
            "National Gallery",
            "Lennon Wall",
            "Strahov Monastery"
        ],
        "Urban Entertainment & Nightlife": [
            "Karlovy Lazne Club",
            "Cross Club",
            "Lucerna Music Bar",
            "Roxy",
            "Chapeau Rouge",
            "JazzDock",
            "Hemingway Bar",
            "BeerGeek Bar"
        ],
        "Nature & Outdoor Adventure": [
            "Petrin Hill & Tower",
            "Vltava River Kayaking",
            "Letna Park Stroll",
            "Divoká Šárka Hiking",
            "Vyšehrad Fortress Walk",
            "Stromovka Park Cycling",
            "Boat Ride on Vltava",
            "Troja Chateau Gardens"
        ],
        "Relaxation & Wellness": [
            "Beer Spa Bernard",
            "Lazne Pramen Spa",
            "Saunia Sauna Park",
            "Wellness & Spa at Four Seasons",
            "Mama Spa",
            "Wellness Hotel Step",
            "Alpine Club Spa",
            "Coco Spa"
        ]
    },
    "Sofia": {
        "Culture & Historical Exploration": [
            "Alexander Nevsky Cathedral",
            "Boyana Church",
            "National Palace of Culture",
            "Sofia History Museum",
            "Saint Sofia Church",
            "Vitosha Boulevard",
            "Ivan Vazov National Theatre",
            "Russian Church"
        ],
        "Urban Entertainment & Nightlife": [
            "Vitosha Blvd Bars",
            "PM Club",
            "Bedroom Premium Club",
            "Yalta Club",
            "Reservoir Dogs",
            "Terminal 1",
            "One More Bar",
            "The Steps"
        ],
        "Nature & Outdoor Adventure": [
            "Vitosha Mountain Hike",
            "Dragalevtsi Monastery Trail",
            "Zlatnite Mostove",
            "South Park Cycling",
            "Boyana Waterfall",
            "Vrabnitsa Park",
            "Borisova Gradina",
            "Aleko Hut Excursion"
        ],
        "Relaxation & Wellness": [
            "Sense Hotel Spa",
            "Aquahouse Thermal & Beach",
            "Elements Spa",
            "Le SPA at Grand Hotel Sofia",
            "Spa Club Sense",
            "Sofia Spa Center",
            "ARTE Spa",
            "Hilton Sofia Spa"
        ]
    },
    "Amsterdam": {
        "Culture & Historical Exploration": [
            "Rijksmuseum",
            "Van Gogh Museum",
            "Anne Frank House",
            "Dam Square & Royal Palace",
            "Stedelijk Museum",
            "Begijnhof",
            "Hermitage Amsterdam",
            "Westerkerk"
        ],
        "Urban Entertainment & Nightlife": [
            "Leidseplein Squares",
            "Rembrandtplein District",
            "Paradiso",
            "Melkweg",
            "Bitterzoet",
            "Canvas Rooftop",
            "Claire Café",
            "De School"
        ],
        "Nature & Outdoor Adventure": [
            "Canal Boat Tour",
            "Vondelpark Cycling",
            "Amstel River Kayaking",
            "Hortus Botanicus",
            "Amsterdamse Bos",
            "Zaanse Schans Windmills",
            "Marken & Volendam Day Trip",
            "Pampus Island"
        ],
        "Relaxation & Wellness": [
            "Spa Zuiver",
            "Sauna Deco & Wellness",
            "AIRE Ancient Baths",
            "Hotel Okura Spa",
            "Wellness 1926",
            "Babylon Health Club",
            "Armani/Spa Amsterdam",
            "The City Street Spa"
        ]
    },
    "Stuttgart": {
        "Culture & Historical Exploration": [
            "Mercedes-Benz Museum",
            "Porsche Museum",
            "Staatsgalerie Stuttgart",
            "Old Castle (Altes Schloss)",
            "Ludwigsburg Palace",
            "Kunstmuseum Stuttgart",
            "Wilhelma Zoo & Botanical Garden",
            "Markthalle"
        ],
        "Urban Entertainment & Nightlife": [
            "Schankstelle Club",
            "Climax Institutes",
            "Lehmann Club",
            "Kowalski",
            "Tasch’n",
            "Porsche Arena Events",
            "Kulturbrauerei",
            "Alte Kanzlei Bar"
        ],
        "Nature & Outdoor Adventure": [
            "Killesberg Park",
            "Forest Trails of the Black Forest",
            "Neckar River Cruise",
            "Bärensee Hike",
            "Solitude Palace Grounds",
            "Uracher Waterfall Day Trip",
            "Birkenkopf Hill Viewpoint",
            "Max-Eyth-See"
        ],
        "Relaxation & Wellness": [
            "Mineralbad Berg",
            "Vabali Spa Stuttgart",
            "Panoramabad Leuze",
            "Friedrichsbad Thermal Bath",
            "Bäder Viadukt",
            "Zahn Spa",
            "Wellness im Dorint",
            "Hotel Traube Tonbach Spa"
        ]
    },
    "Stockholm": {
        "Culture & Historical Exploration": [
            "Vasa Museum",
            "Gamla Stan Old Town",
            "Skansen Open-Air Museum",
            "Royal Palace",
            "Fotografiska",
            "ABBA The Museum",
            "Moderna Museet",
            "Nobel Museum"
        ],
        "Urban Entertainment & Nightlife": [
            "Stureplan Clubs",
            "Berns Salonger",
            "Icebar by ICEHOTEL",
            "Trädgården",
            "F12 Terrassen",
            "Mosebacke Etablissement",
            "Debaser Strand",
            "Marie Laveau"
        ],
        "Nature & Outdoor Adventure": [
            "Archipelago Boat Tour",
            "Djurgården Cycling",
            "Hagaparken Walk",
            "Kayaking under City Bridges",
            "Riddarholmen Stroll",
            "Tyresta National Park",
            "Långholmen Island",
            "Brunnsviken Rowing"
        ],
        "Relaxation & Wellness": [
            "Sturebadet Spa",
            "Selma City Spa",
            "Nobis Holistic Spa",
            "Yasuragi Japanese Spa",
            "Centralbadet",
            "Chokladfabriken Spa",
            "Clarion Spa",
            "Hotel Diplomat Spa"
        ]
    },
    "Lisbon": {
        "Culture & Historical Exploration": [
            "Belém Tower",
            "Jerónimos Monastery",
            "São Jorge Castle",
            "Alfama District",
            "National Tile Museum",
            "Carmo Convent",
            "Commerce Square",
            "Lisbon Cathedral"
        ],
        "Urban Entertainment & Nightlife": [
            "Bairro Alto Bars",
            "Cais do Sodré Clubs",
            "Lux Frágil",
            "Park Rooftop Bar",
            "Pensão Amor",
            "MusicBox",
            "Casa Independente",
            "Foxtrot"
        ],
        "Nature & Outdoor Adventure": [
            "Tram 28 Ride",
            "Sintra Day Trip",
            "Belém Riverside Walk",
            "Arrábida Hike",
            "Costa da Caparica Surfing",
            "Tagus Estuary Birdwatching",
            "Moorish Castle Hike",
            "Monsanto Forest"
        ],
        "Relaxation & Wellness": [
            "Lisboa Rio Spa",
            "Float in Spa",
            "Four Seasons Spa Lisbon",
            "Bairro Alto Hotel Spa",
            "Corpo Santo Wellness",
            "The Spa at Tivoli Avenida",
            "Penha Longa Spa",
            "Lifecool Physiotherapy & Spa"
        ]
    },
    "Oslo": {
        "Culture & Historical Exploration": [
            "Viking Ship Museum",
            "Akershus Fortress",
            "National Gallery",
            "Munch Museum",
            "Holmenkollen Ski Museum",
            "Opera House Rooftop",
            "Fram Museum",
            "Kon-Tiki Museum"
        ],
        "Urban Entertainment & Nightlife": [
            "Bar Vulkan",
            "Blå Club",
            "The Villa",
            "Lawrence",
            "Jaeger",
            "Katakomben",
            "Lektern Barge",
            "Soho Oslo"
        ],
        "Nature & Outdoor Adventure": [
            "Oslofjord Kayaking",
            "Hiking in Nordmarka",
            "Boat Tour on the Fjord",
            "Bygdøy Peninsula Cycling",
            "Sognsvann Lake Swim",
            "Kjeragbolten Day Trip",
            "Holmenkollen Trail Run",
            "Museum Island Walks"
        ],
        "Relaxation & Wellness": [
            "The Well Spa",
            "SALT Sauna",
            "Elements Spa Aker Brygge",
            "Vulkana Floating Sauna",
            "Farris Bad (nearby)",
            "Huk Beach Chill",
            "St. Halvard Spa",
            "Hotel Continental Spa"
        ]
    },
    "Athens": {
        "Culture & Historical Exploration": [
            "Acropolis & Parthenon",
            "Acropolis Museum",
            "Ancient Agora",
            "Plaka District",
            "Temple of Olympian Zeus",
            "Panathenaic Stadium",
            "National Archaeological Museum",
            "Roman Agora"
        ],
        "Urban Entertainment & Nightlife": [
            "Psiri Bars",
            "Gazi District Clubs",
            "Kolonaki Lounges",
            "Brettos Bar",
            "Six d.o.g.s",
            "Balux Café",
            "Baba Au Rum",
            "Half Note Jazz Club"
        ],
        "Nature & Outdoor Adventure": [
            "Mount Lycabettus Hike",
            "Philopappos Hill",
            "Saronic Gulf Cruise",
            "National Garden Walk",
            "Filopappou Park",
            "Lake Vouliagmeni",
            "Attica Zoological Park",
            "Mount Parnitha Trails"
        ],
        "Relaxation & Wellness": [
            "Glyfada Beach",
            "Thermae at Cape Sounio",
            "Hammam Baths",
            "Astir Beach Club",
            "Divani Apollon Palace Spa",
            "Holistic Spa Athens",
            "Lycabettus Pool Lounge",
            "Evia Day Spa"
        ]
    },
    "Copenhagen": {
        "Culture & Historical Exploration": [
            "Tivoli Gardens",
            "Nyhavn",
            "Rosenborg Castle",
            "Amalienborg Palace",
            "Christiansborg Palace",
            "National Museum",
            "SMK Art Museum",
            "Little Mermaid"
        ],
        "Urban Entertainment & Nightlife": [
            "Meatpacking District",
            "Rust",
            "Culture Box",
            "Ruby Cocktail Bar",
            "Bakken at KB18",
            "Ved Siden Af",
            "The Jane",
            "Jolene Bar"
        ],
        "Nature & Outdoor Adventure": [
            "Canal Kayak Tour",
            "Amager Beach Park",
            "Dyrehaven Deer Park",
            "Frederiksberg Gardens",
            "Superkilen Park",
            "Utterslev Mose",
            "Christianshavn Cycling",
            "Freetown Christiania Walk"
        ],
        "Relaxation & Wellness": [
            "Kurhotel Skodsborg Spa",
            "AIRE Ancient Baths",
            "SP34 Wellness",
            "Manon Les Suites Pool",
            "WELL Being Spa",
            "Brøndums Hotel Spa",
            "Copenhagen Marriott Spa",
            "Hotel d’Angleterre Spa"
        ]
    },
    "Zürich": {
        "Culture & Historical Exploration": [
            "Kunsthaus Zürich",
            "Swiss National Museum",
            "Grossmünster",
            "Fraumünster",
            "Rietberg Museum",
            "Lindenhof",
            "Opera House Tour",
            "Cabaret Voltaire"
        ],
        "Urban Entertainment & Nightlife": [
            "Langstrasse Bars",
            "Widder Bar",
            "Hive Club",
            "Mascotte Jazz Club",
            "Exil",
            "Frau Gerolds Garten",
            "Kaufleuten",
            "Plaza Club"
        ],
        "Nature & Outdoor Adventure": [
            "Lake Zurich Boat",
            "Uetliberg Hike",
            "Zurich Zoo",
            "Botanical Garden",
            "Greifensee Bike",
            "Pfäffikersee",
            "Sihlwald Forest",
            "Greifensee Birdwatching"
        ],
        "Relaxation & Wellness": [
            "Thermalbad & Spa",
            "Poolamare Spa",
            "Seerose Resort Spa",
            "La Sana Spa",
            "Mandarin Oriental Spa",
            "Park Hyatt Spa",
            "Spa at Chedi Andermatt",
            "Dolder Grand Spa"
        ]
    },
    "Antwerp": {
        "Culture & Historical Exploration": [
            "MAS Museum",
            "Cathedral of Our Lady",
            "Rubens House",
            "Plantin-Moretus Museum",
            "Grote Markt",
            "Red Star Line Museum",
            "City Hall Tour",
            "Museum aan de Stroom"
        ],
        "Urban Entertainment & Nightlife": [
            "Zuid District Bars",
            "Café d’Anvers",
            "Propaganda",
            "Ampere",
            "Het Eilandje",
            "Trix Club",
            "Café De Muze",
            "Madiz"
        ],
        "Nature & Outdoor Adventure": [
            "Scheldt River Cruise",
            "Park Spoor Noord",
            "Rivierenhof Park",
            "Antwerp Zoo",
            "Middelheim Park Sculpture",
            "Kalmthoutse Heide",
            "Stadspark",
            "Eikenstraat Cycling"
        ],
        "Relaxation & Wellness": [
            "Aquafun Park",
            "Historic Spa Days Antwerp",
            "Thermae Palace Spa",
            "Wellness at Hilton",
            "Park Inn Spa",
            "Ostinato Spa",
            "CitySpa 51°",
            "Spa at Hotel Julien"
        ]
    },
    "Kraków": {
        "Culture & Historical Exploration": [
            "Wawel Castle",
            "Main Market Square",
            "St. Mary’s Basilica",
            "Kazimierz District",
            "Schindler’s Factory",
            "National Museum",
            "Wieliczka Salt Mine",
            "Planty Park Walk"
        ],
        "Urban Entertainment & Nightlife": [
            "Szewska Street Bars",
            "Alchemia",
            "Prozak 2.0",
            "Forum Przestrzenie",
            "Frantic Club",
            "House of Beer",
            "Tap Bar",
            "Klub Pauza"
        ],
        "Nature & Outdoor Adventure": [
            "Vistula Boulevards",
            "Zakrzówek Quarry Swim",
            "Tyniec Abbey Trail",
            "Jordan Park",
            "Krakus Mound",
            "Ojców National Park",
            "Zakopane Day Trip",
            "Błonia Meadow"
        ],
        "Relaxation & Wellness": [
            "Spa at Hotel Stary",
            "Q Hotel Spa",
            "Thermal Pools Bukovina",
            "Aqua Park Zakopane",
            "Mobile Sauna by Vistula",
            "Karb Spa",
            "Radisson Blu Spa",
            "Sheraton Spa"
        ]
    },
    "Minsk": {
        "Culture & Historical Exploration": [
            "National Opera & Ballet",
            "Victory Square",
            "Great Patriotic War Museum",
            "Island of Tears",
            "Holy Spirit Cathedral",
            "Stalin Line",
            "Belarusian State Museum",
            "Yakub Kolas Museum"
        ],
        "Urban Entertainment & Nightlife": [
            "Partisan Club",
            "Dozari",
            "BOPEN",
            "Black Hall",
            "Club 13",
            "Picasso Lounge",
            "Madiz",
            "Zoo Bar"
        ],
        "Nature & Outdoor Adventure": [
            "Yanka Kupala Park",
            "Chelyuskinites Park",
            "Lositsky Park",
            "Svislach River Cruise",
            "Trinity Hill",
            "Dog Lake",
            "Ascension Sunday Hill",
            "Zaslavsky Lake"
        ],
        "Relaxation & Wellness": [
            "Wellness Anna",
            "Paradise Spa",
            "Amber Spa",
            "Lotus Spa",
            "Aquacentrum Water Park",
            "Imperial Spa",
            "Alexander Spa",
            "Lido Wellness"
        ]
    },
    "Tallinn": {
        "Culture & Historical Exploration": [
            "Toompea Castle",
            "Alexander Nevsky Cathedral",
            "Town Hall Square",
            "Kadriorg Palace",
            "Kumu Art Museum",
            "Seaplane Harbour",
            "St. Olaf’s Church",
            "St. Catherine’s Passage"
        ],
        "Urban Entertainment & Nightlife": [
            "Telliskivi Creative City",
            "Club Hollywood",
            "Von Krahl",
            "Red Emperor",
            "Porgu",
            "Vana Villem",
            "Hell Hunt",
            "Liblikas Bar"
        ],
        "Nature & Outdoor Adventure": [
            "Pirita Beach",
            "Nõmme Forest Trails",
            "Tallinn TV Tower Park",
            "Tuhkana Bog",
            "Kadriorg Park",
            "Lennusadam Kayak",
            "Kloogaranna Beach",
            "Maarjamäe Coastal Trail"
        ],
        "Relaxation & Wellness": [
            "Kalev Spa Waterpark",
            "Eforea Spa & Wellness",
            "Meresuu Spa",
            "Therma Center Tallinn",
            "Viimsi SPA",
            "Aura Spa Tartu",
            "Nehatu Spa",
            "V Spa"
        ]
    },
    "Helsinki": {
        "Culture & Historical Exploration": [
            "Helsinki Cathedral",
            "Ateneum Art Museum",
            "Suomenlinna Fortress",
            "Temppeliaukio Church",
            "National Museum of Finland",
            "Design Museum",
            "Kiasma",
            "Market Square"
        ],
        "Urban Entertainment & Nightlife": [
            "Kallio District",
            "Icebar",
            "Ääniwalli",
            "Tavastia Club",
            "Kaiku",
            "Kuudes Linja",
            "Baarikärpänen",
            "Siltanen"
        ],
        "Nature & Outdoor Adventure": [
            "Archipelago Ferry Tour",
            "Nuuksio National Park",
            "Seurasaari Walk",
            "Hietaniemi Beach",
            "Sipoonkorpi Park",
            "Teurastamo Urban Farm",
            "Esplanade Park",
            "Linnanmäki Gardens"
        ],
        "Relaxation & Wellness": [
            "Allas Sea Pool & Sauna",
            "Löyly Sauna",
            "Holiday Inn Spa",
            "Clarion Spa",
            "Hotel Kämp Spa",
            "Serenity Wellness",
            "Kylpylä Spa Hotel",
            "St. George’s Spa"
        ]
    },
    "Chisinau": {
        "Culture & Historical Exploration": [
            "Stefan Cel Mare Park",
            "National Museum of History",
            "Cathedral of Christ’s Nativity",
            "Pushkin Museum",
            "Mileștii Mici Winery",
            "Sculpture Alley",
            "Triumphal Arch",
            "Valea Morilor Park"
        ],
        "Urban Entertainment & Nightlife": [
            "Pushkin Bar",
            "OK Club",
            "Doina Club",
            "Spot Lounge",
            "Vis-a-Vis",
            "Cotton Pub",
            "Club Vegas",
            "Odeon Cafe"
        ],
        "Nature & Outdoor Adventure": [
            "Codru Forest Trails",
            "Duruitoarea Veche Cave",
            "Padurea Domneasca",
            "Cricova Wine Tunnels",
            "Brânza Lake",
            "Chisinau Botanical Garden",
            "Dendrarium Park",
            "Ghidighici Reservoir"
        ],
        "Relaxation & Wellness": [
            "Aqua Park Chisinau",
            "SPA Nufărul Alb",
            "Aquaterra Spa",
            "Villa Romania Spa",
            "President Hotel Spa",
            "Dendrarium Wellness",
            "Classic Spa Center",
            "Sofia Spa"
        ]
    },
    "Belfast": {
        "Culture & Historical Exploration": [
            "Titanic Belfast",
            "Ulster Museum",
            "City Hall Tour",
            "St. George’s Market",
            "Crumlin Road Gaol",
            "Peace Wall",
            "Murals Black Taxi Tour",
            "Grand Opera House"
        ],
        "Urban Entertainment & Nightlife": [
            "Cathedral Quarter",
            "Dirty Onion",
            "Filthy McNasty’s",
            "The Spaniard",
            "Emerald Bar",
            "Lavery’s",
            "BrewBot",
            "Thompson’s Garage"
        ],
        "Nature & Outdoor Adventure": [
            "Giant’s Causeway Trip",
            "Cave Hill Hike",
            "Botanic Gardens",
            "Lagan Towpath",
            "Rathlin Island Ferry",
            "Murlough Bay Walk",
            "Belfast Hills Trail",
            "Tollymore Forest Park"
        ],
        "Relaxation & Wellness": [
            "Culloden Estate Spa",
            "La Mon Hotel Spa",
            "Europa Hotel Spa",
            "Slieve Donard Spa",
            "Thompson Spa",
            "Grand Central Spa",
            "The MAC Chill Zone",
            "Absolute Spa Belfast"
        ]
    },
    "Vilnius": {
        "Culture & Historical Exploration": [
            "Gediminas’ Tower",
            "Vilnius Cathedral",
            "St. Anne’s Church",
            "Gedimino Prospektas",
            "Uzupis Art Incubator",
            "Church of St. Peter and St. Paul",
            "Museum of Occupations",
            "Užupis Constitution Wall"
        ],
        "Urban Entertainment & Nightlife": [
            "Paupio Klubas",
            "Peronas",
            "Bremena Bar",
            "Opium Club",
            "Loftas",
            "Salionas",
            "Piano Man Bar",
            "Birdman Nights"
        ],
        "Nature & Outdoor Adventure": [
            "Verkiai Regional Park",
            "Trakai Castle Day Trip",
            "Vingis Park Trails",
            "Neris River Canoeing",
            "Belmonto Leisure Park",
            "Karoliniškės Forest",
            "Sun & Moon Trail",
            "Green Lakes Cycling"
        ],
        "Relaxation & Wellness": [
            "SPA VILNIUS City",
            "Belvilis Wellness Resort",
            "Druskininkai Day Spa",
            "Grand Spa Lietuva",
            "Amberton Spa",
            "Erdvės SPA",
            "Vilnius Grand Resort Spa",
            "Thermana Park"
        ]
    },
    "Riga": {
        "Culture & Historical Exploration": [
            "House of the Blackheads",
            "Riga Cathedral",
            "Art Nouveau District",
            "National Opera",
            "Three Brothers",
            "Museum of the Occupation",
            "St. Peter’s Church Tower",
            "Latvian Ethnographic Open-Air"
        ],
        "Urban Entertainment & Nightlife": [
            "Skyline Bar",
            "La Rocca",
            "Dirty Deal Teatro",
            "One One",
            "Piens",
            "First Dacha",
            "Folkklubs Ala Pagrabs",
            "Coyote Fly"
        ],
        "Nature & Outdoor Adventure": [
            "Mežaparks",
            "Bolderāja Beach",
            "Daugava River Cruise",
            "Latgale Embankment",
            "Skanstes Lake",
            "Kengarags Forest",
            "Ķemeri National Park",
            "Ķīšezers Windsurfing"
        ],
        "Relaxation & Wellness": [
            "ESPA Riga",
            "Wellton Riverside SPA",
            "SPA Illa",
            "Azur SPA",
            "Radisson Blu Daina Spa",
            "Vita Nova",
            "Thermana Laško",
            "Jurmala Beach Spa"
        ]
    },
    "Zagreb": {
        "Culture & Historical Exploration": [
            "Upper Town & St. Mark’s",
            "Zagreb Cathedral",
            "Museum of Broken Relationships",
            "Archaeological Museum",
            "Lotrščak Tower",
            "Croatian National Theatre",
            "Art Pavilion",
            "Stone Gate"
        ],
        "Urban Entertainment & Nightlife": [
            "Tkalčićeva Street",
            "Katran",
            "Opera Club",
            "Pivana",
            "Dežman Bar",
            "The Garden Brewery",
            "Vintage Industrial",
            "Johann Franck"
        ],
        "Nature & Outdoor Adventure": [
            "Maksimir Park",
            "Jarun Lake",
            "Mount Medvednica",
            "Bundek Park",
            "Sava River Kayaking",
            "Botanical Garden",
            "Zrinjevac Park",
            "Sljeme Hiking"
        ],
        "Relaxation & Wellness": [
            "Thermana Laško Day Spa",
            "Jupiter Wellness&Fitness",
            "Esplanade Wellness",
            "Holistic Concept",
            "Zagreb Spa Studio",
            "Lifeclass Portorož (day trip)",
            "Spa at Sheraton",
            "Wellness Point"
        ]
    },
    "Sarajevo": {
        "Culture & Historical Exploration": [
            "Baščaršija Old Bazaar",
            "Latin Bridge",
            "Gazi Husrev-beg Mosque",
            "War Tunnel Museum",
            "Sarajevo Cathedral",
            "Yellow Fortress",
            "Museum of Crimes",
            "National Theatre"
        ],
        "Urban Entertainment & Nightlife": [
            "City Pub",
            "Sloga Club",
            "Cinemas Sloga",
            "Coloseum Club",
            "Oscar Cafe",
            "Top Bar",
            "Jazzbina",
            "Kriterion"
        ],
        "Nature & Outdoor Adventure": [
            "Trebević Cable Car",
            "Vrelo Bosne spring",
            "Skakavac Waterfall",
            "Bijambare Caves",
            "Bjelasnica Ski",
            "Igman Hiking",
            "Hajd Park",
            "Miljacka Riverwalk"
        ],
        "Relaxation & Wellness": [
            "Terme Ilidža",
            "Sarajevo Spa Centar",
            "Zira Spa",
            "Wellness S-Quare",
            "Hotel Hills Spa",
            "Ballkan Spa",
            "Aqua Park Ilidža",
            "Malak Spa"
        ]
    },
    "Skopje": {
        "Culture & Historical Exploration": [
            "Old Bazaar",
            "Skopje Fortress",
            "Stone Bridge",
            "Macedonia Square",
            "Archaeological Museum",
            "Memorial House of Mother Teresa",
            "City Museum",
            "Matka Canyon"
        ],
        "Urban Entertainment & Nightlife": [
            "Epicentar",
            "Club Epic",
            "Booze Bar",
            "Shame",
            "Destiny Club",
            "Opium Club",
            "Atmosfera",
            "Cuba Libre"
        ],
        "Nature & Outdoor Adventure": [
            "Matka Lake Canoe",
            "Mount Vodno",
            "Millennium Cross Hike",
            "Skopje City Park",
            "Kozjak Reservoir",
            "Tikvesh Wine Trail",
            "Macedonian Philharmonic Park",
            "Barricades Trail"
        ],
        "Relaxation & Wellness": [
            "Wellness Villa Vodno",
            "Spa FlySpa",
            "Regnum Hotel Spa",
            "Alexandar Palace Spa",
            "Hotel Kovachevich Spa",
            "Sauna Skopje",
            "Thermae Syhne Spa",
            "City Wellness"
        ]
    },
    "Tbilisi": {
        "Culture & Historical Exploration": [
            "Narikala Fortress",
            "Old Town (Kala)",
            "Bridge of Peace",
            "Metekhi Church",
            "Sioni Cathedral",
            "Georgian National Museum",
            "Rustaveli Avenue",
            "Fabrika Art Space"
        ],
        "Urban Entertainment & Nightlife": [
            "Bassiani",
            "Khidi",
            "Mziani",
            "Lab Club",
            "Funicular Bar",
            "Drama Bar",
            "Ezo",
            "Ceremony"
        ],
        "Nature & Outdoor Adventure": [
            "Mtatsminda Park",
            "Turtle Lake",
            "Kartlis Deda Hike",
            "Mtskheta Day Trip",
            "Lisi Lake",
            "Abanotubani Sulfur Baths",
            "Tbilisi National Park",
            "Gori Day Tour"
        ],
        "Relaxation & Wellness": [
            "Sulfur Bathhouses",
            "Orbeliani Baths",
            "Tbilisi Marriott Spa",
            "Rooms Hotel Spa",
            "Vera Spa",
            "Merab Kostava Wellness",
            "Euphoria Bath",
            "Eden Spa"
        ]
    },
    "Baku": {
        "Culture & Historical Exploration": [
            "Icherisheher (Old City)",
            "Maiden Tower",
            "Palace of the Shirvanshahs",
            "Heydar Aliyev Center",
            "Azerbaijan State Museum of History",
            "Azerbaijan Carpet Museum",
            "Yarat Contemporary Art Space",
            "Museum of Modern Art Baku"
        ],
        "Urban Entertainment & Nightlife": [
            "Otto Club",
            "Capitol Night Club",
            "Status Club",
            "360 Sky Bar",
            "Finnegan’s Irish Pub",
            "People Live Bar",
            "Pasifico Baku",
            "Nizami Street Bars"
        ],
        "Nature & Outdoor Adventure": [
            "Baku Boulevard Promenade",
            "Gobustan Rock Art Cultural Landscape",
            "Mud Volcanoes Tour",
            "Yanar Dag (Burning Mountain)",
            "Absheron Peninsula Beaches",
            "Caspian Sea Boat Cruise",
            "Highland Park Trails",
            "Flame Towers Viewing Platform"
        ],
        "Relaxation & Wellness": [
            "Four Seasons Hotel Spa",
            "JW Marriott Absheron Spa",
            "Fairmont Baku Flame Towers Spa",
            "Bilgah Beach Spa & Resort",
            "Hilton Baku Spa",
            "Hyatt Regency Baku Spa",
            "Park Boulevard Spa",
            "SPA by Victoria"
        ]
    },
    "Dublin": {
        "Culture & Historical Exploration": [
            "Trinity & Book of Kells",
            "Guinness Storehouse",
            "Dublin Castle",
            "Kilmainham Gaol",
            "Temple Bar Cultural",
            "Chester Beatty",
            "EPIC Museum",
            "Christ Church Cathedral"
        ],
        "Urban Entertainment & Nightlife": [
            "Temple Bar Pubs",
            "The Bernard Shaw",
            "Whelan’s",
            "Dicey’s Garden",
            "The Stag’s Head",
            "The Porterhouse",
            "Copper Face Jacks",
            "Opium Rooms"
        ],
        "Nature & Outdoor Adventure": [
            "Phoenix Park Cycling",
            "Howth Cliff Walk",
            "Killiney Hill",
            "Bray Day Trip",
            "Dublin Bay Cruise",
            "Wicklow Mountains",
            "Irelands Eye Ferry",
            "Avonmore Nature Walk"
        ],
        "Relaxation & Wellness": [
            "The Marker Spa",
            "The Spa at Powerscourt",
            "Cliff at Lyons",
            "Great Northern Spa",
            "Kerry Spa",
            "Serenity Day Spa",
            "Element Belle Spa",
            "Glenlo Abbey Spa"
        ]
    },
    "Bristol": {
        "Culture & Historical Exploration": [
            "SS Great Britain",
            "Clifton Suspension Bridge",
            "Bristol Cathedral",
            "M Shed",
            "Stokes Croft Street Art",
            "Cabot Tower",
            "Blaise Castle",
            "Red Lodge Museum"
        ],
        "Urban Entertainment & Nightlife": [
            "Thekla",
            "Motion",
            "Lakota",
            "Rex Club",
            "Small Bar",
            "Exchange",
            "Mother’s Ruin",
            "Bar 44"
        ],
        "Nature & Outdoor Adventure": [
            "Avon Gorge Walk",
            "Leigh Woods",
            "Ashton Court",
            "Bristol Zoo Gardens",
            "Blaise Castle Estate",
            "Bristol Harbourside",
            "Severn Beach",
            "Cheddar Gorge Day Trip"
        ],
        "Relaxation & Wellness": [
            "Lido Spa",
            "Pure Spa & Beauty",
            "Bristol Marriott Spa",
            "The Berkeley Square",
            "Clayton Spa",
            "24/7 Health Club",
            "Escape Spa",
            "YTL Spa"
        ]
    },
    "Cardiff": {
        "Culture & Historical Exploration": [
            "Cardiff Castle",
            "National Museum Cardiff",
            "Llandaff Cathedral",
            "St Fagans Open-Air",
            "Norwegian Church",
            "Bute Park",
            "Doctor Who Experience",
            "Principality Stadium Tour"
        ],
        "Urban Entertainment & Nightlife": [
            "Womanby Street",
            "The Dead Canary",
            "Lab 22",
            "Revolution",
            "Retro",
            "Y Mochyn Du",
            "Tiny Rebel",
            "Clwb Ifor Bach"
        ],
        "Nature & Outdoor Adventure": [
            "Cardiff Bay Barrage",
            "Roath Park Lake",
            "Coed-y-Mwstwr",
            "Garth Mountain",
            "Llandaff Fields",
            "Penarth Pier",
            "Ogmore Beach",
            "Dan-yr-Ogof Caves"
        ],
        "Relaxation & Wellness": [
            "Park Plaza Spa",
            "Vale Resort Spa",
            "Norton House Spa",
            "Metropole Spa",
            "Aura Spa",
            "Ragdale Hall (day trip)",
            "Village Urban Resorts",
            "The Spa at Celtic Manor"
        ]
    },
    "Manchester": {
        "Culture & Historical Exploration": [
            "John Rylands Library",
            "Manchester Museum",
            "Science and Industry",
            "People’s History Museum",
            "Chetham’s Library",
            "Castlefield",
            "Albert Hall",
            "Whitworth Gallery"
        ],
        "Urban Entertainment & Nightlife": [
            "Deansgate Locks",
            "Warehouse Project",
            "Albert Schloss",
            "The Printworks",
            "Hidden",
            "Gorilla",
            "The Liars Club",
            "Yes"
        ],
        "Nature & Outdoor Adventure": [
            "Peak District Day Trip",
            "Heaton Park",
            "Ethical Adventures Trail",
            "Cheshire Forest",
            "Salford Quays Cycling",
            "Bridgewater Canal Walk",
            "Rivington Pike",
            "Dane Valley Hike"
        ],
        "Relaxation & Wellness": [
            "The Spa at Midland",
            "Corinthian Spa",
            "Edwardian Spa",
            "Banya No.1",
            "Urban Retreat",
            "Live Well Spa",
            "Serenity Salon",
            "Spa Experience"
        ]
    },
    "Leeds": {
        "Culture & Historical Exploration": [
            "Royal Armouries Museum",
            "Kirkstall Abbey",
            "Leeds City Museum",
            "Thackray Medical Museum",
            "Cartwright Hall Art Gallery",
            "Temple Newsam House",
            "Thoresby Gallery",
            "Abbey House Museum"
        ],
        "Urban Entertainment & Nightlife": [
            "Call Lane Bars",
            "Belgrave Music Hall",
            "Brudenell Social Club",
            "Merrion Centre Rooftop",
            "Leeds Dock Clubs",
            "Headrow House",
            "The Wardrobe",
            "Digital"
        ],
        "Nature & Outdoor Adventure": [
            "Roundhay Park",
            "Golden Acre Park",
            "Otley Chevin Forest Park",
            "Leeds–Liverpool Canal Walk",
            "Temple Newsam Parklands",
            "Meanwood Valley Trail",
            "Harewood House Grounds",
            "Yeadon Tarn Sailing"
        ],
        "Relaxation & Wellness": [
            "Thorpe Park Spa",
            "Village Spa Leeds",
            "Oulton Hall Spa",
            "Kirkstall Brewery Spa",
            "QHotels Spa",
            "Escape Spa Leeds",
            "Clayton Spa & Leisure",
            "Live Well Club"
        ]
    },
    "Liverpool": {
        "Culture & Historical Exploration": [
            "The Beatles Story",
            "Liverpool Cathedral",
            "Tate Liverpool",
            "Walker Art Gallery",
            "Maritime Museum",
            "Williamson Tunnels",
            "St George’s Hall",
            "World Museum"
        ],
        "Urban Entertainment & Nightlife": [
            "Mathew Street Bars",
            "Concert Square",
            "Baltic Triangle",
            "Camp and Furnace",
            "Heebie Jeebies",
            "Alchemist",
            "Ruby Lounge",
            "McCoy’s"
        ],
        "Nature & Outdoor Adventure": [
            "Sefton Park Palm House",
            "Albert Dock Waterfront Walk",
            "Wirral Coastal Path",
            "Otterspool Promenade",
            "Formby Sand Dunes",
            "Crosby Beach Sculpture Trail",
            "Speke Hall Gardens",
            "Mersey Ferry Cruise"
        ],
        "Relaxation & Wellness": [
            "Titanic Hotel Spa",
            "Eforea Spa at Hilton",
            "The Spa at Eco Hotel",
            "Bloom Spa Liverpool",
            "Pure Spa Victoria Square",
            "Spa at Hope Street Hotel",
            "Livewell Spa",
            "Expression Hair & Beauty"
        ]
    },
    "Newcastle upon Tyne": {
        "Culture & Historical Exploration": [
            "BALTIC Centre for Contemporary Art",
            "Newcastle Castle",
            "Discovery Museum",
            "Grey Street Theatre",
            "St Nicholas’ Cathedral",
            "Laing Art Gallery",
            "Life Science Centre",
            "Stephenson Railway Museum"
        ],
        "Urban Entertainment & Nightlife": [
            "Bigg Market",
            "The Ouseburn Valley",
            "PRYZM Newcastle",
            "Digital Newcastle",
            "The Cluny",
            "Alvinos Wine Bar",
            "Jordan’s Cocktail Bar",
            "Popworld"
        ],
        "Nature & Outdoor Adventure": [
            "Quayside Riverside Walk",
            "Jesmond Dene Park",
            "Hadrian’s Wall Day Trip",
            "Tynemouth Longsands Beach",
            "Downhill Ski Centre",
            "Tyne Green Cycling",
            "Walney Island Birdwatching",
            "Derwent Reservoir"
        ],
        "Relaxation & Wellness": [
            "Barras Bridge Spa",
            "Jesmond Dene House Spa",
            "Malmaison Spa",
            "Dakota Spa Newcastle",
            "LiveWell Newcastle",
            "Holistic Kind Spa",
            "The Spa at Ramside",
            "Reform North Spa"
        ]
    },
    "Sheffield": {
        "Culture & Historical Exploration": [
            "Millennium Gallery",
            "Kelham Island Museum",
            "Sheffield Cathedral",
            "Abbeydale Industrial Hamlet",
            "Graves Gallery",
            "Weston Park Museum",
            "Sheffield Manor Lodge",
            "Trafford Centre Art Space"
        ],
        "Urban Entertainment & Nightlife": [
            "Ecclesall Road Pubs",
            "The Leadmill",
            "Tamper Sellers Wheel",
            "Redux",
            "Yellow Arch Studios",
            "MCG Leeds",
            "The Harley",
            "District"
        ],
        "Nature & Outdoor Adventure": [
            "Peak District Day Hike",
            "Rivelin Valley Trail",
            "Ladybower Reservoir",
            "Chatsworth House Grounds",
            "Sheffield Botanical Gardens",
            "Fox Valley Park",
            "Nab Wood Circular Walk",
            "Rother Valley Country Park"
        ],
        "Relaxation & Wellness": [
            "Mercure Spa",
            "Spa 1877",
            "Sheffield’s Live Well Club",
            "Bannatyne Spa",
            "Robertson’s Health",
            "Spa at Leopold Hotel",
            "Holistic Heaven",
            "The Rutland Hotel Spa"
        ]
    },
    "Nottingham": {
        "Culture & Historical Exploration": [
            "Nottingham Castle",
            "Great Central Railway",
            "Southwell Minster",
            "Museum of Nottingham Life",
            "City of Caves",
            "Wollaton Hall",
            "Green’s Windmill",
            "Newstead Abbey"
        ],
        "Urban Entertainment & Nightlife": [
            "Hockley Arts Club",
            "Mint Club",
            "Bunkers Hill",
            "Stealth Bar",
            "The Bodega",
            "Junkyard Golf Club",
            "Pearl Club",
            "Penny Lane"
        ],
        "Nature & Outdoor Adventure": [
            "Sherwood Forest",
            "Bestwood Country Park",
            "Attenborough Nature Reserve",
            "River Trent Cruise",
            "Colwick Country Park",
            "Cannock Chase Day Trip",
            "Victoria Leisure Centre",
            "Matlock Bath"
        ],
        "Relaxation & Wellness": [
            "Urban Escape Spa",
            "Owl House Day Spa",
            "Cleopatras Spa",
            "Bannatyne Spa Nottingham",
            "Village Spa",
            "Livewell Leisure",
            "Holistic Harmony",
            "Omni Health"
        ]
    },
    "Leicester": {
        "Culture & Historical Exploration": [
            "King Richard III Visitor Centre",
            "New Walk Museum & Art Gallery",
            "Leicester Cathedral",
            "National Space Centre",
            "Jewry Wall Museum",
            "Abbey Pumping Station",
            "Hinckley Museum",
            "Belgrave Hall"
        ],
        "Urban Entertainment & Nightlife": [
            "Granby Street",
            "Madame Jojo’s",
            "The Shed",
            "The Cookie",
            "Atom",
            "Brendan’s Whiskey Bar",
            "Firebug",
            "Zoo"
        ],
        "Nature & Outdoor Adventure": [
            "Bradgate Park",
            "Watermead Country Park",
            "Bosworth Battlefield",
            "Beacon Hill Country Park",
            "River Soar Walk",
            "Humberstone Heights",
            "Charnwood Forest",
            "West Bridge Leisure Centre"
        ],
        "Relaxation & Wellness": [
            "Oasis Health Club",
            "City Escape Spa",
            "Bannatyne Spa Leicester",
            "Spa at Knighton Fields",
            "Village Spa",
            "Holistic Henri",
            "The Retreat Spa",
            "Livewell"
        ]
    },
    "Bradford": {
        "Culture & Historical Exploration": [
            "National Science and Media Museum",
            "Cartwright Hall",
            "Bradford Cathedral",
            "Saltaire World Heritage Site",
            "Salts Mill Gallery",
            "Cliffe Castle Museum",
            "Bradford Industrial Museum",
            "Royal Armouries Leeds"
        ],
        "Urban Entertainment & Nightlife": [
            "Sunbridge Wells",
            "The Alhambra Theatre",
            "Revolution",
            "Popworld Bradford",
            "O2 Academy",
            "The Underground",
            "Madagascar Bar",
            "Lilac Lounge"
        ],
        "Nature & Outdoor Adventure": [
            "Leeds Liverpool Canal",
            "Limestone Trail",
            "Ilkley Moor",
            "Ilkley Cliff Top Walk",
            "Malham Cove Day Trip",
            "Bronte Country",
            "Roundhay Park",
            "Bingley Five Rise"
        ],
        "Relaxation & Wellness": [
            "Velocity Health & Fitness",
            "The Hidden Sanctuary Spa",
            "Village Spa Bradford",
            "Bannatyne Spa",
            "Serenity Spa",
            "Urban Retreat",
            "Livewell",
            "Holistic Haven"
        ]
    },
    "Coventry": {
        "Culture & Historical Exploration": [
            "Coventry Cathedral",
            "Transport Museum",
            "Herbert Art Gallery",
            "St Mary’s Guildhall",
            "War Memorial Park",
            "Priory Visitor Centre",
            "Lady Godiva Statue",
            "Coventry Archives"
        ],
        "Urban Entertainment & Nightlife": [
            "FarGo Village",
            "The Tin Music and Arts",
            "Fargo Pantry Bar",
            "Bodega Social",
            "Popworld",
            "The Yard",
            "Hooters",
            "Opera House Bar"
        ],
        "Nature & Outdoor Adventure": [
            "Coventry Canal Walk",
            "Rhinefield Ornamental Drive",
            "Ryton Pools Country Park",
            "Coombe Abbey Park",
            "Burbage Common",
            "Meriden",
            "Kennetts Pool",
            "Kenilworth Castle Grounds"
        ],
        "Relaxation & Wellness": [
            "Mana Spa",
            "The Bannatyne Spa",
            "Village Spa Coventry",
            "Serenity Salon",
            "Holistic Coventry",
            "Livewell Club",
            "Clayton Spa",
            "Urban Spa"
        ]
    },
    "Birmingham": {
        "Culture & Historical Exploration": [
            "Birmingham Museum & Art Gallery",
            "Library of Birmingham",
            "Cadbury World",
            "Thinktank Science Museum",
            "Black Country Living Museum",
            "Soho House",
            "Aston Hall",
            "Barber Institute"
        ],
        "Urban Entertainment & Nightlife": [
            "Broad Street Bars",
            "Digbeth Dining Club",
            "Rainbow Venues",
            "The Night Owl",
            "LAB11",
            "The Jam House",
            "Cosmo",
            "Popworld"
        ],
        "Nature & Outdoor Adventure": [
            "Cannon Hill Park",
            "Birmingham Botanical Gardens",
            "Sutton Park",
            "Elan Valley (day trip)",
            "Lickey Hills",
            "Edgbaston Reservoir",
            "River Rea Walk",
            "Sarehole Mill"
        ],
        "Relaxation & Wellness": [
            "The Belfry Spa",
            "Santai Spa",
            "Bannatyne Spa",
            "Village Spa",
            "Urban Retreat Spa",
            "Serenity Salon",
            "Holistic Haven",
            "Livewell"
        ]
    },
    "Glasgow": {
        "Culture & Historical Exploration": [
            "Kelvingrove Art Gallery",
            "Glasgow Cathedral",
            "Riverside Museum",
            "Hunterian Museum",
            "The Tenement House",
            "People’s Palace",
            "Gallery of Modern Art",
            "St Mungo Museum"
        ],
        "Urban Entertainment & Nightlife": [
            "Sauchiehall Street Clubs",
            "The Garage",
            "SWG3",
            "Sub Club",
            "Brel",
            "Nice N Sleazy",
            "Barras Art and Design",
            "King Tut’s Wah Wah Hut"
        ],
        "Nature & Outdoor Adventure": [
            "Glasgow Green Walk",
            "Loch Lomond Day Trip",
            "Botanic Gardens",
            "Pollok Country Park",
            "Kelvingrove Park",
            "Clyde Walkway",
            "Cochno Stone Trail",
            "Mugdock Country Park"
        ],
        "Relaxation & Wellness": [
            "Blythswood Square Spa",
            "Pure Spa & Beauty",
            "The Watt Spa",
            "Spa at Kimpton Blythswood",
            "Urban Retreat",
            "Serenity Salon",
            "Holistic Glasgow",
            "Livewell Club"
        ]
    },
    "Edinburgh": {
        "Culture & Historical Exploration": [
            "Edinburgh Castle",
            "National Museum of Scotland",
            "Holyrood Palace",
            "Scottish Parliament",
            "Real Mary King’s Close",
            "Surgeons’ Hall Museums",
            "The Royal Yacht Britannia",
            "National Galleries of Scotland"
        ],
        "Urban Entertainment & Nightlife": [
            "Grassmarket pubs",
            "Cowgate clubs",
            "The Bongo Club",
            "Sneaky Pete’s",
            "The Voodoo Rooms",
            "Whistle Binkies",
            "Bannerman’s Bar",
            "Stramash"
        ],
        "Nature & Outdoor Adventure": [
            "Arthur’s Seat hike",
            "Calton Hill walk",
            "Royal Botanic Garden",
            "Portobello Beach",
            "Water of Leith Walkway",
            "Holyrood Park cycling",
            "Pentland Hills trip",
            "Leith Shore waterfront"
        ],
        "Relaxation & Wellness": [
            "One Spa at Sheraton",
            "The Balmoral Spa",
            "The Spa at Prestonfield",
            "Pure Spa & Beauty",
            "Holistic Heaven",
            "LiveWell Edinburgh",
            "Nirvana Spa",
            "Urban Retreat Spa"
        ]
    },
    "Ljubljana": {
        "Culture & Historical Exploration": [
            "Ljubljana Castle",
            "National Gallery",
            "Tivoli Mansion",
            "Museum of Modern Art",
            "City Museum of Ljubljana",
            "Franciscan Church",
            "Plečnik House",
            "Metelkova Art Centre"
        ],
        "Urban Entertainment & Nightlife": [
            "Metelkova bars",
            "Kino Šiška",
            "Cirkus Pub",
            "Daktari Cocktail Bar",
            "Open Kitchen Street Food",
            "Centralna Postaja",
            "Trinity Club",
            "Klub Tiffany"
        ],
        "Nature & Outdoor Adventure": [
            "Tivoli Park cycling",
            "Ljubljanica River cruise",
            "Rožnik Hill trail",
            "Šmarna Gora hike",
            "Koseze Pond walk",
            "Botanical Garden stroll",
            "Golovec Forest run",
            "Ljubljana Marsh excursion"
        ],
        "Relaxation & Wellness": [
            "Sense Wellness Club",
            "Zlati Klub Spa",
            "Tervis Spa",
            "Kalma Wellbeing",
            "City Spa Ljubljana",
            "Wellness Oaza",
            "Aqua Life Resort",
            "Holistic Harmony"
        ]
    },
    "Tirana": {
        "Culture & Historical Exploration": [
            "Et'hem Bey Mosque",
            "Skanderbeg Square",
            "National History Museum",
            "Bunk’Art 2",
            "Pyramid of Tirana",
            "Clock Tower",
            "House of Leaves",
            "National Art Gallery"
        ],
        "Urban Entertainment & Nightlife": [
            "Blloku district bars",
            "Sky Club rooftop",
            "Era Club",
            "Radio Bar",
            "Folie Terrace",
            "Monk Cocktail Bar",
            "Discoteca Lollipop",
            "Tango Club"
        ],
        "Nature & Outdoor Adventure": [
            "Mount Dajti cable car",
            "Grand Park of Tirana",
            "Kavajë Beach day trip",
            "Petrela Castle hike",
            "Rruga e Arbërit drive",
            "Dajti National Park trails",
            "Farka Lake walk",
            "Erzeni River kayaking"
        ],
        "Relaxation & Wellness": [
            "Glow Wellness & Spa",
            "Hilton Tirana Spa",
            "Plaza Spa",
            "Tirana Wellness Center",
            "Urban Spa Tirana",
            "Royal Spa",
            "Elena Spa",
            "Holistic Haven"
        ]
    }
}

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS city_activities")
cursor.execute("DROP TABLE IF EXISTS activities")
cursor.execute("DROP TABLE IF EXISTS cities")

cursor.execute('''
CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    latitude REAL,
    longitude REAL,
    country TEXT
)''')

cursor.execute('''
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)''')

cursor.execute('''
CREATE TABLE city_activities (
    city_id INTEGER,
    activity_id INTEGER,
    description TEXT,
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (activity_id) REFERENCES activities(id)
)''')
# this block inserts each activity name into the activites table and 
activity_ids = {}
for name in activity_names:
    cursor.execute("INSERT INTO activities (name) VALUES (?)", (name,))
    activity_ids[name] = cursor.lastrowid

# this part inserts details of cities and retrieves city details
for city, (lat, lon, country) in raw_city_data.items():
    cursor.execute("INSERT INTO cities (name, latitude, longitude, country) VALUES (?, ?, ?, ?)",
                   (city, lat, lon, country))
    cursor.execute("SELECT id FROM cities WHERE name = ?", (city,))
    city_id = cursor.fetchone()[0]
    for activity in activity_names:
        cursor.execute("SELECT id FROM activities WHERE name = ?", (activity,))
        activity_id = cursor.fetchone()[0]
        if city in custom_city_activities and activity in custom_city_activities[city]:
            for desc in custom_city_activities[city][activity]:
                cursor.execute('''
                    INSERT INTO city_activities (city_id, activity_id, description)
                    VALUES (?, ?, ?)
                ''', (city_id, activity_id, desc))
        else:
            cursor.execute('''
                INSERT INTO city_activities (city_id, activity_id, description)
                VALUES (?, ?, NULL)
            ''', (city_id, activity_id))
            
# this function saves the changes in the database and closes it 
conn.commit()
conn.close()
