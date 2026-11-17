---
id: computing-software.devops-ci-cd.release-engineering.testing-config-with-conftest
name: testing-config-with-conftest
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, conftest, environment-configuration, policy-as-code]
level: practitioner
status: docs-checked
description: "Test configuration files (Kubernetes YAML, Helm output, Terraform plans, Dockerfiles) against Rego policies with conftest in CI before they reach any environment."
sources: ["https://www.conftest.dev/", "https://www.openpolicyagent.org/docs/policy-language"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing config with conftest

conftest runs OPA Rego policies against structured config: YAML, JSON, HCL, Dockerfile, INI, TOML.

## Policy
```rego
# policy/deployment.rego
package main
import rego.v1

deny contains msg if {
  input.kind == "Deployment"
  some c in input.spec.template.spec.containers
  not c.resources.limits.memory
  msg := sprintf("container %s has no memory limit", [c.name])
}
warn contains msg if {
  input.kind == "Deployment"
  input.spec.replicas < 2
  msg := "fewer than 2 replicas"
}
```

## Run
```bash
# render first (Helm, Kustomize), write the output to a file, then:
conftest test rendered/prod.yaml
conftest test Dockerfile --namespace docker
conftest test plan.json --namespace terraform     # plan exported as JSON
conftest verify            # runs policy unit tests (*_test.rego)
```
Conftest looks for `deny`, `violation` and `warn` rules (optionally suffixed, for example `deny_myrule`); see the conftest docs for how each affects the exit code.

## Practices
- Keep policies in a shared repo and distribute them (see conftest's policy sharing docs) so all teams use the same versions.
- Write policy tests (`test_*` rules) and run `conftest verify` in the policy repo's CI.
- Render per environment: prod overlays often break rules that dev passes.
- Pair with cluster admission control; conftest gives earlier feedback.

## Verify
- [ ] A manifest without memory limits fails CI with the policy message; `conftest verify` passes.

## Checked

2026-10-28. Confirmed against conftest.dev: deny, violation and warn rules with optional suffix, supported formats (Dockerfile, HCL, INI, TOML among them), the --namespace flag, conftest verify with tests in a *_test.rego file by convention, deny contains msg if syntax; OPA policy language page for Rego. Removed: --fail-on-warn, conftest pull, stdin invocation, exit-code claims, and the Helm, Kustomize and Terraform commands (not conftest commands; outside this lane).

Method: documentation only; no commands were run.
