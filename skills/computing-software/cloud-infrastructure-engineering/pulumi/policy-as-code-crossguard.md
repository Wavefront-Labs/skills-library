---
id: computing-software.cloud-infrastructure-engineering.pulumi.policy-as-code-crossguard
name: policy-as-code-crossguard
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, crossguard, policy-pack, pulumi-policy, policy-as-code]
level: practitioner
status: docs-checked
description: "Pulumi Policies (CrossGuard) model: policies, policy packs, PulumiPolicy.yaml, runtimes, running a pack locally with --policy-pack, and versioning."
sources:
  - https://www.pulumi.com/docs/iac/crossguard/
  - https://www.pulumi.com/docs/iac/crossguard/core-concepts/
  - https://www.pulumi.com/docs/iac/crossguard/configuration/
  - https://www.pulumi.com/docs/iac/crossguard/get-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pulumi Policies (CrossGuard) model

Policies are written in TypeScript, JavaScript, Python or OPA (Rego) and apply to Pulumi programs in any language. They run as analyzer plugins.

- **Policy**: one rule, validating a single resource as declared or a whole stack (when a rule spans resources). Has a name, description and validation function, plus metadata (severity, remediation steps, links, compliance control references).
- **Policy pack**: a project directory with a `PulumiPolicy.yaml` (the policy equivalent of `Pulumi.yaml`: runtime, optional version, description, entry point) and one or more policies. A pack may define a configuration schema so one pack enforces stricter thresholds in production than in development.
- **Policy group**: applies packs to stacks or cloud accounts in Pulumi Cloud.
- Pre-built packs (Pulumi Best Practices, AWS Organizations Tag Policies from Essentials up; CIS, PCI DSS, HITRUST, NIST, ISO 27001, CMMC on Enterprise) need no code. Custom packs are written by you.

## Run locally
```bash
pulumi preview --policy-pack /path/to/policy-pack
pulumi up --policy-pack /path/to/pack-1 --policy-pack /path/to/pack-2   # repeat the flag for more packs
```
Local execution works with any backend, including self-managed. The pack must be on disk where Pulumi runs and its runtime installed. IaC-managed resources are checked during `preview` and `up`, before the cloud changes; a violation of a mandatory policy stops the deployment.

## Publishing and versions
`pulumi policy publish` creates a new semantic version rather than replacing one. A policy group references a specific version, so publishing changes nothing enforced until the group is pointed at it; enable `latest` to track releases automatically.

## Runtime requirements
The runtime in `PulumiPolicy.yaml`, not the program's language, decides what must be installed: `nodejs` needs Node.js; `python` needs Python (Pulumi creates the virtualenv); `opa` needs the OPA language plugin (downloaded on first use; `pulumi plugin install language opa` where downloads are disabled). A pack declaring `runtime: nodejs` always runs with Node.js, even when the program uses Bun. All pre-built packs run on Node.js. When a policy group enforces a pack, the CLI downloads it to `~/.pulumi/policies` and installs dependencies on first use of a version (network required that first time).

## Checked
2026-11-03. Confirmed on the Policy as code, Policy packs and Get started pages. Removed: the `pulumi policy new aws-typescript` command, the TypeScript and Python code (`validateResourceOfType`, `PolicyPack`, `ResourceValidationPolicy` signatures), `policy enable`, unknown-value and `validateStack` claims and the Verify paragraph, because no page read documents the SDK API. See the Policy API and SDK reference before writing policy code.
Method: documentation only; no commands were run.
