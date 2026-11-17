---
id: computing-software.cloud-infrastructure-engineering.kyverno.variables-and-context
name: variables-and-context
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [variables, context, request-object, serviceaccountname, images, shallow-substitution, helm-escaping]
level: practitioner
status: docs-checked
description: "Use variables in legacy Kyverno rules: {{ }} syntax, built-ins, image variables, context entries, escaping and where variables are not allowed."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/variables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax: JMESPath inside `{{ }}`. Plain JMESPath fields such as `jmesPath` take no braces. Policy-field references use `$(./../key_1/key_2)`. Escape with a backslash: `\$( )` and `\{{ }}`. In Helm charts wrap Kyverno variables as `` {{`{{ ... }}`}} ``.

Built-ins: `serviceAccountName`, `serviceAccountNamespace`, `request.roles`, `request.clusterRoles`, `images`. The first four are unavailable when `spec.background: true`. AdmissionReview data: `request.operation`, `request.object`, `request.oldObject` (null for CREATE and CONNECT), `request.userInfo` (`username`, `groups`), `request.namespace`.

Images: under `images.containers`, `initContainers` or `ephemeralContainers` each entry has `registry`, `path`, `name`, `tag`, `digest`, `reference`, `referenceWithTag`; tag and digest are mutually exclusive. Empty registry defaults to `docker.io` and empty tag to `latest` (configurable in the ConfigMap). Hyphenated names need quoting: `images.containers.\"my-container\".tag`. `{{ images.containers.*.name }}` returns all.

Context entries, evaluated in order (later ones can use earlier ones; the last redeclaration wins): `variable` (`value`, `jmesPath`, `default`; one of value or jmesPath required) and `configMap`. For API server calls see the External Data Sources page.

Nested lookups resolve the inner expression first. `{{- var }}` does one-time shallow substitution, useful when data itself contains `{{ }}` (such as HCL).

Not allowed in `match`, `exclude` or `patchesJson6902.path`. Allowed in context, preconditions, validation patterns and deny, `patchesStrategicMerge`, generate data and verifyImages. Order: rules selected, match conditions, preconditions, rule body.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/policy-types/cluster-policy/variables/.

Method: documentation only; no commands were run.
