# Local model setup

The application has separate Space and local runtimes:

- **Space:** `openbmb/MiniCPM5-1B` through Transformers, plus
  `nvidia/nemotron-ocr-v2` for screenshots
- **Local:** `openbmb/MiniCPM5-1B-GGUF` through `llama-cpp-python`

No remote model API is required.

## Supported environment

Nemotron OCR v2 requires Linux amd64, an NVIDIA GPU, CUDA build/runtime
compatibility, and Python 3.12. The Space metadata pins Python 3.12.

Install the Space dependencies:

```bash
python -m pip install -r requirements.txt
```

The OCR dependency is NVIDIA's prebuilt `cp312` wheel from its official
ZeroGPU Space. The Space follows NVIDIA's CUDA 12.8 PyTorch and torchvision
requirements for OCR. MiniCPM uses Transformers on the same ZeroGPU allocation.
The Space does not install `llama-cpp-python`.

## MiniCPM configuration

Defaults:

```text
openbmb/MiniCPM5-1B-GGUF
MiniCPM5-1B-Q8_0.gguf
```

Overrides:

```powershell
$env:MODEL_REPO_ID = "openbmb/MiniCPM5-1B-GGUF"
$env:MODEL_FILENAME = "MiniCPM5-1B-Q8_0.gguf"
$env:MODEL_CONTEXT_SIZE = "8192"
$env:MODEL_GPU_LAYERS = "0"
$env:MODEL_ENABLE_THINKING = "0"
```

Use `MODEL_PATH` for an existing GGUF. Schema-constrained generation is the
default because it is more reliable for the application response contract.
Set `MODEL_ENABLE_THINKING=1` only for experiments; it uses a larger token
budget but still must produce schema-valid JSON.

Set `MODEL_GPU_LAYERS=-1` when using a locally built CUDA-enabled
`llama-cpp-python` installation outside ZeroGPU.

```powershell
python -m pip install -r requirements-local.txt
python app.py --download-model
python app.py --test-endpoint
python app.py
```

## ZeroGPU lifecycle

Inference runs inside `@spaces.GPU(duration=60)`. Nemotron OCR first extracts
paragraph text from a screenshot, then the Transformers MiniCPM5-1B model
assesses that text. Both Space models are cached in the ZeroGPU worker. Local
runs use only the separate GGUF/llama.cpp path.

## Language limits

Nemotron OCR v2 officially supports English, Chinese, Japanese, Korean, and
Russian. It does not officially support Urdu script. Roman Urdu uses Latin
characters and may be readable, but accuracy is not guaranteed.

MiniCPM5-1B is officially evaluated in English and Chinese. Urdu and Roman Urdu
reasoning/output are best effort and must be validated on this app's data.
