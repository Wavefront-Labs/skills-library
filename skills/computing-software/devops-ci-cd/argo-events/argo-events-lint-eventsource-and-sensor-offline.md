---
id: computing-software.devops-ci-cd.argo-events.argo-events-lint-eventsource-and-sensor-offline
name: argo-events-lint-eventsource-and-sensor-offline
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, argo-events-lint, ci, validation, strict, recursive, pre-commit]
level: practitioner
status: docs-checked
description: "Validate EventSource and Sensor manifests offline with argo-events lint, including recursive, strict and CI usage and its limits."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/lint.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events lint eventsource and sensor offline

`argo-events lint` is built into the argo-events binary (`make build`, then `./dist/argo-events lint --help`) and runs the same validation the controllers perform, without a cluster: EventSource config and required fields, Sensor dependencies, triggers and trigger templates, and schema conformance.

```bash
argo-events lint event-source.yaml sensor.yaml
argo-events lint examples/event-sources/
argo-events lint -R examples/          # recurse into subdirectories
argo-events lint --strict sensor.yaml  # fail on warnings too
```

Exit code 0 means everything is valid, 1 means at least one validation error, so it fits CI jobs and pre-commit hooks (for example a `.git/hooks/pre-commit` that lints staged `.yaml` and `.yml` files). Multi-document YAML separated by `---` is validated per document ("document 1", "document 2").

Typical errors: `endpoint can't be empty` (EventSource) and `no triggers found` (Sensor). Linting a Sensor offline yields a warning `Sensor validation incomplete (EventBus not available)` / `nil eventbus`, because a dummy EventBus is used; this is expected.

Limits: only `.yaml` and `.yml` files containing EventSource or Sensor kinds are processed, and referenced service accounts, secrets and workflow templates are not validated. If nothing prints, check the file has valid YAML and the right `kind`.

## Checked

2026-11-04. Confirmed against the Linting EventSource and Sensor Resources page: build and `--help` usage, the commands and `-R`/`--strict` flags, exit codes 0 and 1, the pre-commit hook, multi-document YAML output, the two error messages, the EventBus warning with the dummy EventBus, ignored files, limitations and the no-output checklist. Nothing removed.
Method: documentation only; no commands were run.
