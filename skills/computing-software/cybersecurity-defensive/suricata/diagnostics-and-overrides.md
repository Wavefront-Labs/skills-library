---
id: computing-software.cybersecurity-defensive.suricata.diagnostics-and-overrides
name: diagnostics-and-overrides
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [set-option, dump-config, build-info, list-keywords, engine-analysis]
level: practitioner
status: docs-checked
description: "Inspect and override Suricata at the command line: --set, --dump-config, --build-info, --dump-features, --list-keywords, --list-app-layer-protos and --disable-hashing."
sources: ["https://docs.suricata.io/en/latest/command-line-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Diagnostics and overrides

- `--set <key>=<value>`: override one config value, for example `--set default-log-dir=/path/to/dir`. It can change existing list entries by index but cannot add new ones, for example `--set outputs.1.eve-log.enabled=no`. Indexes shift when the YAML changes, so check `--dump-config` first.
- `--dump-config`: print the loaded configuration and exit.
- `--build-info`: show how this binary was built.
- `--dump-features`: list features provided, to compare against rule `requires`.
- `--list-keywords=[all|json|csv|<kword>]`: supported rule keywords.
- `--list-app-layer-protos`, `--list-runmodes`: supported protocols and runmodes.
- `--engine-analysis`: print reports selected by the `engine-analysis` config parameter, then exit.
- `--disable-detection`: turn off the detection engine.
- `--disable-hashing`: disables md5, sha1 and sha256, and with them filestore, JA3 and hash keywords.
- `--plugin <path>`: load a plugin; a directory loads every `.so` in it.

## Checked

2026-11-04. Every option above confirmed against the Suricata Command Line Options page.

Method: documentation only; no commands were run.
