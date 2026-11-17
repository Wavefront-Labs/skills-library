---
id: computing-software.ai-ml-engineering.llama-cpp.server-tools-and-mcp
name: server-tools-and-mcp
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, builtin-tools, mcp-servers, agent-mode, security]
level: advanced
status: docs-checked
description: "Enable experimental built-in tools and MCP stdio servers in llama-server and understand the security limits."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server tools and MCP servers

Both features are experimental; do not enable them in untrusted environments.

**Built-in tools:** `--tools all` or a comma-separated list. Available: `read_file`, `file_glob_search`, `grep_search`, `exec_shell_command`, `write_file`, `edit_file`, `get_info`. `--tools-runtime` can run them in `docker:`, `podman:`, `docker-container:`, `podman-container:` or `ssh:` environments instead of the host.

**MCP servers:** only the stdio transport is supported. Declare servers in a Cursor-compatible JSON file:

```json
{ "mcpServers": { "example": { "command": "/path/to/server", "args": [] } } }
```

```bash
llama-server -m /path/to/model.gguf --mcp-servers-config mcp.json
```

Or inline with `--mcp-servers-json`. Entry keys: `command` (required), `args`, `env` (merged over parent environment), `cwd`, `timeout_ms` (per tool call, default 30000). Each server is started once to list its tools, stopped, and respawned when a tool is called. Tools are named `<server>_<tool>` and appear in the Web UI and `GET /tools`; colliding names are skipped. MCP works independently of `--tools`.

`--agent` enables the CORS proxy and all built-in tools; `--ui-mcp-proxy` only lets the Web UI reach remote MCP servers.

The child process has the server's privileges. These options also limit `--cors-origins` to localhost by default. The README says the `/tools` REST API is intended for internal use by the Web UI, may change or be removed, and must not be used in a downstream application.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: --tools and its tool names, --tools-runtime options, stdio-only MCP, the JSON file shape, entry keys and the 30000 ms default, spawn and respawn behaviour, tool naming and collisions, --agent, --ui-mcp-proxy, the CORS localhost default and the privilege warning. Reworded: the /tools API note.

Method: docs-only read of cited pages, 2026-11-08
