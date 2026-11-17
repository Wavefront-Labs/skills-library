---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-fmt-validate
name: grafana-alloy-fmt-validate
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [alloy-fmt, alloy-validate, fmt-test, fmt-write, exit-codes, config-validation]
level: intro
status: docs-checked
description: "Format and validate Alloy configs with alloy fmt (--write, --test) and alloy validate, and what validation does and does not check."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/cli/fmt.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/cli/validate.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# alloy fmt and alloy validate

## fmt
```shell
alloy fmt [--write|--test] /path/to/config.alloy
```
With no file or `-`, it reads standard input. `--write` / `-w` rewrites the file (not allowed with stdin, and skipped if nothing changes). `--test` / `-t` writes nothing and exits non-zero if the file would change, which fits CI. The two flags are mutually exclusive. It fails on syntax errors but does not check that components are configured properly.

## validate
```shell
alloy validate /path/to/config.alloy
```
Accepts a file or a directory (`*.alloy`, nested directories ignored). Valid gives exit code zero; invalid gives non-zero with diagnostics on stderr.

Flags: `--config.format`, `--config.bypass-conversion-errors`, `--config.extra-args`, `--stability.level`, `--feature.community-components.enabled`. Set `--stability.level` and `--feature.community-components.enabled` to the same values you use at run time.

Checks performed: syntax errors, missing components, component name conflicts, required properties, unknown properties, `foreach` blocks and `declare` blocks. The page calls validation limited in scope: it checks only that list.

## Checked

2026-11-08. Read the fmt and validate CLI reference pages in full. Confirmed: usage, stdin behaviour, `--write` and `--test` (short forms, mutual exclusion, stdin restriction, no-op write), what fmt does not validate, validate path handling, exit codes and stderr diagnostics, the five flags, the note to match stability and community flags to run time, and the list of checks. Removed the unconfirmed claim about unreachable endpoints and the claim about what failure results from mismatched flags.

Method: documentation only; no commands were run.
