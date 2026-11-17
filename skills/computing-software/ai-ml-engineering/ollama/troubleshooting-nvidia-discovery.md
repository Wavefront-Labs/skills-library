---
id: computing-software.ai-ml-engineering.ollama.troubleshooting-nvidia-discovery
name: troubleshooting-nvidia-discovery
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [nvidia-discovery, cuda-error-level, nvidia-modprobe, uvm]
level: advanced
status: docs-checked
description: "Debug Linux NVIDIA GPU discovery errors (codes 3, 46, 100, 999) with driver, container, uvm and dmesg checks."
sources:
  - https://docs.ollama.com/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: recover a GPU that Ollama cannot initialize.

At startup Ollama inventories GPUs. Initialization failures show in the server log as codes such as 3 (not initialized), 46 (device unavailable), 100 (no device) or 999 (unknown). The page lists techniques to try:

- If you use a container, set up the container runtime first (Docker page) and verify it works: `docker run --gpus all ubuntu nvidia-smi`. If this fails, Ollama cannot see the GPU.
- Check whether the uvm driver is loaded with `sudo nvidia-modprobe -u`, or reload it with `sudo rmmod nvidia_uvm` then `sudo modprobe nvidia_uvm`.
- Try rebooting.
- Make sure the latest NVIDIA drivers are installed; the page says that in general the latest driver gives the best results.
- Set `CUDA_ERROR_LEVEL=50` to get more diagnostic logs.
- Check kernel messages with `sudo dmesg | grep -i nvrm` and `sudo dmesg | grep -i nvidia`.

If none of these resolve it, the page says to gather this information and file an issue.

For Docker setups where the GPU works at first and then drops to CPU with GPU discovery failures in the server log, the page says to disable systemd cgroup management: add `"exec-opts": ["native.cgroupdriver=cgroupfs"]` to `/etc/docker/daemon.json` on the host.

## Checked

2026-11-08. Error codes, the six checks, the file-an-issue advice and the cgroup driver fix against the troubleshooting page (docs.ollama.com/troubleshooting). Removed "restart Docker" after the daemon.json change (the page does not say it) and reworded `nvidia-modprobe -u` and the reboot step to match the page's wording.

Method: documentation only; no commands were run.
