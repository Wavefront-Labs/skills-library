---
id: computing-software.cloud-infrastructure-engineering.kyverno.cli-test
name: cli-test
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [kyverno-test, cli-test, kyverno-test-yaml, test-case-selector, junit-output, policy-ci]
level: practitioner
status: docs-checked
description: "Run kyverno test against folders or git repos holding kyverno-test.yaml: flags, test-case-selector, output formats, and the CI pattern."
sources:
  - https://kyverno.io/docs/kyverno-cli/reference/kyverno_test/
  - https://kyverno.io/docs/guides/testing-policies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Usage: `kyverno test [local folder or git repository]... [flags]`. Each target needs a test manifest, `kyverno-test.yaml` by default (change with `-f`/`--file-name`). The manifest declares expected results, and the command compares them with the actual results; a mismatch fails the test. The pages read do not document the manifest schema.

Flags:
- `--detailed-results`; `--fail-only` (show only failures).
- `-b`/`--git-branch` for a git source.
- `-o`/`--output-format`: `json`, `yaml`, `markdown` or `junit`.
- `--registry`: local Docker credentials to reach registries for external data.
- `--remove-color`.
- `--require-tests`: error if no tests are found, catching folders that silently run nothing.
- `-t`/`--test-case-selector`: comma-separated `policy=`, `rule=`, `resource=` pairs, default `policy=*,rule=*,resource=*`.
- `--warnings-as-errors`: deprecation warnings fail the run.

Examples: `kyverno test .`; `kyverno test https://github.com/kyverno/policies/pod-security --git-branch main`; `kyverno test . --test-case-selector "policy=disallow-latest-tag, rule=require-image-tag, resource=test-require-image-tag-pass"`.

CI pattern from the guide: install the CLI (`kyverno/action-install-cli@v0.2.0`, `release: 'v1.11.0'`; changing the release simulates a Kyverno upgrade), run `kyverno test tests/` for predefined cases and `kyverno apply policies/ -r resources/` for unknown resources. Any failing step halts the pipeline. Sample policies and tests live in github.com/kyverno/policies, one folder per case with `kyverno-test.yaml`, a policy file and a resource file.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
