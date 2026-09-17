# ============================================
# model.py
# Alzheimer MRI Prediction Module
# ============================================

import numpy as np
import tensorflow as tf
from PIL import Image

from config import MODEL_PATH, CLASS_NAMES


IMG_SIZE = (224, 224)


# Load model only once
_model = None


def load_model():
    global _model

    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)

    return _model


def preprocess_image(image):
    """
    Preprocess uploaded MRI image for EfficientNetB0.
    """

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    image = image.convert("RGB")
    image = image.resize(IMG_SIZE)

    image_array = np.array(image, dtype=np.float32)

    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array


def predict_image(image):
    """
    Predict Alzheimer class from MRI image.

    Returns:
        predicted_class
        confidence
        probabilities
    """

    model = load_model()

    processed_image = preprocess_image(image)

    predictions = model.predict(
        processed_image,
        verbose=0
    )[0]

    predicted_index = int(
        np.argmax(predictions)
    )

    confidence = float(
        predictions[predicted_index]
    )

    predicted_class = CLASS_NAMES[
        predicted_index
    ]

    probabilities = {
        CLASS_NAMES[i]: float(predictions[i])
        for i in range(len(CLASS_NAMES))
    }

    return (
        predicted_class,
        confidence,
        probabilities
    )