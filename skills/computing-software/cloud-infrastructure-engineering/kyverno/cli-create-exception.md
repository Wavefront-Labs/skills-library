---
id: computing-software.cloud-infrastructure-engineering.kyverno.cli-create-exception
name: cli-create-exception
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [create-exception, kyverno-create, policy-rules-flag, exception-scaffold, cli-create]
level: intro
status: docs-checked
description: "Scaffold a Kyverno PolicyException file with kyverno create exception: name, namespace, policy-rules, any/all filters, background and output flags."
sources:
  - https://kyverno.io/docs/kyverno-cli/reference/kyverno_create_exception/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Usage: `kyverno create exception [name] [flags]` writes a PolicyException file.

Example: `kyverno create exception my-exception --namespace my-ns --policy-rules "policy,rule-1,rule-2" --any "kind=Pod,kind=Deployment,name=test-*"` creates `my-exception` in `my-ns` for the policy `policy`, rules `rule-1` and `rule-2`, matching Pods or Deployments named `test-*`.

Flags:
- `--policy-rules=policy,rule-1,rule-2,...`: policy name first, then rule names.
- `--any`: resource filters where any may match (`kind=Pod,kind=Deployment,name=test-*`).
- `--all`: filters that must all match.
- `--namespace`: namespace of the exception.
- `-b`/`--background`: default `true`; set `false` to exclude the policy from background scans.
- `-o`/`--output`: output path; console if unset.

Remember the exception only takes effect if the cluster has legacy PolicyExceptions enabled (`enablePolicyException`, `exceptionNamespace`). The generated resource targets the legacy `kyverno.io` exception form, which is deprecated in v1.19; check against the policy-exceptions skill for the CEL form.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
