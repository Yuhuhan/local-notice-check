"""Gradio Server routes and static frontend."""

from __future__ import annotations

from typing import Any

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from gradio import Server

from app.config import STATIC_DIR
from app.model_endpoint import model_status, probe_ocr_runtime, probe_space_runtime
from app.service import analyze_notice
from app.trace import trace_status

app = Server()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.api(
    name="analyze",
    description="Assess a notice for common scam signals.",
    concurrency_limit=1,
)
def analyze_api(
    text: str = "",
    image_data_url: str = "",
    example_id: str = "",
    save_trace: bool = True,
    output_language: str = "en",
) -> dict[str, Any]:
    return analyze_notice(
        text,
        image_data_url,
        example_id,
        save_trace,
        output_language,
    )


@app.api(name="status", description="Return model and privacy status.", queue=False)
def status_api() -> dict[str, Any]:
    return model_status()


@app.api(
    name="runtime_probe",
    description="Return sanitized fixed-input model runtime diagnostics.",
)
def runtime_probe_api() -> dict[str, str]:
    return probe_space_runtime()


@app.api(
    name="ocr_probe",
    description="Return sanitized bundled-image OCR runtime diagnostics.",
)
def ocr_probe_api() -> dict[str, str]:
    return probe_ocr_runtime()


@app.api(
    name="trace_status",
    description="Return privacy-safe trace queue status.",
    queue=False,
)
def trace_status_api() -> dict[str, Any]:
    return trace_status()


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}
