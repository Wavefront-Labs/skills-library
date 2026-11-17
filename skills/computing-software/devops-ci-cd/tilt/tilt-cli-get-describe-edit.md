---
id: computing-software.devops-ci-cd.tilt.tilt-cli-get-describe-edit
name: tilt-cli-get-describe-edit
category: computing-software
field: devops-ci-cd
product: tilt
tags: [cli-get-describe-edit, tilt, tilt-cli, api-objects]
level: practitioner
status: docs-checked
description: "Inspect and modify objects in a running Tilt session with tilt get, tilt describe and tilt edit: syntax, selectors, output formats and flags."
sources:
  - "https://docs.tilt.dev/cli/tilt_get.html"
  - "https://docs.tilt.dev/cli/tilt_describe.html"
  - "https://docs.tilt.dev/cli/tilt_edit.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tilt get, describe, edit

These commands talk to the Tilt HTTP server of a running session. When Tilt was started with a non-default address, pass `--host` (env `TILT_HOST`, default localhost) and `--port` (env `TILT_PORT`, default 10350).

## tilt get

Display one or many resources.

```
tilt get TYPE [NAME | -l label]
```

- `-o, --output`: json, yaml, kyaml, name, go-template, go-template-file, template, templatefile, jsonpath, jsonpath-as-json, jsonpath-file, custom-columns, custom-columns-file, wide.
- `-l, --selector` label query (supports `=`, `==`, `!=`, e.g. `-l key1=value1,key2=value2`); `--field-selector` field query.
- `-L, --label-columns`, `--show-labels`, `--show-kind`, `--no-headers`.
- `--sort-by` takes a JSONPath such as `{.metadata.name}` (integer or string field).
- `-w, --watch` lists then watches; `--watch-only` watches without listing first.
- `--ignore-not-found` returns exit code 0 when the object does not exist.
- `--show-managed-fields` keeps managedFields in JSON or YAML output.

## tilt describe

Show details of a resource or group of resources.

```
tilt describe (-f FILENAME | TYPE [NAME_PREFIX | -l label] | TYPE/NAME)
```

Options: `-f, --filename` (file, directory or URL), `-k, --kustomize` (cannot combine with `-f` or `-R`), `-R, --recursive`, `-l, --selector`.

## tilt edit

Edit a resource on the server.

```
tilt edit (RESOURCE/NAME | -f FILENAME)
```

Options: `-o, --output`, `--output-patch` (print the patch if edited), `--save-config`, `--field-manager` (default `kubectl-edit`), `--validate` (strict or true, warn, ignore or false; default strict), `--windows-line-endings`, `-f`, `-k`, `-R`, `--template`.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/cli/tilt_get.html, https://docs.tilt.dev/cli/tilt_describe.html, https://docs.tilt.dev/cli/tilt_edit.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
