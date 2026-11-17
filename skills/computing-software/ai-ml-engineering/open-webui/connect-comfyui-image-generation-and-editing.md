---
id: computing-software.ai-ml-engineering.open-webui.connect-comfyui-image-generation-and-editing
name: connect-comfyui-image-generation-and-editing
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, image-generation, comfyui, workflow, node-mapping]
level: advanced
status: docs-checked
description: "Connect ComfyUI to Open WebUI for image generation and editing: listen flag, API-format workflow export, node ID mapping and common validation errors."
sources:
  - https://docs.openwebui.com/features/chat-conversations/image-generation-and-editing/comfyui
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Connect ComfyUI for image generation and editing

Goal: Open WebUI generates and edits images by posting your own ComfyUI API workflow (community guide).

## Network
- Start ComfyUI with `--listen` (binds 0.0.0.0; UI on port 8188). Open the port in the host firewall if needed (`sudo ufw allow 8188/tcp`).
- Open WebUI in Docker on native Linux needs `--add-host=host.docker.internal:host-gateway`, plus `-e COMFYUI_BASE_URL=http://host.docker.internal:8188/` and `-e ENABLE_IMAGE_GENERATION=True`.
- SwarmUI as backend: Base URL `http://<swarmui-host>:7801/ComfyBackendDirect`, with SwarmUI LAN access on.

## Generation (Settings > Admin > Images)
1. Turn Image Generation on; under Create Image set the engine to `ComfyUI`; choose Model, Image Size, Steps.
2. Base URL then click the refresh icon to test the connection; add an API Key if required.
3. In ComfyUI: Settings > turn on "Dev Mode", load the generation workflow, File menu > **Export (API)**. Upload that JSON in Open WebUI under ComfyUI Workflow.
4. Map nodes: each row is Key (input name in the node `inputs` block) plus Node Ids (comma-separated). Generation defaults: Prompt `text` (required), Model `ckpt_name`, Width `width`, Height `height`, Steps `steps`, Seed `seed`. Only the prompt node ID is strictly required. Look up IDs as the top-level keys of the exported JSON. Change a key if needed, e.g. `seed` to `noise_seed`; Flux-style workflows may need several comma-separated IDs (the page's examples are `1, 2` and, for a seed applied to several samplers, `3, 15, 22`).
5. Save. Outputs from Save Image, Save Image (Advanced), Save Animated WEBP/PNG and Preview Image nodes are returned; animated stays animated.

## Editing
Same page, **Edit Image** section: switch **Image Edit** on (off by default), engine `ComfyUI`, its OWN Base URL and API Key (no fallback to generation settings), and a separate edit workflow. Edit defaults: Image `image` and Prompt `prompt` (both required), Model `unet_name`, Width, Height. No negative prompt, steps, seed or batch size.

## Gotchas
- `Value not in list: ckpt_name` means the model name sent is not valid for that node type (for example a VAE sent to a checkpoint loader).
- `Missing input <key>` means a required input was not mapped; hardcode it in the workflow or map it.
- Image Prompt Generation toggle (Admin > Images) only affects Legacy function calling; in Native mode the model writes the prompt itself.
- There is no per-message Generate Image button: switch Image on in the chat Integrations menu and ask for the image.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/chat-conversations/image-generation-and-editing/comfyui (read in full): --listen, ufw port 8188, the docker run flags and env vars, SwarmUI Base URL, admin Images steps, Dev Mode and Export (API), the generation and edit default keys and required fields, supported output nodes, separate edit Base URL and API Key, the two error strings, Image Prompt Generation being Legacy-only, and the missing Generate Image button. Corrected: the multiple-ID example attribution.
Method: documentation only; no commands were run.
