---
id: computing-software.devops-ci-cd.helm.chart-best-practices-conventions
name: chart-best-practices-conventions
category: computing-software
field: devops-ci-cd
product: helm
tags: [best-practices, naming, chart-names, labels, values-naming, yaml-conventions, semver, standard-labels]
level: practitioner
status: docs-checked
description: "Helm chart conventions: DNS-1123 chart names, camelCase values, flat structure, standard labels and pinned image tags."
sources:
  - https://helm.sh/docs/chart_best_practices/conventions/
  - https://helm.sh/docs/chart_best_practices/values/
  - https://helm.sh/docs/chart_best_practices/labels/
  - https://helm.sh/docs/chart_best_practices/pods/
  - https://helm.sh/docs/chart_best_practices/templates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Rules from the Chart Best Practices guide.

Chart names: DNS-1123 label rules. Only lowercase letters, numbers and dashes; start and end with a lowercase letter or number; at most 63 characters (`drupal`, `nginx-lego`, `aws-cluster-autoscaler`). Invalid: uppercase, underscores, dots, leading or trailing dash. `helm lint` validates chart names against these rules.

Versions: Helm uses SemVer 2 where possible (Docker image tags are an exception). When a SemVer version goes into a label, the `+` is conventionally changed to `_`. YAML is indented two spaces, never tabs. Do not set `metadata.namespace` in chart templates; the namespace comes from the client call (`--namespace`).

Template files (`templates/`):

- `.yaml` extension for YAML output, `.tpl` for files producing no formatted content.
- Dashed file names (`my-example-configmap.yaml`), not camelCase; one resource per file; the name reflects the kind (`foo-pod.yaml`, `bar-svc.yaml`).
- Defined templates (`define`) are global across the chart and its subcharts, so namespace them: `nginx.fullname`, not `fullname`. `helm create` does this for you.
- Whitespace inside braces: `{{ .foo }}`, `{{- print "bar" -}}`, not `{{.foo}}`. Chomp whitespace where possible and avoid runs of blank lines in output.
- Use template comments `{{- /* ... */}}` to document defined templates; they do not appear in output. YAML `#` comments inside templates show up in `helm install --debug`, but beware: a `#` comment line that contains a `{{ required ... }}` is still evaluated, so an unset value breaks rendering. Wrap such lines in a template comment.
- JSON style is fine for short lists (`arguments: ["--dirname", "/foo"]`) and for genuinely JSON content, but not for complex constructs.

Values (`values.yaml`):

- Names begin with a lowercase letter and use camelCase (`chickenNoodleSoup`). No initial caps (they may clash with built-ins such as `.Release.Name`) and no hyphens.
- A dashed key (for example a dependency named `gitlab-runner`) cannot use dot notation; read it with `{{ index .Values "gitlab-runner" "checkInterval" }}`.
- Favor flat over nested (`serverName` rather than `server.name`): nested values need an existence check at every level. Nesting is acceptable when there are many related variables and at least one is non-optional.
- Quote all strings. YAML coercion is surprising (`false` vs `"false"`, large integers like `12345678` can become scientific notation); store large integers as strings and convert with `{{ int $value }}`. Tags such as `!!string` are consumed by the parser, so the type data is lost after one parse.
- Make values easy to override with `--set`: prefer maps over lists (`servers.foo.port=80` rather than `servers[0].port=80`, which breaks when ordering changes).
- Document every property with a comment that begins with the property name and gives at least one sentence (`# serverHost is the host name for the webserver`), so docs can be grepped and correlated.

Labels and annotations: metadata is a label if Kubernetes uses it to identify the resource or operators want to query by it; otherwise it is an annotation. Helm hooks are always annotations. Helm never requires a particular label. Recommended (REC) set:

- `app.kubernetes.io/name`: the app name.
- `helm.sh/chart`: `{{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}`.
- `app.kubernetes.io/managed-by`: `{{ .Release.Service }}`.
- `app.kubernetes.io/instance`: `{{ .Release.Name }}`.

Optional (OPT): `app.kubernetes.io/version` (`{{ .Chart.AppVersion }}`), `app.kubernetes.io/component`, `app.kubernetes.io/part-of`.

Pods and PodTemplates (Deployment, ReplicaSet, DaemonSet, StatefulSet, ReplicationController and others):

- Images use a fixed tag or the image SHA, never floating tags such as `latest`, `head` or `canary`. Images may be put in `values.yaml` (as one field, or image and tag as two).
- `helm create` wires `imagePullPolicy: {{ .Values.image.pullPolicy }}` with `pullPolicy: IfNotPresent` in `values.yaml`; Kubernetes also defaults to `IfNotPresent` if unset.
- Declare a `selector` with `matchLabels` in every PodTemplate set. In a Deployment, without it the entire label set is used to select pods, which breaks if you use labels that change, such as version or release date.

## Checked

2026-11-08. Checked against the five Helm 4 chart best-practices pages (conventions, values, labels, pods, templates), each read in full. Corrected chart-name rules to DNS-1123 and removed unsourced claims.

Method: documentation only; no commands were run.
