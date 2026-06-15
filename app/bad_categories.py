"""
Content-moderation category keyword tables.

A generic, business-agnostic taxonomy for classifying images from their Google
Vision labels. Each category maps to a list of lowercase keywords; an image is
matched to a category when any label Vision detected (or the hasText / isHuman /
hasLogo markers) equals one of that category's keywords.

How to use it for YOUR business
-------------------------------
You don't moderate on every category — you pick the ones that matter for your
use case and treat them as a "verify list" (flag for review) or an "alert list"
(hard block). For example:

  - A photo gallery might verify PetsAndAnimals, VehiclesTransport, People.
  - A marketplace might verify Weapons, Counterfeit, Drugs.
  - A dating app might verify People and alert on ExplicitContent.
  - A kids' brand might alert on Alcohol, Tobacco, Gambling, Violence.

Categories are grouped below by theme. Keywords are realistic Google Vision
label outputs (lowercased). Add or remove freely — `get_categories()` simply
looks the name up in CATEGORIES.
"""

CATEGORIES = {
    # ----------------------------------------------------------------------
    # PEOPLE
    # ----------------------------------------------------------------------
    "HumanBody": [
        "face", "head", "arm", "leg", "hand", "finger", "foot", "knee",
        "shoulder", "neck", "back", "chest", "stomach", "skin", "hair",
        "mouth", "lip", "eye", "eyelash", "eyebrow", "nose", "ear", "cheek",
        "chin", "forehead", "jaw", "tooth", "tongue", "wrist", "elbow",
        "ankle", "thigh", "muscle", "beard", "moustache",
    ],
    "HumanPresence": [
        "person", "people", "human", "human body", "man", "woman", "male",
        "female", "child", "kid", "baby", "infant", "toddler", "girl", "boy",
        "teenager", "adult", "elder", "senior", "crowd", "group photo",
        "selfie", "portrait", "photograph", "smile", "facial expression",
        "gesture", "standing", "sitting", "walking", "audience", "family",
        "couple", "friendship",
    ],
    "ClothingAndSwimwear": [
        "clothing", "fashion", "outfit", "dress", "shirt", "t-shirt", "blouse",
        "jacket", "coat", "sweater", "hoodie", "jeans", "trousers", "pants",
        "shorts", "skirt", "miniskirt", "suit", "uniform", "costume", "hat",
        "cap", "shoe", "sneakers", "boots", "high heels", "sandals", "scarf",
        "glove", "sock", "stockings", "tie", "belt",
        # revealing / swimwear (often used as a "needs review" signal)
        "bikini", "swimsuit", "swimwear", "lingerie", "underwear", "bra",
        "panties", "thong", "topless", "shirtless", "barechested", "cleavage",
    ],

    # ----------------------------------------------------------------------
    # ANIMALS & NATURE
    # ----------------------------------------------------------------------
    "PetsAndAnimals": [
        "animal", "pet", "dog", "puppy", "cat", "kitten", "horse", "pony",
        "rabbit", "hamster", "guinea pig", "ferret", "bird", "parrot", "canary",
        "fish", "goldfish", "aquarium", "turtle", "reptile", "snake", "lizard",
        "frog", "rodent", "mammal", "carnivore", "whiskers", "fur", "paw",
        "tail", "snout", "zoo",
    ],
    "Wildlife": [
        "wildlife", "wild animal", "lion", "tiger", "leopard", "cheetah",
        "bear", "wolf", "fox", "deer", "elephant", "giraffe", "zebra",
        "rhinoceros", "hippopotamus", "monkey", "ape", "gorilla", "kangaroo",
        "crocodile", "alligator", "shark", "whale", "dolphin", "eagle", "owl",
        "hawk", "insect", "spider", "butterfly", "bee", "jungle", "safari",
    ],
    "NatureAndOutdoors": [
        "nature", "landscape", "sky", "cloud", "sunset", "sunrise", "horizon",
        "mountain", "hill", "valley", "cliff", "forest", "tree", "plant",
        "grass", "flower", "petal", "leaf", "garden", "park", "field",
        "meadow", "desert", "snow", "ice", "rock", "stone", "cave", "volcano",
        "wood", "soil", "fog", "rainbow",
    ],
    "WaterRelatedElements": [
        "water", "ocean", "sea", "lake", "river", "pond", "stream",
        "waterfall", "beach", "shore", "coast", "wave", "tide", "swimming pool",
        "pool", "water park", "fountain", "harbor", "marina", "dock", "pier",
        "surfing", "diving", "snorkeling", "rafting", "kayak", "canoe",
    ],

    # ----------------------------------------------------------------------
    # TRANSPORT
    # ----------------------------------------------------------------------
    "VehiclesTransport": [
        "vehicle", "car", "automobile", "sports car", "suv", "van", "truck",
        "pickup truck", "bus", "minibus", "motorcycle", "scooter", "moped",
        "bicycle", "bike", "tricycle", "boat", "ship", "yacht", "sailboat",
        "jet ski", "airplane", "aircraft", "jet", "helicopter", "drone",
        "train", "tram", "subway", "metro", "taxi", "ambulance", "fire truck",
        "tractor", "forklift", "wheel", "tire", "engine", "car accident",
        "traffic collision", "traffic",
    ],

    # ----------------------------------------------------------------------
    # FOOD, DRINK, SOCIAL
    # ----------------------------------------------------------------------
    "FoodDrinksAndParties": [
        "food", "meal", "dish", "cuisine", "snack", "dessert", "cake",
        "fast food", "fruit", "vegetable", "bread", "pizza", "burger",
        "sandwich", "salad", "soup", "rice", "pasta", "meat", "seafood",
        "drink", "beverage", "coffee", "tea", "juice", "soft drink", "water",
        "restaurant", "cafe", "kitchen", "dining", "table",
        # social / nightlife
        "party", "celebration", "festival", "concert", "nightclub", "club",
        "bar", "pub", "dancing", "dance",
    ],
    "Alcohol": [
        "alcohol", "alcoholic beverage", "wine", "red wine", "white wine",
        "champagne", "beer", "draft beer", "cocktail", "liquor", "whiskey",
        "vodka", "rum", "tequila", "gin", "brandy", "sake", "wine glass",
        "wine bottle", "beer bottle", "beer glass", "shot glass", "bartender",
        "drunk", "intoxication",
    ],
    "Tobacco": [
        "tobacco", "cigarette", "cigar", "cigarillo", "smoking", "smoke",
        "nicotine", "vape", "vaping", "e-cigarette", "vaporizer", "hookah",
        "shisha", "pipe", "ashtray", "lighter",
    ],

    # ----------------------------------------------------------------------
    # SUBSTANCES
    # ----------------------------------------------------------------------
    "Drugs": [
        "drug", "drugs", "narcotic", "cocaine", "heroin", "methamphetamine",
        "meth", "ecstasy", "lsd", "magic mushrooms", "opioids", "ketamine",
        "ghb", "pcp", "bath salts", "mdma", "molly", "acid", "psilocybin",
        "shrooms", "angel dust", "special k", "painkillers",
        "prescription drugs", "adderall", "ritalin", "xanax", "valium",
        "methadone", "benzodiazepines", "barbiturates", "steroids",
        "testosterone", "anabolic steroids", "marijuana", "joint", "cannabis",
        "weed", "hashish", "hash oil", "bong", "water pipe", "chillum",
        "bubbler", "dabbing", "dabs", "blunt", "spliff", "syringe", "needle",
        "powder", "pills",
    ],

    # ----------------------------------------------------------------------
    # WEAPONS & VIOLENCE
    # ----------------------------------------------------------------------
    "Weapons": [
        "weapon", "weaponry", "gun", "firearm", "pistol", "handgun", "revolver",
        "rifle", "shotgun", "assault rifle", "machine gun", "ammunition",
        "bullet", "magazine", "grenade", "explosive", "bomb", "knife", "blade",
        "dagger", "sword", "machete", "axe", "bayonet", "spear", "bow",
        "crossbow", "arrow", "taser", "pepper spray", "brass knuckles",
    ],
    "Violence": [
        "violence", "fight", "fighting", "assault", "brawl", "riot", "war",
        "combat", "battle", "soldier", "military", "blood", "gore", "wound",
        "injury", "corpse", "death", "weapon", "protest", "vandalism",
        "destruction", "explosion", "fire", "burning",
    ],

    # ----------------------------------------------------------------------
    # ACTIVITIES
    # ----------------------------------------------------------------------
    "SportsAndFitness": [
        "sport", "sports", "athlete", "exercise", "fitness", "gym", "workout",
        "yoga", "pilates", "running", "jogging", "marathon", "cycling",
        "swimming", "soccer", "football", "basketball", "baseball", "tennis",
        "golf", "volleyball", "rugby", "cricket", "hockey", "boxing",
        "martial arts", "karate", "judo", "wrestling", "weightlifting",
        "bodybuilding", "skiing", "snowboarding", "skateboarding", "climbing",
        "surfing", "stadium", "ball",
    ],
    "EntertainmentAndMedia": [
        "entertainment", "media", "tv", "television", "movie", "film", "cinema",
        "theatre", "stage", "performance", "concert", "music", "musician",
        "band", "singer", "dj", "microphone", "guitar", "piano", "drum",
        "video game", "gaming", "console", "controller", "animation", "cartoon",
        "comics", "anime", "celebrity", "award", "festival",
    ],
    "ArtAndDrawings": [
        "art", "artwork", "painting", "drawing", "sketch", "illustration",
        "doodle", "graffiti", "mural", "street art", "digital art",
        "sculpture", "statue", "carving", "pottery", "ceramic", "mosaic",
        "collage", "calligraphy", "tattoo", "nude", "abstract", "canvas",
    ],

    # ----------------------------------------------------------------------
    # RELIGION & POLITICS
    # ----------------------------------------------------------------------
    "ReligiousAndPolitical": [
        "religion", "religious", "church", "cathedral", "chapel", "mosque",
        "temple", "synagogue", "shrine", "cross", "crucifix", "bible", "quran",
        "torah", "prayer", "worship", "priest", "monk", "nun", "rosary",
        "candle", "altar", "politics", "political", "flag", "politician",
        "government", "election", "vote", "protest", "demonstration", "rally",
        "campaign", "parliament",
    ],

    # ----------------------------------------------------------------------
    # MONEY, GAMBLING, FRAUD
    # ----------------------------------------------------------------------
    "MoneyAndFinance": [
        "money", "cash", "banknote", "currency", "coin", "dollar", "euro",
        "credit card", "debit card", "wallet", "bank", "atm", "investment",
        "stock market", "cryptocurrency", "bitcoin", "gold", "jewelry",
        "diamond", "luxury",
    ],
    "Gambling": [
        "gambling", "casino", "poker", "blackjack", "roulette", "slot machine",
        "betting", "bet", "lottery", "dice", "playing card", "jackpot",
        "wager", "bookmaker", "chips",
    ],

    # ----------------------------------------------------------------------
    # MEDICAL & HEALTH
    # ----------------------------------------------------------------------
    "MedicalAndHealth": [
        "medical", "medicine", "hospital", "clinic", "doctor", "nurse",
        "surgery", "operation", "patient", "wheelchair", "crutch", "bandage",
        "wound", "blood", "x-ray", "mri", "stethoscope", "syringe", "injection",
        "pill", "tablet", "pharmacy", "prescription", "first aid", "ambulance",
        "disease", "infection", "rash",
    ],

    # ----------------------------------------------------------------------
    # OBJECTS, TECH, PLACES
    # ----------------------------------------------------------------------
    "TechnologyAndElectronics": [
        "technology", "electronics", "electronic device", "computer", "laptop",
        "desktop", "monitor", "screen", "keyboard", "mouse", "smartphone",
        "phone", "mobile phone", "tablet", "camera", "television", "headphones",
        "speaker", "microphone", "router", "server", "circuit", "robot",
        "drone", "gadget", "charger", "cable",
    ],
    "BuildingsAndArchitecture": [
        "building", "architecture", "house", "home", "apartment", "skyscraper",
        "tower", "office", "factory", "warehouse", "store", "shop", "mall",
        "hotel", "school", "hospital", "stadium", "bridge", "monument", "ruins",
        "construction", "real estate", "property", "facade", "roof", "window",
        "door", "wall", "room", "interior",
    ],
    "TextAndDocuments": [
        "text", "document", "paper", "paper product", "book", "magazine",
        "newspaper", "letter", "handwriting", "calligraphy", "font",
        "receipt", "invoice", "ticket", "passport", "id card", "license",
        "certificate", "contract", "sign", "poster", "banner", "label",
        "screenshot", "qr code", "barcode",
    ],

    # ----------------------------------------------------------------------
    # ALERT / HARD-BLOCK BUCKETS
    # ----------------------------------------------------------------------
    "ExplicitContent": [
        "nudity", "nude", "naked", "pornography", "porn", "erotica", "erotic",
        "sexual content", "sexual activity", "intercourse", "genitals",
        "genitalia", "breasts", "nipple", "buttocks", "cleavage", "lingerie",
        "underwear", "topless", "barechested", "stripper", "adult content",
        "fetish", "bdsm", "sex toy",
    ],
    "HateAndExtremism": [
        "hate", "hate speech", "hate symbol", "racism", "discrimination",
        "swastika", "nazi", "white supremacy", "extremism", "terrorism",
        "terrorist", "propaganda", "genocide", "anti-semitic", "islamophobic",
        "homophobic", "transphobic", "xenophobic", "sexist", "ableist",
        "cult", "radicalization",
    ],
    "SelfHarmAndDisturbing": [
        "self-harm", "suicide", "self-injury", "cutting", "gore", "blood",
        "corpse", "autopsy", "decomposition", "mutilation", "torture",
        "body horror", "graphic surgery", "disturbing", "crime scene",
        "accident",
    ],
    "IllegalAndFraud": [
        "scam", "scams", "fraud", "phishing", "counterfeit", "counterfeiting",
        "forgery", "stolen goods", "theft", "robbery", "smuggling",
        "money laundering", "tax evasion", "identity theft", "impersonation",
        "piracy", "copyright infringement", "illegal sales", "black market",
    ],

    # Broad catch-all bucket that combines several of the alert buckets above
    # into a single "anything flagged" list.
    "SafeSearchFlaggedContent": [
        "adult", "spoof", "medical", "violence", "racy", "hate", "drugs",
        "gambling", "tobacco", "terrorism", "propaganda", "harassment",
        "bullying", "self-harm", "suicide", "child abuse", "exploitation",
        "weaponry", "weapon", "assault", "fighting", "accidents",
        "misinformation", "disinformation", "scams", "fraud", "phishing",
        "nudity", "theft", "robbery", "counterfeiting", "counterfeit",
        "pornography", "erotica", "barechested", "breasts", "genitals",
        "buttocks", "sexual content", "profanity", "obscenity", "racism",
        "discrimination", "animal cruelty", "genocide", "torture",
        "mutilation", "stalking", "anti-semitic", "islamophobic", "homophobic",
        "transphobic", "xenophobic", "sexist", "ableist", "conspiracy",
        "cults", "political extremism", "impersonation", "identity theft",
        "copyright infringement", "illegal sales", "stolen goods",
        "money laundering", "tax evasion", "bestiality", "pedophilia",
        "sexual harassment", "body horror", "graphic surgery", "gore", "blood",
        "autopsy", "decomposition", "vandalism", "soldier", "smoking",
    ],
}


def get_categories(name: str) -> list:
    """Return the keyword list for a category, or [] if unknown."""
    return CATEGORIES.get(name, [])


def all_category_names() -> list:
    """Convenience: every available category name."""
    return list(CATEGORIES.keys())
