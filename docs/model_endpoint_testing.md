# Testing the local model

The Space inference path is:

```text
Custom frontend
  -> queued Gradio backend
  -> Nemotron OCR v2 for screenshot text
  -> app/model_endpoint.py
  -> MiniCPM5-1B through Transformers on ZeroGPU
```

Local endpoint tests use MiniCPM5-1B GGUF through `llama-cpp-python`.

## Fast checks

Run tests that do not load the model:

```powershell
python app.py --self-test
python -m unittest
```

Download the configured GGUF:

```powershell
python -m pip install -r requirements-local.txt
python app.py --download-model
```

Run a real text-generation contract test:

```powershell
python app.py --test-endpoint
```

The command fails unless the model returns all required fields:

- `risk_label`
- `simple_explanation`
- `red_flags`
- `safe_next_steps`
- `reply_draft`

The old Modal deployments and request scripts are intentionally preserved under
`experiments/` for comparison and reproducibility. They are not imported by the
application.
