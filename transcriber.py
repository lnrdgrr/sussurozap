import os
import time

import whisper

import paths

_MODEL_NAME = "base"
_model = None

SUPPORTED_EXTENSIONS = (".ogg", ".mp3", ".aiff", ".aif")

_vendor_ffmpeg_dir = paths.vendor_ffmpeg_dir()
if _vendor_ffmpeg_dir:
    os.environ["PATH"] = _vendor_ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")


def _get_model():
    global _model
    if _model is None:
        _model = whisper.load_model(_MODEL_NAME, download_root=paths.vendor_models_dir())
    return _model


def transcribe_file(file_path):
    """Transcribe an audio file with the local Whisper model.

    Returns a dict: {text, duration_sec, model_used}
    Raises FileNotFoundError / ValueError / RuntimeError on failure.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(SUPPORTED_EXTENSIONS)
        raise ValueError(f"Formato não suportado ({ext}). Formatos aceitos: {supported}")

    model = _get_model()

    start = time.time()
    try:
        result = model.transcribe(file_path, fp16=False)
    except Exception as exc:
        raise RuntimeError(f"Falha ao transcrever o áudio: {exc}") from exc
    processing_sec = time.time() - start

    segments = result.get("segments") or []
    audio_duration_sec = segments[-1]["end"] if segments else 0.0

    text = result.get("text", "").strip()
    return {
        "text": text,
        "duration_sec": round(audio_duration_sec, 2),
        "processing_sec": round(processing_sec, 2),
        "model_used": _MODEL_NAME,
    }
