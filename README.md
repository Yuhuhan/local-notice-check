---
title: NoticeCheck
emoji: 🔎
author: Kingabzpro
collaborators:
- Codex
colorFrom: indigo
colorTo: red
sdk: gradio
sdk_version: 6.17.3
app_file: app.py
python_version: 3.12
pinned: true
license: mit
tags:
- llama-cpp-python
- minicpm5-1b
- nemotron-ocr-v2
- gguf
- zerogpu
- scam-detection
- online-safety
- pakistan
- english
short_description: Review suspicious Pakistani messages before you act.
---

# NoticeCheck

NoticeCheck is a local-first safety assistant for suspicious Pakistani messages,
bills, bank alerts, challans, courier notices, and screenshots. It returns:

- a risk label
- a short explanation based on visible evidence
- warning signs and safer next actions
- a brief reply draft when replying is appropriate

NoticeCheck does not verify the sender and does not provide legal or financial
advice. Find official contact details independently before paying, clicking,
replying, or sharing personal information.

## Runtime

```text
Text or screenshot
        |
        v
Custom Gradio Server frontend
        |
        +--> Nemotron OCR v2 for screenshot text
        |
        v
MiniCPM5-1B Q8_0 through llama-cpp-python
        |
        v
Structured risk assessment
```

- **Reasoning:** `openbmb/MiniCPM5-1B-GGUF`
- **GGUF:** `MiniCPM5-1B-Q8_0.gguf`
- **OCR:** `nvidia/nemotron-ocr-v2`
- **Hosting:** Hugging Face Spaces ZeroGPU or local NVIDIA hardware
- **Interface:** custom English HTML, CSS, and JavaScript

The application does not use a remote model API and has no heuristic assessment
fallback. Model and OCR failures are returned explicitly.

## Repository Layout

```text
app.py                 Thin Space launcher
app/
  cli.py               CLI and startup
  config.py            Environment configuration
  model_endpoint.py    MiniCPM llama.cpp inference
  ocr.py               Nemotron OCR adapter
  server.py            Gradio/FastAPI routes
  service.py           Assessment orchestration
  trace.py             Trace subsystem adapter
static/                Custom frontend
traces/                Privacy-safe trace runtime and tools
experiments/           Preserved historical model experiments
tests/                 Application and trace tests
```

## Run

Nemotron OCR's official wheel requires Linux, Python 3.12, and NVIDIA CUDA.

```bash
python -m pip install -r requirements.txt
python app.py --download-model
python app.py --self-test
python app.py
```

See [local model setup](docs/local_model_setup.md) for environment variables and
ZeroGPU details.

## Testing

```bash
python app.py --self-test
python -m unittest
node --check static/app.js
```

Run a real MiniCPM generation contract test with:

```bash
python app.py --test-endpoint
```

## Language Limits

Nemotron OCR v2 officially supports English, Chinese, Japanese, Korean, and
Russian. Urdu-script screenshots are unsupported. Roman Urdu uses Latin
characters and may work, but OCR accuracy is not guaranteed.

MiniCPM5-1B is officially evaluated in English and Chinese. Urdu and Roman Urdu
responses remain best effort and require task-specific evaluation.

## Privacy-Safe Traces

Trace publishing is optional. Published records contain minimized,
deterministic metadata and exclude raw message text, OCR text, screenshots,
links, identifiers, and complete model responses.

```bash
python -m traces.scripts.analyze_trace_dataset
```

See [the trace dataset card](traces/dataset_card.md) for the schema and privacy
rules.

## Safety

- Redact CNIC numbers, account details, OTPs, PINs, and card information.
- Never trust a phone number or link solely because it appears in a message.
- Confirm through an official website, app, card, statement, or helpline you
  locate independently.
- Treat the output as decision support, not proof that a message is genuine.
