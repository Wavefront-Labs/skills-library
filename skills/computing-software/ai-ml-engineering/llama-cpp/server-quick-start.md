---
id: computing-software.ai-ml-engineering.llama-cpp.server-quick-start
name: server-quick-start
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, llama-server, quick-start, health-check]
level: intro
status: docs-checked
description: "Start llama-server, its default listen address and port, the health endpoint and a first curl request."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Starting llama-server

`llama-server` is the HTTP server in llama.cpp. It is built with the rest of the project, or as a single target.

```bash
cmake -B build
cmake --build build --config Release -t llama-server
./build/bin/llama-server -m /path/to/model.gguf -c 2048
```

Defaults per the server README:

- Listens on `127.0.0.1` at port `9931` (`--host`, `--port`). The web UI is served at the same URL.
- `-c 0` (the default) takes the context size from the model.
- `--timeout` (server read/write timeout) defaults to 3600 seconds.

First request:

```bash
curl --request POST --url http://localhost:9931/completion \
  --header "Content-Type: application/json" \
  --data '{"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}'
```

`GET /health` is public (no API key check) and `/v1/health` also works. While the model is loading it returns HTTP 503 with `{"error": {"code": 503, "message": "Loading model", "type": "unavailable_error"}}`. Once ready it returns HTTP 200 with `{"status": "ok"}`.

Docker form: `docker run -p 8080:8080 -v /path/to/models:/models ghcr.io/ggml-org/llama.cpp:server -m models/7B/ggml-model.gguf -c 512 --host 0.0.0.0 --port 8080`. The CUDA image is `server-cuda`, run with `--gpus all` and `--n-gpu-layers 99`.

To build with HTTPS support use `-DLLAMA_OPENSSL=ON` (OpenSSL 3).

## Checked

2026-11-08. Confirmed in the llama.cpp server README: build commands, default listen address 127.0.0.1 and port 9931, -c 0 default, --timeout default 3600, the curl example, /health behaviour and bodies, the Docker commands and the OpenSSL build flag. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
