---
id: computing-software.ai-ml-engineering.llm-application-engineering.code-execution-sandboxes-for-agents
name: code-execution-sandboxes-for-agents
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, agents, code-execution-sandbox, gvisor, firecracker, container-isolation, code-execution-tool]
level: practitioner
status: docs-checked
description: "Run model-generated code safely: Claude server-side code execution or self-hosted sandboxes (gVisor, Firecracker, locked-down containers) with limits and no egress."
sources:
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/code-execution-tool
  - https://gvisor.dev/docs/
  - https://firecracker-microvm.github.io/
  - https://docs.docker.com/engine/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Code execution sandboxes for agents

Model-written code is untrusted code - it may be wrong, destructive or steered by injected content. Run it where the worst case is losing the sandbox.

## Option 1: hosted execution
Claude's code execution tool runs in Anthropic-managed containers:
```python
resp = client.messages.create(model="claude-opus-5-5", max_tokens=16000,
    tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
    messages=[{"role": "user", "content": "Analyse sales.csv and plot monthly revenue."}])
```
Results come back as `bash_code_execution_tool_result` blocks (stdout, stderr, return_code); files are exchanged via the Files API. No infrastructure to run, but the environment and network are fixed by the provider. Other hosted options: E2B, Modal, Daytona, cloud notebook sandboxes.

## Option 2: self-hosted
Isolation strength, weakest to strongest: plain container < container + gVisor (user-space kernel) < microVM (Firecracker/Kata) < separate VM/host.
```bash
docker run --rm --runtime=runsc \
  --network none --read-only --tmpfs /tmp:rw,size=256m \
  --memory 1g --cpus 1 --pids-limit 128 \
  --cap-drop ALL --security-opt no-new-privileges --user 65534:65534 \
  -v "$JOB_DIR":/work:rw -w /work sandbox-python:3.12 timeout 60 python main.py
```
- `--network none` or an egress proxy with an allowlist (package index mirror only); open internet enables exfiltration and abuse.
- No credentials, cloud metadata endpoint access (block it at the network layer) or Docker socket inside.
- CPU/memory/pid/disk/time limits stop fork bombs and runaway loops.
- Fresh sandbox per task or per session; destroy afterwards. Persistent sandboxes accumulate state an attacker can use.
- Pre-build images with common libraries; installing packages at runtime needs network and adds supply-chain risk.

## Wiring into the agent loop
- Return stdout/stderr truncated to a budget with an exit code; errors go back as tool results so the model can fix its code.
- Treat output files as untrusted when they flow to other systems (sanitize before rendering HTML, scanning before sharing).
- Log code and outputs for audit.

## Verify
- [ ] Escape tests: reading host files, reaching the metadata endpoint, opening outbound sockets, fork bomb - all fail.
- [ ] Timeouts and memory limits enforced (test scripts exceed them and are killed).
- [ ] Sandbox destroyed after each task (no leftover containers/volumes).

## Checked

2026-11-02. Checked against the Claude code execution tool page (tool type code_execution_20260521, bash_code_execution_tool_result with stdout, stderr, return_code, Files API, containers with no internet access, model id), the Docker docker container run reference (--network, --read-only, --tmpfs, --memory, --cpus, --pids-limit, --cap-drop, no-new-privileges, --user, --runtime, -w), the gVisor Docker quick start (runsc runtime) and the Firecracker and gVisor home pages (microVM and user-space kernel isolation). Removed the 169.254.169.254 address (cloud metadata endpoint is named generally instead) because no fetched page states it.

Method: documentation only; no commands were run.
