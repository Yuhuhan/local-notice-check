# Field Notes: Making NoticeCheck Fully Local

NoticeCheck started as a cloud-backed version of my Pakistan Notice Helper app.
For the Hugging Face Hackathon, I rebuilt it so the same pipeline could also run
locally with Docker Compose and an NVIDIA GPU.

## What I Tried

I tested several vision-language model setups before settling on the current
architecture. Smaller MiniCPM-V experiments were not reliable enough on
high-risk scam cases. Qwen experiments performed better, but introduced larger
models, separate vision projectors, cold starts, and more infrastructure.

The final app uses:

- `openbmb/MiniCPM5-1B` for structured notice assessment
- `nvidia/NVIDIA-Nemotron-Parse-v1.2` for screenshot text extraction
- Hugging Face ZeroGPU for the hosted demo
- Docker Compose and local CUDA for private local deployment

## Problems I Hit

Structured output was one of the first major issues. Models sometimes returned
incomplete or malformed JSON. I added a strict schema, bounded prompts,
normalization, retries, and a repair pass so every successful result follows the
same contract.

The ZeroGPU deployment exposed several integration problems:

- CUDA and PyTorch ABI mismatches
- missing OCR dependencies such as `einops`, `open_clip_torch`, and `ftfy`
- GPU quota handling and Hugging Face iframe token forwarding
- model-loading and cold-start failures hidden behind worker wrappers

Screenshot handling also required more than OCR. Ordinary photos could produce
image descriptions or parser output instead of notice text. Sending that output
to the language model caused generic generation failures. I added semantic
region filtering and a dedicated warning that asks the user to upload a clear
notice or message screenshot.

The local Docker build revealed another practical problem: one Python dependency
needed compilation, so the CUDA image required `build-essential`. CUDA base
images and model caches are also large, which made persistent volumes and Docker
disk cleanup important parts of testing.

## What I Learned

Making an AI application local is not only about downloading model weights. A
usable local product also needs:

- reproducible GPU and dependency setup
- predictable structured output
- explicit input validation
- clear user-facing failure messages
- privacy-aware tracing
- persistent model caching
- realistic disk and VRAM planning

I also learned to treat model evaluation as part of product development. A model
that works in a simple smoke test may still fail on phishing links, OTP theft,
Roman Urdu screenshots, harmless reminders, or the application's JSON contract.

## Result

NoticeCheck now has a redesigned English interface and can run in two modes:

- hosted on Hugging Face ZeroGPU
- fully local on an NVIDIA GPU

The local version starts with:

```bash
docker compose up --build
```

## Links

- [Live demo](https://huggingface.co/spaces/build-small-hackathon/noticecheck)
- [GitHub repository](https://github.com/kingabzpro/local-notice-check)
- [Privacy-safe trace dataset](https://huggingface.co/datasets/build-small-hackathon/pakistan-notice-helper-traces)
- [LinkedIn project post](https://www.linkedin.com/posts/1abidaliawan_huggingfacehackathon-huggingface-ai-ugcPost-7471594790506192896--_53/)
