# Upload with Google Vision (Python)

Flask backend that accepts an uploaded image and analyzes it with the Google
Cloud Vision API. It analyzes the image bytes uploaded directly by the client —
no storage bucket required.

## Run

```bash
docker compose up -d --build
```

The API listens on `http://localhost:5000`.

## Endpoints

| Method | Path       | Description                          |
|--------|------------|--------------------------------------|
| GET    | `/`        | Welcome / status                     |
| GET    | `/health`  | Health check                         |
| POST   | `/analyze` | Upload an image and analyze it       |

## Analyze an image (Postman)

1. Method: **POST**, URL: `http://localhost:5000/analyze`
2. Body tab → **form-data**
3. Add key `image`, set its type to **File**, and choose an image (max 10 MB)
4. Send.

That's it — no roles, no options. Every image is analyzed the same way and the
result is also logged server-side (`docker compose logs -f`).

### What the analysis contains

The image's Vision labels are matched against the full taxonomy in
[app/bad_categories.py](app/bad_categories.py) — a generic, business-agnostic set
(29 categories, ~900 keywords). Every category that matches is reported in
`matchedCategories`:

```
People:      HumanBody, HumanPresence, ClothingAndSwimwear
Animals:     PetsAndAnimals, Wildlife
Nature:      NatureAndOutdoors, WaterRelatedElements
Transport:   VehiclesTransport
Food/social: FoodDrinksAndParties, Alcohol, Tobacco
Substances:  Drugs
Weapons:     Weapons, Violence
Activities:  SportsAndFitness, EntertainmentAndMedia, ArtAndDrawings
Society:     ReligiousAndPolitical, MoneyAndFinance, Gambling, MedicalAndHealth
Objects:     TechnologyAndElectronics, BuildingsAndArchitecture, TextAndDocuments
Alert:       ExplicitContent, HateAndExtremism, SelfHarmAndDisturbing,
             IllegalAndFraud, SafeSearchFlaggedContent
```

### Example response

```json
{
  "filename": "cat.jpg",
  "analysis": {
    "labels": ["cat", "felidae", "whiskers", "snout", "fur", "..."],
    "text": null,
    "isHuman": false,
    "hasLogo": null,
    "safeSearch": { "adult": "very_unlikely", "racy": "unlikely", "...": "..." },
    "safeSearchClassification": "need_approval",
    "matchedCategories": { "PetsAndAnimals": ["cat", "whiskers", "fur", "snout"] },
    "categories": ["PetsAndAnimals"]
  },
  "raw": { "labelAnnotations": [], "logoAnnotations": [], "safeSearchAnnotation": {}, "fullTextAnnotation": {} }
}
```

- `analysis` is the processed summary: detected labels, any text, human/logo
  presence, SafeSearch ratings, and which categories the image matched.
- `raw` is the unmodified Google Vision response.

### Server log

Each upload is logged both to the console (`docker compose logs -f`) **and** to a
file at `logs/analyze.log` on the host (mounted volume, rotates at 5 MB, keeps 5
backups):

```
[INFO] Received image 'cat.jpg' (84614 bytes)
[INFO] Analyzed 'cat.jpg': labels=['cat', 'whiskers', ...] categories=['PetsAndAnimals'] safeSearch=need_approval
[INFO] Full analysis 'cat.jpg': {"labels": [...], "matchedCategories": {...}, ...}
```

The log location is set by the `LOG_FILE` env var in `docker-compose.yml`.

## Credentials

Authentication uses a Google service-account key. The key is mounted into the
container and pointed to by `GOOGLE_APPLICATION_CREDENTIALS`
(`/keys/service-account.json`, set in `docker-compose.yml`). Put your own key at
`keys/service-account.json` to use a different project. The `keys/` folder is
git-ignored.

## Project layout

```
.
├── app/
│   ├── main.py            # Flask routes (/, /health, /analyze) + logging
│   ├── google_vision.py   # Vision API call (uploads image bytes as `content`)
│   ├── image_analyze.py   # Response processing + category matching
│   ├── bad_categories.py  # Generic category keyword taxonomy
│   └── requirements.txt
├── keys/service-account.json   # git-ignored
├── Dockerfile
└── docker-compose.yml
```
