import json
import os

import webview

import history_db
import paths
import transcriber

_BASE_DIR = paths.base_dir()


class Api:
    def transcribe_file(self, file_path):
        try:
            result = transcriber.transcribe_file(file_path)
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

        history_db.save_transcription(
            filename=os.path.basename(file_path),
            filepath=file_path,
            transcript_text=result["text"],
            duration_sec=result["duration_sec"],
            model_used=result["model_used"],
        )
        return {"ok": True, **result}

    def get_history(self):
        return history_db.get_history_grouped_by_day()

    def open_file_dialog(self):
        patterns = ";".join(f"*{ext}" for ext in transcriber.SUPPORTED_EXTENSIONS)
        file_types = (f"Arquivos de áudio ({patterns})",)
        result = webview.windows[0].create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
        )
        if result:
            return result[0]
        return None


def _on_dropzone_drop(window, event):
    files = (event.get("dataTransfer") or {}).get("files") or []
    for file in files:
        full_path = file.get("pywebviewFullPath")
        if full_path:
            window.evaluate_js(f"window.transcribePath({json.dumps(full_path)})")


def _setup_drag_and_drop(window):
    dropzone = window.dom.get_element("#dropzone")
    if dropzone:
        dropzone.on("drop", lambda event: _on_dropzone_drop(window, event))


def main():
    history_db.init_db()
    api = Api()
    window = webview.create_window(
        "SussuroZap",
        os.path.join(_BASE_DIR, "ui", "index.html"),
        js_api=api,
        width=1000,
        height=700,
        min_size=(700, 500),
    )
    window.events.loaded += _setup_drag_and_drop
    webview.start()


if __name__ == "__main__":
    main()
