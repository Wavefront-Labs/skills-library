---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-vap-generation-flags-and-bindings
name: opa-gatekeeper-vap-generation-flags-and-bindings
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, validatingadmissionpolicy, vap, vapb, generate, default-create-vap-for-templates, enforcement-actions]
level: sme
status: docs-checked
description: "Have Gatekeeper generate ValidatingAdmissionPolicy and binding resources from CEL templates and constraints, and map enforcement actions to validationActions."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/validating-admission-policy.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper vap generation flags and bindings

VAP generation is beta (v3.20) and on by default. Kubernetes needs both a policy (VAP) and a binding (VAPB). Gatekeeper can generate both from templates using the `K8sNativeValidation` engine:
- `--default-create-vap-for-templates=true` generates a VAP per such template; override per template with `generateVAP: true` in the engine `source`.
- `--default-create-vap-binding-for-constraints=true` generates a VAPB per constraint. Override per constraint through scoped actions: with `enforcementAction: scoped`, a VAPB is generated only if `vap.k8s.io` appears in `scopedEnforcementActions`.

Action mapping to `validationActions`: `deny` is Deny, `warn` is Warn, `dryrun` is Audit.

If the engine `source` omits `failurePolicy`, `--default-k8s-native-validation-failure-policy` (default `Fail`) applies, both to Gatekeeper CEL evaluation and generated VAPs. If a VAP cannot resolve its Constraint `paramKind`, `Fail` rejects matching requests; clusters needing availability during bootstrapping can set `Ignore`.

Generated VAPs inherit the validating webhook `namespaceSelector` (including the `admission.gatekeeper.sh/ignore` label) when `--sync-vap-enforcement-scope` is on (deprecated, removal planned in v3.24). Upgrading changed exemption behaviour: namespaces matching an exemption flag without the label are no longer exempt, so review them before upgrading. Gatekeeper webhook can act as backup if VAP fails open.

## Checked

2026-11-04. Confirmed against validating-admission-policy.md (generation flags, scoped actions, action mapping, failure policy, namespace exemptions). Removed or corrected: nothing.

Method: documentation only; no commands were run.
