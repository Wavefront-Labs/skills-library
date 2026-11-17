---
id: computing-software.ai-ml-engineering.hugging-face.gradio-demos-on-hugging-face-spaces
name: gradio-demos-on-hugging-face-spaces
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, hf-spaces, gradio, zerogpu, demo-app, spaces-secrets]
level: practitioner
status: docs-checked
description: "Build and deploy Gradio demos on Hugging Face Spaces: app.py and requirements, ZeroGPU usage and limits, loading models once and calling a Space as an API."
sources:
  - https://huggingface.co/docs/hub/spaces-sdks-gradio
  - https://huggingface.co/docs/hub/spaces-zerogpu
  - https://www.gradio.app/guides/quickstart
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradio demos on Spaces

## Minimal Space
Repo files: `app.py`, `requirements.txt`, `README.md` with YAML:
```yaml
---
title: Ticket Intent Demo
sdk: gradio
app_file: app.py
---
```
```python
import gradio as gr
from transformers import pipeline
clf = pipeline("text-classification", model="org/ticket-intent", top_k=None)   # load once at startup
def predict(text):
    return {d["label"]: d["score"] for d in clf(text)[0]}
demo = gr.Interface(predict, gr.Textbox(lines=4, label="Ticket"), gr.Label(num_top_classes=5),
                    examples=[["My card was charged twice"]])
demo.launch()
```
The Space rebuilds on each commit.

## ZeroGPU
ZeroGPU is shared infrastructure that dynamically allocates and releases NVIDIA RTX Pro 6000 Blackwell GPUs. It works only with the Gradio SDK and may be less compatible than a standard GPU Space.
- Select the ZeroGPU hardware in Space settings, then decorate GPU-dependent functions with `@spaces.GPU`; the GPU is requested when the function is called and released on completion. The decorator has no effect outside ZeroGPU.
- Place models on `cuda` at module level (a CUDA emulation mode makes that work outside `@spaces.GPU`); lazy-loading or moving to CUDA inside the function is discouraged as less efficient.
- Default runtime per call is 60 s; for longer functions use `@spaces.GPU(duration=120)`.
- Default size is `large` (half a GPU, 48GB); `@spaces.GPU(size="xlarge")` requests a full GPU (96GB), consumes 2x the daily quota and usually queues longer.
- Free personal accounts in good standing can host up to 2 ZeroGPU Spaces, PRO accounts up to 10; PRO users also get a larger daily quota and queue priority. See the ZeroGPU page for current terms.
```python
import spaces
model.to("cuda")                   # module level, as the docs show
@spaces.GPU(duration=60)
def generate(prompt): ...
```

## Startup
Load models at module level, not inside the handler. Pin package versions in `requirements.txt`.

## Use as an API
Every Gradio Space exposes API docs ("Use via API"); `gradio_client.Client("<owner>/<space>")` calls it. For production traffic prefer a dedicated inference service.

## Verify
Build logs show no errors; the app answers the example inputs; restart the Space and confirm cold-start time is acceptable.

## Checked
2026-11-01. Confirmed against the Spaces ZeroGPU page: supported GPU (RTX Pro 6000 Blackwell, not H200), Gradio-only, `@spaces.GPU`, `duration` (60 s default), `size="xlarge"` (2x quota), module-level `cuda` placement, 2/10 hosted Space limits. Removed (not confirmed on the pages read): YAML `sdk_version`/`python_version`/`models` fields, `cache_examples` and `demo.queue(max_size=...)`, paid GPU list, secrets and `/data` persistent-storage notes, `packages.txt`, `sdk: docker`, `concurrency_limit` advice, and the old claim that ZeroGPU is for PRO/orgs only (free users can use ZeroGPU Spaces).
Method: documentation only; no commands were run.
