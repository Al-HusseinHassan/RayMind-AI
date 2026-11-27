"""
prediction.py - inference code for the DEPI classifier (CT, CXR and cough-sound images).

There is one trained model per modality. Files expected next to this script:
    config.json        image size, colour mode and, for each modality, its model file and preprocessing
    class_names.json   class names, in the same order used during training
    best_model_CT.keras, best_model_CXR.keras, best_model_Cough_sound.keras

Requirements:  pip install tensorflow pillow numpy

Public functions
    preprocessor(image, modality)              -> numpy array (1, height, width, 3) ready for model.predict
    final_prediction(image, modality)          -> dict with predicted class, confidence and all probabilities

`modality` is "CT", "CXR" or "Cough sound". `image` can be a file path, bytes, an open
file / upload object, a PIL image or a numpy array.

Command line:
    python prediction.py path/to/image.jpg CXR
"""
import io
import json
import os
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image

PACKAGE_DIR = Path(__file__).resolve().parent


# ----------------------------------------------------------------------------------------------
# 1) Loading the artifacts
# ----------------------------------------------------------------------------------------------
def _artifacts_dir():
    """Folder that holds config.json, class_names.json and the .keras files."""
    for folder in (os.environ.get("ARTIFACTS_DIR"), PACKAGE_DIR, PACKAGE_DIR / "artifacts"):
        if folder and (Path(folder) / "config.json").exists():
            return Path(folder)
    raise FileNotFoundError("config.json was not found. Keep the artifact files next to prediction.py "
                            "or set the ARTIFACTS_DIR environment variable.")


@lru_cache(maxsize=1)
def load_config():
    """Returns (config, class_names, folder). Read once."""
    folder = _artifacts_dir()
    with open(folder / "config.json", encoding="utf-8") as f:
        config = json.load(f)
    with open(folder / config.get("class_names_file", "class_names.json"), encoding="utf-8") as f:
        class_names = json.load(f)
    return config, class_names, folder


def _check_modality(modality):
    config, _, _ = load_config()
    if modality not in config["modalities"]:
        raise ValueError(f"Unknown modality '{modality}'. Choose one of: {list(config['modalities'])}")


@lru_cache(maxsize=None)
def load_model(modality):
    """Load the model of one modality once and reuse it."""
    _check_modality(modality)
    config, class_names, folder = load_config()
    model = tf.keras.models.load_model(folder / config["modalities"][modality]["model_file"], compile=False)
    if model.output_shape[-1] != len(class_names):
        raise ValueError(f"The {modality} model has {model.output_shape[-1]} outputs but "
                         f"class_names.json has {len(class_names)} classes.")
    return model


# ----------------------------------------------------------------------------------------------
# 2) Image preprocessing (must match what was done during training)
# ----------------------------------------------------------------------------------------------
def _to_pil_image(image):
    """Turn a path, bytes, file-like object, PIL image or numpy array into a PIL image."""
    if isinstance(image, Image.Image):
        return image
    if isinstance(image, (str, os.PathLike)):
        return Image.open(image)
    if isinstance(image, (bytes, bytearray)):
        return Image.open(io.BytesIO(image))
    if isinstance(image, np.ndarray):
        array = image
        if array.dtype != np.uint8:                                  # floats in 0..1 -> 0..255
            array = (array * 255.0 if array.max() <= 1.0 else array).clip(0, 255).astype("uint8")
        return Image.fromarray(array)
    if hasattr(image, "read"):                                       # open file or uploaded file object
        return Image.open(image)
    raise TypeError(f"Unsupported image type: {type(image)}")


def preprocessor(image, modality):
    """
    Prepare one image for the model of `modality`:
      1. read it and convert to 3-channel RGB (grayscale / RGBA / palette images are handled),
      2. resize to the training size (config["image_size"]) with bilinear interpolation,
      3. normalize: "rescale_0_1" -> pixels / 255, "vgg19" -> VGG19 ImageNet preprocessing,
      4. add the batch dimension -> shape (1, height, width, 3).
    """
    _check_modality(modality)
    config, _, _ = load_config()
    height, width = config["image_size"]

    try:
        pil_image = _to_pil_image(image).convert("RGB")
    except (OSError, ValueError) as error:
        raise ValueError(f"Could not read the image: {error}") from error

    array = np.asarray(pil_image, dtype="float32")                   # (h, w, 3), values 0..255
    array = tf.image.resize(array, (height, width), method="bilinear").numpy()

    if config["modalities"][modality]["preprocessing"] == "vgg19":
        array = tf.keras.applications.vgg19.preprocess_input(array.copy())
    else:
        array = array / 255.0

    return np.expand_dims(array, axis=0).astype("float32")


# ----------------------------------------------------------------------------------------------
# 3) Prediction
# ----------------------------------------------------------------------------------------------
def final_prediction(image, modality):
    """
    Run the whole pipeline on one image and return:
        {
          "modality": "CXR",
          "predicted_class": "covid",
          "class_index": 3,
          "confidence": 0.9731,            # probability of the predicted class, 0..1
          "probabilities": {"Healthy": 0.01, "LungsCancer": 0.0, "Pneumonia": 0.01, "covid": 0.97}
        }
    """
    _, class_names, _ = load_config()
    model = load_model(modality)

    probabilities = model.predict(preprocessor(image, modality), verbose=0)[0]
    class_index = int(np.argmax(probabilities))
    return {
        "modality": modality,
        "predicted_class": class_names[class_index],
        "class_index": class_index,
        "confidence": float(probabilities[class_index]),
        "probabilities": {name: float(p) for name, p in zip(class_names, probabilities)},
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Usage: python prediction.py path/to/image.jpg "CT" | "CXR" | "Cough sound"')
    print(json.dumps(final_prediction(sys.argv[1], sys.argv[2]), indent=2))
