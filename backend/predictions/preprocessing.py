from __future__ import annotations

from io import BytesIO
from typing import Any

import cv2
import numpy as np
from PIL import Image

IMAGE_SIZE = 300


def open_uploaded_image(uploaded_file) -> Image.Image:
    uploaded_file.seek(0)
    image = Image.open(BytesIO(uploaded_file.read())).convert("RGB")
    uploaded_file.seek(0)
    return image


def enhance_image(image: Image.Image) -> Image.Image:
    """Apply CLAHE contrast enhancement and return a new PIL image."""
    arr = np.asarray(image.convert("RGB")).astype(np.uint8)
    lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    return Image.fromarray(enhanced)


def preprocess_image_for_model(image: Image.Image, image_size: int = IMAGE_SIZE) -> np.ndarray:
    arr = np.asarray(image.convert("RGB")).astype(np.uint8)
    arr = cv2.resize(arr, (image_size, image_size), interpolation=cv2.INTER_AREA)
    return np.expand_dims(arr.astype("float32"), axis=0)


def build_metadata_row(request_data: dict[str, Any], feature_columns: list[str]) -> dict[str, Any]:
    """Build one metadata row using the schema produced by training.

    Missing values are passed as None and handled by the fitted sklearn imputer.
    """
    aliases = {
        "gender": "sex",
        "sex": "sex",
        "age": "age",
        "smoke": "smoke",
        "drink": "drink",
        "anatom_site": "anatom_site",
        "region": "anatom_site",
        "body_site": "anatom_site",
    }
    row = {}
    lowered_request = {str(k).lower(): v for k, v in request_data.items()}
    for feature in feature_columns:
        key = str(feature).lower()
        source_key = aliases.get(key, key)
        row[feature] = lowered_request.get(source_key, None)
    return row
