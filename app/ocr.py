"""Nemotron OCR v2 adapter for screenshot text extraction."""

from __future__ import annotations

import base64
import ctypes
import gc
import importlib.util
import io
import re
import sys
import threading
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

SUPPORTED_IMAGE_PATTERN = re.compile(
    r"^data:image/(?:png|jpeg|jpg|webp);base64,(.+)$",
    re.I | re.S,
)
_PIPELINES: dict[str, Any] = {}
_PIPELINE_LOCK = threading.RLock()


class OCRRuntimeError(RuntimeError):
    """A sanitized OCR failure safe to expose through the API."""


def ocr_installed() -> bool:
    return importlib.util.find_spec("nemotron_ocr") is not None


def decode_image_data_url(image_data_url: str) -> bytes:
    match = SUPPORTED_IMAGE_PATTERN.match(image_data_url)
    if not match:
        raise OCRRuntimeError("Unsupported image data.")
    try:
        image_bytes = base64.b64decode(match.group(1), validate=True)
    except (ValueError, TypeError) as exc:
        raise OCRRuntimeError("Invalid image data.") from exc
    if not image_bytes:
        raise OCRRuntimeError("The uploaded image is empty.")
    return image_bytes


def _get_pipeline(language: str = "multi") -> Any:
    with _PIPELINE_LOCK:
        if language not in _PIPELINES:
            try:
                import torch

                for root in map(Path, sys.path):
                    for library in root.glob("nvidia/cuda_runtime/lib/libcudart.so*"):
                        ctypes.CDLL(str(library), mode=ctypes.RTLD_GLOBAL)
                        break
                if torch.cuda.is_available():
                    torch.cuda.init()
                from nemotron_ocr.inference.pipeline_v2 import NemotronOCRV2
            except ImportError as exc:
                raise OCRRuntimeError(
                    "Nemotron OCR v2 or its CUDA runtime is unavailable."
                ) from exc
            _PIPELINES[language] = NemotronOCRV2(lang=language)
        return _PIPELINES[language]


def extract_text(image_data_url: str) -> str:
    """Extract ordered paragraph text using NVIDIA's Space integration pattern."""
    image_bytes = decode_image_data_url(image_data_url)
    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            image_array = np.array(image.convert("RGB"))
        predictions = _get_pipeline("multi")(
            image_array,
            merge_level="paragraph",
        )
        text = "\n\n".join(
            str(item.get("text", "")).strip()
            for item in predictions
            if isinstance(item, dict) and str(item.get("text", "")).strip()
        ).strip()
        if not text:
            raise OCRRuntimeError("No readable text was found in the screenshot.")
        return text
    except OCRRuntimeError:
        raise
    except Exception as exc:
        raise OCRRuntimeError("Nemotron OCR could not read the screenshot.") from exc


def close_ocr() -> None:
    """Release cached OCR pipelines for local shutdown or explicit cleanup."""
    with _PIPELINE_LOCK:
        _PIPELINES.clear()
    gc.collect()
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except ImportError:
        pass
