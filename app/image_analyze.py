"""
Image analysis.

Turns a raw Google Vision response into a readable summary and matches the
detected labels against the full category taxonomy in bad_categories.py. No
roles, no per-business config — every upload is analyzed against everything, and
the caller decides what to do with the matches.
"""

from bad_categories import CATEGORIES

# Labels that indicate a person is in the image.
HUMAN_LABELS = {
    "face", "chin", "cheek", "eyebrow", "eye", "nose", "mouth", "lip", "ear",
    "forehead", "man", "woman", "girl", "boy", "child", "adult", "people", "human",
}

# SafeSearch likelihood -> numeric risk level.
SAFE_SEARCH_LEVELS = {
    "UNKNOWN": 0,
    "VERY_UNLIKELY": 0,
    "UNLIKELY": 1,
    "POSSIBLE": 2,
    "LIKELY": 3,
    "VERY_LIKELY": 4,
}


def process(response: dict) -> dict:
    """Build the analysis summary from a serialized Vision response."""
    labels = [a["description"].lower() for a in response.get("labelAnnotations", [])]

    # Keys we match categories against: the labels plus the markers below.
    image_analysis = {label: None for label in labels}

    full_text = response.get("fullTextAnnotation", {}).get("text", "")
    text = " ".join(full_text.split()).strip().lower() if full_text else None
    if text:
        image_analysis["hasText"] = text

    is_human = any(label in HUMAN_LABELS for label in labels)
    if is_human:
        image_analysis["isHuman"] = None

    logos = [a["description"].strip().lower() for a in response.get("logoAnnotations", [])]
    has_logo = ", ".join(dict.fromkeys(logos)) if logos else None
    if has_logo:
        image_analysis["hasLogo"] = has_logo

    safe_search = response.get("safeSearchAnnotation", {})
    matched = _match_all_categories(list(image_analysis.keys()))

    return {
        "labels": labels,
        "text": text,
        "isHuman": is_human,
        "hasLogo": has_logo,
        "safeSearch": {k: v.lower() for k, v in safe_search.items()},
        "safeSearchClassification": classify_image(safe_search),
        "matchedCategories": matched,            # {category: [keywords]} that hit
        "categories": list(matched.keys()),      # just the category names
    }


def _match_all_categories(analysis_keys: list) -> dict:
    """Match the detected keys against every category in the taxonomy."""
    keys = set(analysis_keys)
    matched = {}
    for category, keywords in CATEGORIES.items():
        hits = [kw for kw in keywords if kw in keys]
        if hits:
            matched[category] = hits
    return matched


def classify_image(safe_search: dict) -> str:
    """Risk classification from the SafeSearch annotation."""
    max_level = 0
    for likelihood in safe_search.values():
        max_level = max(max_level, SAFE_SEARCH_LEVELS.get(likelihood, 0))

    if max_level >= 3:
        return "alert"
    if max_level == 2:
        return "need_approval"
    return "good"
