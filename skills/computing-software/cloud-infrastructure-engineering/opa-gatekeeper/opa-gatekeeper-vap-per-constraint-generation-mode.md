---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-vap-per-constraint-generation-mode
name: opa-gatekeeper-vap-per-constraint-generation-mode
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, vap-generation-mode, per-constraint, paramkind, migration, generate, rollout]
level: sme
status: docs-checked
description: "Switch Gatekeeper to per-Constraint VAP generation, understand the parameter visibility and CEL size trade-offs, and migrate modes with a two-phase rollout."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/validating-admission-policy.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper vap per constraint generation mode

Default mode is `template`: one shared VAP per template using `paramKind`. Setting `--vap-generation-mode=constraint` (Helm `vapGenerationMode: constraint`) generates one VAP and VAPBinding per Constraint, embeds `spec.parameters` in the VAP, and omits `paramKind` and `paramRef`. That removes the kube-apiserver dependency on Constraint CRD discovery at startup.

Trade-offs:
- Parameter visibility: embedded parameters are readable by anyone with get, list or watch on the generated VAPs, even without access to the Constraint kind. Do not put secrets in parameters.
- Size: Kubernetes CEL expressions are capped at 100,000 Unicode code points; oversized ones produce a generation error and the existing VAP keeps enforcing old parameters.
- Cost: one compiled VAP per Constraint; template updates rewrite every derived VAP.
- Templates must read parameters via `variables.params`; direct references to the VAP top-level `params` are rejected.

All pods assigned the `generate` operation must use the same mode. Migrate in two phases: (1) upgrade with `audit.disableGenerateOperation=true` and `controllerManager.disableGenerateOperation=true`, leaving the mode unchanged; (2) verify every old generator pod, including Terminating ones, is gone; (3) upgrade with the new mode and restore the generation assignments. Roll back the same way with `template`. During the pause existing policies keep enforcing but changes do not converge.

## Checked

2026-11-08: read the Per-Constraint VAP generation section of website/docs/validating-admission-policy.md in the Gatekeeper repo (partial read, that section only). Confirmed the mode flag and Helm value, parameter visibility, the 100,000 code point limit, variables.params requirement, generate-operation rules and the two-phase rollout. Nothing removed.

Method: documentation only; no commands were run.
