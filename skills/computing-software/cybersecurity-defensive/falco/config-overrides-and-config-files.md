---
id: computing-software.cybersecurity-defensive.falco.config-overrides-and-config-files
name: config-overrides-and-config-files
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [config-files, config-d, merge-strategy, option-override, falco-yaml]
level: advanced
status: docs-checked
description: "Override falco.yaml with -o, list indexes and append syntax, and layer extra files with config_files and merge strategies."
sources:
  - https://falco.org/docs/reference/daemon/config-options/
  - https://falco.org/docs/reference/daemon/cli-arguments/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The configuration file is `/etc/falco/falco.yaml`, or a configmap on Kubernetes. Select another file with `-c <path>`.

Command line override: `-o key=value` or `--option`. For nested keys use `-o key.subkey=value`. For lists, address by index, `-o key.subkey[0]=value`, and since Falco 0.38.0 append with `-o key.subkey[]=value`. Escape literal dots or brackets with a backslash.

Since 0.38.0 `config_files` loads more files after the main one; files and directories are accepted, and the default is `/etc/falco/config.d`. Since 0.41.0 each entry may carry a merge strategy (default `append`; files in a directory load in lexicographical order):

```yaml
config_files:
  - /etc/falco/config.d
  - path: /etc/falco/config.append.d/
    strategy: append
  - path: /etc/falco/extra_config.yaml
    strategy: add-only
```

- `append`: sequence keys are appended, scalars overridden, new keys added.
- `override`: existing keys overridden, new keys added.
- `add-only`: existing keys ignored, new keys added.

Gotcha: merging happens only at the root key. If a file in `config.d` sets any `engine:` key, the whole `engine:` section from `falco.yaml` is replaced, so edits to `engine.buf_size_preset` in `falco.yaml` are ignored. Edit the file in `config.d` instead, or remove it.

## Checked

2026-11-08. Read in full: the Falco Configuration Options page (raw markdown `docs/content/en/docs/reference/daemon/config-options/index.md`) and the daemon arguments list (`-c`, `-o` escape rule). Confirmed the override syntax, the 0.38.0 and 0.41.0 version gates, the three strategies and the root-key merging warning.

Method: documentation only; no commands were run.
