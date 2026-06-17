# Build an Image Moderation API with Flask, Docker, and Google Cloud Vision


[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat-square&logo=python)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0-darkgreen?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![Google Cloud Vision](https://img.shields.io/badge/Google%20Cloud-Vision%20API-red?style=flat-square&logo=google-cloud)](https://cloud.google.com/vision)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/murilolivorato/gcp-vision-moderation-api-flask-docker?style=social)](https://github.com/murilolivorato/gcp-vision-moderation-api-flask-docker)

<div align="center">
  <img src="https://cdn-images-1.medium.com/max/800/1*llAxB81ZfcSA9bLgAIFsow.png" alt="Text Moderation Flow" width="700">
</div>
---

**Read the full article on Medium:**

✍️ [https://medium.com/@murilolivorato/build-an-image-moderation-api-with-flask-docker-and-google-cloud-vision-6d46b77b978f](https://medium.com/@murilolivorato/build-an-image-moderation-api-with-flask-docker-and-google-cloud-vision-6d46b77b978f)


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

## Usage

**1. Set up the request in Postman.** Create a `POST` request to
`http://localhost:5000/analyze`, open the **Body** tab, and choose **form-data**.
Add a key named `image` and switch its type from *Text* to **File**.

<div align="center">
  <img src="https://cdn-images-1.medium.com/max/800/1*BTnmU2oT9qk83njYFKZ8Kw.png" alt="Postman form-data request set to POST /analyze with an &quot;image&quot; field of type File" width="700">
</div>

**2. Select an image.** Click **Select Files** on the `image` field and pick the
picture you want to analyze (here, a photo of someone surfing).

<div align="center">
  <img src="https://cdn-images-1.medium.com/max/800/1*prEYIEm6konDItNQ69oDag.png" alt="Choosing the surfing image file for the image field" width="700">
</div>

**3. Send the request.** Hit **Send** to upload the image to the API.

<div align="center">
  <img src="https://cdn-images-1.medium.com/max/800/1*RmN_8sobz5uPjRmvVhDDbQ.png" alt="Submitting the request in Postman" width="700">
</div>

**4. Read the response.** The API returns the analysis — detected labels, matched
categories, SafeSearch ratings, and the overall classification:

```json
{
    "analysis": {
        "categories": [
            "WaterRelatedElements",
            "FoodDrinksAndParties",
            "SportsAndFitness"
        ],
        "hasLogo": null,
        "isHuman": false,
        "labels": [
            "boardsport",
            "surfboard",
            "surfing",
            "water",
            "surfing--equipment and supplies",
            "water sport",
            "wave",
            "list of surface water sports",
            "fluid",
            "personal protective equipment"
        ],
        "matchedCategories": {
            "FoodDrinksAndParties": [
                "water"
            ],
            "SportsAndFitness": [
                "surfing"
            ],
            "WaterRelatedElements": [
                "water",
                "wave",
                "surfing"
            ]
        },
        "safeSearch": {
            "adult": "very_unlikely",
            "medical": "very_unlikely",
            "racy": "unlikely",
            "spoof": "very_unlikely",
            "violence": "very_unlikely"
        },
        "safeSearchClassification": "good",
        "text": null
    },
    "filename": "surfing_img.png",
    "raw": {
        "fullTextAnnotation": {},
        "labelAnnotations": [
            {
                "description": "Boardsport",
                "score": 0.9867
            },
            {
                "description": "Surfboard",
                "score": 0.9863
            },
            {
                "description": "Surfing",
                "score": 0.9834
            },
            {
                "description": "Water",
                "score": 0.9824
            },
            {
                "description": "Surfing--Equipment and supplies",
                "score": 0.9772
            },
            {
                "description": "Water sport",
                "score": 0.9634
            },
            {
                "description": "Wave",
                "score": 0.9623
            },
            {
                "description": "List of surface water sports",
                "score": 0.9603
            },
            {
                "description": "Fluid",
                "score": 0.9558
            },
            {
                "description": "Personal protective equipment",
                "score": 0.9555
            }
        ],
        "logoAnnotations": [],
        "safeSearchAnnotation": {
            "adult": "VERY_UNLIKELY",
            "medical": "VERY_UNLIKELY",
            "racy": "UNLIKELY",
            "spoof": "VERY_UNLIKELY",
            "violence": "VERY_UNLIKELY"
        }
    }
}
```

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



<div align="center">
  <h3>⭐ Star This Repository ⭐</h3>
  <p>Your support helps us improve and maintain this project!</p>
  <a href="https://github.com/murilolivorato/gcp-vision-moderation-api-flask-docker/stargazers">
    <img src="https://img.shields.io/github/stars/murilolivorato/gcp-vision-moderation-api-flask-docker?style=social" alt="GitHub Stars">
  </a>
</div>
