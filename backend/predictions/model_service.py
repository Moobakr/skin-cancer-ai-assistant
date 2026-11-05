from __future__ import annotations

import json
import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from django.conf import settings

from .preprocessing import build_metadata_row, preprocess_image_for_model
from .risk import confidence_level, description_for_class, risk_for_class, uncertainty_warnings, DISCLAIMER

try:
    import tensorflow as tf
except Exception:  # pragma: no cover - allows Django shell without TensorFlow installed
    tf = None

DEFAULT_CLASSES = ["ACK", "BCC", "MEL", "NEV", "SCC", "SEK"]


class SkinCancerModelService:
    """Singleton-style model loader.

    The model is loaded once when the service is created. This avoids reloading
    a heavy Keras model on every request.
    """

    def __init__(self):
        self.bundle_dir = Path(settings.MODEL_BUNDLE_DIR)
        self.model = None
        self.class_names = DEFAULT_CLASSES
        self.metadata_schema = None
        self.metadata_preprocessor = None
        self.mode = "demo"
        self.load_error = None
        self._load_bundle()

    def _load_bundle(self):
        model_path = self.bundle_dir / "model.keras"
        class_path = self.bundle_dir / "class_names.json"
        schema_path = self.bundle_dir / "metadata_schema.json"
        preprocessor_path = self.bundle_dir / "metadata_preprocessor.joblib"

        if class_path.exists():
            self.class_names = json.loads(class_path.read_text(encoding="utf-8"))

        if schema_path.exists():
            self.metadata_schema = json.loads(schema_path.read_text(encoding="utf-8"))

        if preprocessor_path.exists():
            self.metadata_preprocessor = joblib.load(preprocessor_path)

        if not model_path.exists():
            self.mode = "demo"
            self.load_error = "No model.keras found in backend/model_bundle. Demo-safe mode is active."
            return
        if tf is None:
            self.mode = "demo"
            self.load_error = "TensorFlow is not available. Demo-safe mode is active."
            return

        try:
            self.model = tf.keras.models.load_model(model_path, compile=False)
            self.mode = "real"
            self.load_error = None
        except Exception as exc:
            self.mode = "demo"
            self.load_error = f"Could not load model: {exc}"

    @property
    def model_loaded(self) -> bool:
        return self.model is not None and self.mode == "real"

    def health(self) -> dict:
        return {
            "status": "ok",
            "model_loaded": self.model_loaded,
            "mode": self.mode,
            "class_names": self.class_names,
            "load_error": self.load_error,
        }

    def _demo_predict(self, image_array: np.ndarray, metadata: dict) -> np.ndarray:
        """Deterministic placeholder probabilities for development without weights.

        This keeps the React/Django app fully demonstrable before training. The
        response always includes a warning that outputs are placeholders.
        """
        seed = int(float(np.mean(image_array)) * 1000) % 100000
        seed += sum(ord(ch) for ch in str(metadata))
        rng = random.Random(seed)
        raw = np.array([rng.random() + 0.2 for _ in self.class_names], dtype="float32")
        return raw / raw.sum()

    def _real_predict(self, image_array: np.ndarray, request_data: dict) -> np.ndarray:
        img = image_array[0]
        augmented = np.stack([
            img,
            img[:, ::-1, :],        # horizontal flip
            img[::-1, :, :],        # vertical flip
            np.rot90(img, k=1),     # 90° rotation
            img[::-1, ::-1, :],     # 180° flip
        ], axis=0)

        if self.metadata_schema and self.metadata_preprocessor:
            feature_columns = self.metadata_schema["feature_columns"]
            row = build_metadata_row(request_data, feature_columns)
            metadata_df = pd.DataFrame([row], columns=feature_columns)
            metadata_array = self.metadata_preprocessor.transform(metadata_df).astype("float32")
            metadata_batch = np.repeat(metadata_array, len(augmented), axis=0)
            all_probs = self.model.predict(
                {"image_input": augmented, "metadata_input": metadata_batch}, verbose=0
            )
        else:
            all_probs = self.model.predict(augmented, verbose=0)

        return np.mean(all_probs, axis=0).astype("float32")

    def predict(self, image, request_data: dict, quality_report: dict) -> dict:
        image_array = preprocess_image_for_model(image)

        if self.model_loaded:
            probs = self._real_predict(image_array, request_data)
            mode_warning = None
        else:
            probs = self._demo_predict(image_array, request_data)
            mode_warning = "Demo-safe mode is active because no trained model bundle is loaded. These probabilities are placeholders."

        probs = probs / max(float(np.sum(probs)), 1e-8)
        probabilities = {self.class_names[i]: float(probs[i]) for i in range(len(self.class_names))}
        sorted_items = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
        predicted_class, confidence = sorted_items[0]

        warnings = uncertainty_warnings(probabilities)
        if mode_warning:
            warnings.insert(0, mode_warning)

        return {
            "predicted_class": predicted_class,
            "confidence": float(confidence),
            "confidence_level": confidence_level(float(confidence)),
            "risk_level": risk_for_class(predicted_class),
            "class_description": description_for_class(predicted_class),
            "probabilities": probabilities,
            "top_predictions": [
                {"class_name": name, "probability": float(prob)} for name, prob in sorted_items[:3]
            ],
            "quality_report": quality_report,
            "quality_warnings": quality_report.get("warnings", []),
            "uncertainty_warnings": warnings,
            "model_mode": self.mode,
            "disclaimer": DISCLAIMER,
        }


model_service = SkinCancerModelService()
