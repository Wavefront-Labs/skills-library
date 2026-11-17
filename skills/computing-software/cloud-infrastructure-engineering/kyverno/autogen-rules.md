---
id: computing-software.cloud-infrastructure-engineering.kyverno.autogen-rules
name: autogen-rules
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [autogen, autogen-controllers, pod-controllers, cronjob, preconditions, status-autogen]
level: practitioner
status: docs-checked
description: "Understand Kyverno auto-gen for Pod rules: which controllers get generated rules, the autogen-controllers annotation, and the cases where it silently turns off."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/autogen/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Auto-gen derives controller rules from a rule that matches only `Pod`, so you do not write one per controller. Generated rules appear in the policy's `status.autogen.rules`.

Defaults: DaemonSet, Deployment, Job, StatefulSet, ReplicaSet and ReplicationController get rules prefixed `autogen-`; CronJob gets `autogen-cronjob-`. ReplicaSet and ReplicationController may need the default resource filters removed from the Kyverno ConfigMap.

Annotation `pod-policies.kyverno.io/autogen-controllers` selects controllers (example `Deployment,Job`); `none` disables auto-gen entirely. Custom resources with an embedded Pod template (for example OpenKruise `CloneSet`) can be listed.

Auto-gen is skipped when:
- `match` or `exclude` uses `names`, `selector` or `annotations`;
- `match` or `exclude` lists kinds beyond `Pod`;
- a mutate rule uses JSON patch on Pods.

Without auto-gen a Pod-matching policy still applies to Pods that controllers create. Exempt them with preconditions on `request.object.metadata.ownerReferences[].kind`. To exclude by labels or annotations, use preconditions with a quoted `"object"` segment (`request."object".metadata.annotations`) so the path is not translated.

Pitfall: patterns on `metadata` such as `namespace` are translated into the Pod template path (`spec.template.metadata`), which can cause false violations; disable auto-gen and write explicit rules.

For the CEL policy types the equivalent is the `autogen.podControllers` field (see the ValidatingPolicy and MutatingPolicy skills).

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
