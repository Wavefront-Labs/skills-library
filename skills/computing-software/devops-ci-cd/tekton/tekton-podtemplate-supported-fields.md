---
id: computing-software.devops-ci-cd.tekton.tekton-podtemplate-supported-fields
name: tekton-podtemplate-supported-fields
category: computing-software
field: devops-ci-cd
product: tekton
tags: [podtemplate, pod-security, scheduling, taskrun]
level: practitioner
status: docs-checked
description: "Customise Tekton TaskRun pods with a podTemplate: supported fields, defaults and the imagePullSecrets entrypoint lookup."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/podtemplates.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `podTemplate` on a TaskRun or PipelineRun sets pod-level options. Supported fields include `env` (takes precedence over `steps` and `stepTemplate` env), `nodeSelector`, `tolerations`, `affinity`, `securityContext`, `volumes`, `runtimeClassName`, `automountServiceAccountToken` (default `true`), `dnsPolicy` (default `ClusterFirst`; `ClusterFirstWithHostNet` is unsupported because Tekton pods cannot use host networking), `dnsConfig`, `enableServiceLinks` (default `true`), `priorityClassName`, `schedulerName` (for example `volcano.sh`), `imagePullSecrets`, `hostNetwork` (default `false`), `hostUsers` (default `true`; `false` creates a user namespace for stronger isolation; alpha, needs the `UserNamespacesSupport` feature gate on Kubernetes 1.25+), `hostAliases` and `topologySpreadConstraints`.

Parameter substitution `$(params.name)` works in string fields when the template is used in PipelineRun `taskRunSpecs`, including per matrix combination, for example a `nodeSelector` keyed by architecture.

If a Task step has no `command` and the podTemplate configures `imagePullSecrets`, the controller uses those secrets to look up the image entrypoint. Pod templates also apply to affinity assistant pods, but only for `tolerations`, `nodeSelector`, `securityContext`, `priorityClassName` and `imagePullSecrets`; a global one can be set with `default-affinity-assistant-pod-template`. A global `default-pod-template` is merged with run-level templates: run-level values win, and `env` and `volumes` merge by `name`.

## Checked

Checked 2026-11-08 against docs/podtemplates.md in tektoncd/pipeline (main), read in full. Confirmed the field list, defaults, dnsPolicy limits, parameter substitution, and the imagePullSecrets entrypoint lookup. Corrected the affinity assistant claim to the docs' five supported fields, removed the unsourced overwrite claim, and added the hostUsers alpha gate and global template merge rules.

Method: documentation only; no commands were run.
