---
id: computing-software.web-development.biome.daemon-json-rpc-methods-overview
name: daemon-json-rpc-methods-overview
category: computing-software
field: web-development
product: biome
tags: [biome, daemon, json-rpc, biome-open-project, biome-scan-project, biome-open-file, biome-change-file, biome-update-settings, third-party-clients, editor-integration]
level: sme
status: docs-checked
description: "The Biome daemon's JSON-RPC protocol: request shape, the project and file lifecycle methods, and the warning that methods are outside semver."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/daemon.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The daemon speaks JSON-RPC 2.0 so third-party clients (editor extensions) can drive it. A request carries `jsonrpc: "2.0"`, an `id`, a `method` and `params`:

```json
{ "jsonrpc": "2.0", "id": 1, "method": "biome/open_project",
  "params": { "path": "/Some/path", "openUninitialized": false } }
```

**Caution:** these methods are not part of the semantic versioning contract and may change without notice.

Lifecycle methods read in full:
- `biome/open_project` takes `{ path, openUninitialized }` (open even when no `biome.json` is found) and returns a `projectKey` (unique project identifier).
- `biome/update_settings` takes `{ projectKey, configuration, extendedConfigurations?, moduleGraphResolutionKind?, workspaceDirectory? }` and returns diagnostics.
- `biome/scan_project` takes `{ projectKey, scanKind, force, watch, verbose? }` (force rescans an already watched folder; watch asks the watcher to watch the path) and returns child configuration files found, diagnostics and the scan duration.
- `biome/open_file` takes `{ path, projectKey, content, documentFileSource?, editorFeatures?, inlineConfig?, persistNodeCache? }`; set `persistNodeCache` only if reparsing is expected, such as via the LSP proxy.
- `biome/change_file` takes `{ path, projectKey, content, version, ... }` and returns diagnostics about dependency and module data, not lint or parse results.
- `biome/close_file`, `biome/file_exists` (`filePath` to boolean), `biome/is_path_ignored` (`path`, `projectKey`, `features` so formatter or linter includes are checked, `ignoreKind`, `isDir`), `biome/file_features` (which features a path supports) and `biome/update_module_graph`.

The page also lists these introspection and processing methods by name: `get_syntax_tree`, `check_file_size`, `get_file_content`, `get_control_flow_graph`, `get_formatter_ir`, `get_type_info`, `get_registered_types`, `get_semantic_model`, `get_module_graph`, `pull_diagnostics`, `process_file`, `pull_actions`, `pull_diagnostics_and_actions`, `format_file`, `format_range`, `format_on_type`, `fix_file`, `rename`, `parse_pattern`, `search_pattern`, `drop_pattern`.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: 'optional' on `features` and the 'in my read' hedge and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
