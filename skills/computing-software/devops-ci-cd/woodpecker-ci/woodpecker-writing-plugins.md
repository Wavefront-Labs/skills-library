---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-writing-plugins
name: woodpecker-writing-plugins
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [plugin-authoring, plugin-env, docker-entrypoint]
level: advanced
status: docs-checked
description: "Write a Woodpecker plugin: image entrypoint, PLUGIN_ settings and output groups."
sources: ["https://woodpecker-ci.org/docs/usage/plugins/creating-plugins"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing a Woodpecker plugin

A plugin is a Docker image whose ENTRYPOINT runs your logic. Users configure it with `settings`, which arrive as uppercase environment variables with a `PLUGIN_` prefix. `url` becomes `PLUGIN_URL`; `-` becomes `_`, so `some_String` gives `PLUGIN_SOME_STRING`. CamelCase is not respected: `anInt` gives `PLUGIN_ANINT`.

Scalars become strings (`some-bool: false` gives `PLUGIN_SOME_BOOL="false"`). Complex values become JSON: a map `complex: {abc: 2, list: [2, 3]}` arrives in `PLUGIN_COMPLEX` as `{"abc": "2", "list": ["2", "3"]}`.

```bash
#!/bin/sh
echo "▶  curl -X ${PLUGIN_METHOD} ${PLUGIN_URL}"
curl -X ${PLUGIN_METHOD} -d ${PLUGIN_BODY} ${PLUGIN_URL}
```

Test locally by running the image with `-e PLUGIN_METHOD=post -e PLUGIN_URL=...`.

Output groups: print a line starting with `▶` followed by two ASCII spaces and a non-empty title to start a collapsible group in the UI. Groups are flat, with no end markers.

Best practices: build for `amd64` and `arm64`, provide binaries for the local backend, use built-in env vars, accept configuration only through settings (do not require `environment` or specific secret names), and add a `docs.md` with metadata (`name` is required) to be listed in the plugin index. Libraries exist for Go, TypeScript and Rust.

## Checked

2026-11-03. Read the Woodpecker creating plugins page and confirmed PLUGIN_ prefix and name conversion, string conversion of scalars, JSON for complex settings, the output group marker with two spaces, best practices, docs.md metadata with only name required, and the Go, TypeScript and Rust libraries. Nothing removed. 

Method: documentation only; no commands were run.
