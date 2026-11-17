---
id: computing-software.devops-ci-cd.dagger.checks-run-filter
name: checks-run-filter
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, checks, dagger-check, glob, ci, toolchain, validation]
level: practitioner
status: docs-checked
description: "Run, list and filter Dagger checks with dagger check, including glob patterns, toolchain namespaces and ignoring checks, locally and in CI."
sources: [https://docs.dagger.io/0.21/introduction/core-concepts/checks, https://docs.dagger.io/0.21/introduction/core-concepts/, https://docs.dagger.io/0.21/introduction/core-concepts/toolchains]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run and filter Dagger checks

Goal: validate a repo with `dagger check` locally and in CI (Dagger 0.21 docs).

A check is a Dagger Function that validates code without requiring arguments, so it can run locally, in CI, from a coding agent or before deploy.

## Commands

```shell
dagger check            # run all checks concurrently
dagger check -l         # list available checks
dagger check lint-*     # glob filter
dagger check security-scan
```
Checks run in parallel; the command exits non-zero if any fails, so CI needs only a step such as:
```yaml
- name: Run checks
  run: dagger check
```
Multiple patterns: a check matching any pattern runs.

## Toolchain checks

Installed toolchains contribute checks, namespaced by toolchain name (`black:format`, `pytest:test`, `security-scanner:scan` in the docs example):
```shell
dagger toolchain install github.com/example/pytest
dagger check pytest:*
dagger check security-scanner:scan
```
(The toolchains page quotes the glob as `dagger check 'pytest:*'`.)

## Ignore checks from a toolchain

In `dagger.json`, under the toolchain entry:
```json
"ignoreChecks": ["dependency-scan", "container-*"]
```
Patterns are scoped to that toolchain, so omit the toolchain prefix. Use for gradual adoption, environment-specific checks or experiments; `dagger check -l` shows what remains.

Related: `computing-software.devops-ci-cd.dagger.checks-create`, `computing-software.devops-ci-cd.dagger.toolchain-install-use`.

## Checked

2026-11-07

Read in full from the docs source: introduction/core-concepts/checks.mdx and toolchains.mdx. Confirmed the commands, glob and multiple-pattern behavior, the toolchain namespacing, the quoted 'pytest:*' form on the toolchains page, the ignoreChecks example and its scoping, and the gradual-adoption note. The toolchains page was added to sources because the ignoreChecks use cases and dagger check -l follow-up appear there.

Method: documentation only; no commands were run.
