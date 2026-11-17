---
id: computing-software.ai-ml-engineering.llama-cpp.server-web-ui-flags
name: server-web-ui-flags
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, web-ui, ui-config, no-ui, api-prefix]
level: intro
status: docs-checked
description: "Serve, hide or configure the llama-server web UI with --ui, --ui-config and --api-prefix."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Web UI options

The web UI is served at the server root, for example `http://127.0.0.1:9931`.

- `--ui` / `--no-ui` (aliases `--webui` / `--no-webui`): enable or disable the Web UI. Default enabled.
- `--ui-config JSON`: JSON that overrides default UI settings.
- `--ui-config-file FNAME`: the same, read from a file.
- `--ui-mcp-proxy`: let the UI reach remote MCP servers via the server (experimental; do not use in untrusted environments).
- `--api-prefix PREFIX`: prefix path the server serves from, without the trailing slash.
- `--path PATH`: path to serve static files from.

Example:

```bash
llama-server -m /path/to/model.gguf --ui-config '{"pasteLongTextToFileLen": 0, "renderUserContentAsMarkdown": true}'
```

When tools or MCP servers are configured, the UI lists them (`<server>_<tool>` names). The README points to settings-keys.ts for the available preferences, and notes that the old flags `--webui-config` and `--webui-config-file` are deprecated but still work as aliases.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: --ui, --ui-config, --ui-config-file, --ui-mcp-proxy, --api-prefix, --path, the default address, the README's ui-config example and the deprecated aliases. Removed: the claim that the UI uses the API key, the reverse-proxy example and the sentence that --no-ui leaves only the API (not stated).

Method: docs-only read of cited pages, 2026-11-08
