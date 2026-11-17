---
id: computing-software.ai-ml-engineering.ollama.troubleshooting-amd-discovery
name: troubleshooting-amd-discovery
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [amd-discovery, kfd, render-group, amd-log-level]
level: advanced
status: docs-checked
description: "Fix Linux AMD GPU discovery: /dev/kfd permissions, video and render groups, ROCm v7 drivers and multi-GPU issues."
sources:
  - https://docs.ollama.com/troubleshooting.md
  - https://docs.ollama.com/gpu.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a Radeon card recognised on Linux.

Typical symptoms are a GPU found by the OS but not used by Ollama, or a fall back to CPU.

Checks from the troubleshooting page:

- Permissions: AMD GPU access typically needs `video` and/or `render` group membership to open `/dev/kfd`; Ollama reports an error in the server log if permissions are wrong. In containers, run `ls -lnd /dev/kfd /dev/dri /dev/dri/*` on the host for the numeric group IDs and pass them with `--group-add`, along with `--device /dev/kfd --device /dev/dri`.
- Driver version: Ollama's ROCm 7 libraries need a compatible ROCm 7 kernel driver. With ROCm 6.x or earlier, GPU initialization times out after 30 seconds and Ollama falls back to CPU. The fix is to upgrade to ROCm v7 with the `amdgpu-install` utility from AMD's ROCm documentation.
- Logging: `AMD_LOG_LEVEL=3` enables info logging in the HIP/ROCm libraries, showing more detailed error codes; `OLLAMA_DEBUG=1` reports extra detail during discovery; `sudo dmesg | grep -i amdgpu` and `grep -i kfd` show driver errors.
- SELinux: `setsebool container_use_devices=1` allows containers to use device nodes.
- Unsupported cards: see `HSA_OVERRIDE_GFX_VERSION` in the AMD skill.

Gibberish output when a model loads across several AMD GPUs on Linux: the page links to AMD's multi-GPU known issues and limitations guide.

After upgrading the driver, reboot and restart Ollama. The failing-discovery log lines read `failure during GPU discovery` and `bootstrap discovery took duration=30s`.

## Checked

2026-11-03. Group membership for `/dev/kfd`, `ls -lnd` and `--group-add`, ROCm 7 driver mismatch with the 30s discovery log lines, `AMD_LOG_LEVEL=3`, `OLLAMA_DEBUG=1`, dmesg and multi-GPU note against the troubleshooting page (docs.ollama.com/troubleshooting); `setsebool` against the GPU page (docs.ollama.com/gpu). Nothing removed.

Method: documentation only; no commands were run.
