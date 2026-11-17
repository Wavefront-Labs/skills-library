---
id: computing-software.cloud-infrastructure-engineering.kyverno.cli-apply
name: cli-apply
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [kyverno-apply, cli-apply, warn-exit-code, values-file, policy-report-cli, ci-policy-check]
level: practitioner
status: docs-checked
description: "Run kyverno apply to test policies against resource files, a cluster, JSON, Envoy or HTTP payloads, with exit-code, exception and output flags."
sources:
  - https://kyverno.io/docs/kyverno-cli/reference/kyverno_apply/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Usage: `kyverno apply <policy files|folders|git URL> [flags]`, for example `kyverno apply policy.yaml --resource res.yaml --set a=1,b=2`. A git URL source takes `--git-branch`/`-b`, `--username`, `--password`.

Inputs:
- Resources: `--resource`/`-r` per file (or a folder); `--cluster`/`-c` reads from the current kubeconfig cluster (`--context`, `--kubeconfig`, `-n` namespace, `--cluster-wide-resources`).
- Variables: `--set`/`-s k=v,...`, `--values-file`/`-f`, `--userinfo`/`-u` for roles, cluster roles and subjects.
- CEL and payloads: `--parameter-resource` for ValidatingAdmissionPolicy/MutatingAdmissionPolicy params, `--context-file`, `--json`, `--envoy-payload`, `--http-payload`, `--crd-path`.
- Mutate-existing targets: `--target-resource`, `--target-resources`.
- Loading: `--batch-size` (default 100), `--concurrent` (default 1), `--continue-on-error` (default true), `--show-performance`.

Behaviour flags:
- `--audit-warn`: report Audit-policy failures as warnings.
- `--continue-on-fail`: move to the next resource.
- `--warnings-as-errors`: deprecation warnings become errors.
- `--warn-exit-code <n>` sets the exit code for warnings (failures and errors still exit 1); `--warn-no-pass` raises it when no object satisfies a policy.

Exceptions: `--exception`/`-e`, `--exceptions-within-policies`, `--exceptions-with-resources`, `--generate-exceptions` (one exception per violation) with `--generated-exception-ttl` (default 720h).

Output: `--output`/`-o` writes mutated or generated resources to a file or directory, `--policy-report`/`-p`, `--output-format json|yaml` (default yaml), `--table`/`-t`, `--detailed-results`, `--remove-color`, `--registry` (uses local Docker credentials for external data), `--stdin`/`-i`.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/kyverno-cli/reference/kyverno_apply/.

Method: documentation only; no commands were run.
