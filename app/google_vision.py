"""
Google Vision service.

Accepts raw image bytes uploaded by the client and sends them to the Vision API
as `content` (a direct upload, rather than pointing Vision at a GCS URI).

Authentication uses a service-account key file, pointed to by the
GOOGLE_APPLICATION_CREDENTIALS env var (the google-cloud-vision client picks it
up automatically).
"""

from google.cloud import vision

# Everything we want Vision to detect on every upload.
FEATURES = [
    {"type_": vision.Feature.Type.LABEL_DETECTION, "max_results": 10},
    {"type_": vision.Feature.Type.TEXT_DETECTION, "max_results": 5},
    {"type_": vision.Feature.Type.LOGO_DETECTION, "max_results": 5},
    {"type_": vision.Feature.Type.SAFE_SEARCH_DETECTION, "max_results": 5},
]


class GoogleVision:
    def __init__(self):
        # Reads GOOGLE_APPLICATION_CREDENTIALS from the environment.
        self.client = vision.ImageAnnotatorClient()

    def verify_image(self, image_bytes: bytes) -> dict:
        """Annotate a single uploaded image and return the raw Vision response."""
        image = vision.Image(content=image_bytes)
        response = self.client.annotate_image({"image": image, "features": FEATURES})

        # Surface API-level errors to the caller.
        if response.error.message:
            return {"error": f"Vision API Error: {response.error.message}"}

        return self._serialize(response)

    @staticmethod
    def _serialize(response) -> dict:
        """Flatten the protobuf response into plain JSON-friendly structures."""
        safe = response.safe_search_annotation
        likelihood = vision.Likelihood

        return {
            "labelAnnotations": [
                {"description": a.description, "score": round(a.score, 4)}
                for a in response.label_annotations
            ],
            "logoAnnotations": [
                {"description": a.description, "score": round(a.score, 4)}
                for a in response.logo_annotations
            ],
            "fullTextAnnotation": {
                "text": response.full_text_annotation.text
            } if response.full_text_annotation.text else {},
            "safeSearchAnnotation": {
                "adult": likelihood(safe.adult).name,
                "spoof": likelihood(safe.spoof).name,
                "medical": likelihood(safe.medical).name,
                "violence": likelihood(safe.violence).name,
                "racy": likelihood(safe.racy).name,
            },
        }
