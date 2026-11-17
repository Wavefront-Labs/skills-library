---
id: computing-software.devops-ci-cd.helm.lookup-function
name: lookup-function
category: computing-software
field: devops-ci-cd
product: helm
tags: [lookup, cluster-query, secrets, dry-run, template, existing-resources]
level: advanced
status: docs-checked
description: "Use the lookup function to read live cluster objects during render, and why it returns empty under helm template."
sources:
  - https://helm.sh/docs/chart_template_guide/functions_and_pipelines/
  - https://helm.sh/docs/chart_template_guide/function_list/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`lookup` queries the Kubernetes cluster during template rendering. Signature: `lookup apiVersion kind namespace name`, all strings. `name` and `namespace` may be empty strings, but for a namespace-scoped resource both must be given when you want a single object.

Docs examples (with the kubectl equivalent):

- One object: `lookup "v1" "Pod" "mynamespace" "mypod"` (`kubectl get pod mypod -n mynamespace`)
- All of a kind in a namespace: `lookup "v1" "Pod" "mynamespace" ""`
- All of a kind in all namespaces: `lookup "v1" "Pod" "" ""`
- One cluster-scoped object: `lookup "v1" "Namespace" "" "mynamespace"`
- All namespaces: `lookup "v1" "Namespace" "" ""`

Return value: a single object comes back as a dictionary you can navigate, such as `(lookup "v1" "Namespace" "" "mynamespace").metadata.annotations`. A list request returns a dictionary whose objects are under `items`, so loop with `range $i, $svc := (lookup "v1" "Service" "mynamespace" "").items`. When nothing is found an empty value is returned, which you can use to test for existence.

Important limits:

- Helm is not supposed to contact the API server during `helm template`, `helm install --dry-run` or `helm upgrade --dry-run`; under `helm template` the function always returns an empty response. To test `lookup` against a running cluster use `--dry-run=server` on `helm template`, `install` or `upgrade`.
- `helm uninstall` and `helm rollback` do not render templates, so `lookup` is never called by them.
- `lookup` uses Helm's existing Kubernetes connection configuration. Any error from the API server, for example missing permission to read the resource, makes template processing fail, so the user running Helm needs the matching RBAC rights.

An illustrative pattern (not from the docs) is keeping a generated Secret value stable across upgrades. The empty-result test is what makes it work on a first install:

```yaml
{{- $s := lookup "v1" "Secret" .Release.Namespace "db" }}
password: {{ if $s }}{{ $s.data.password }}{{ else }}{{ randAlphaNum 16 | b64enc }}{{ end }}
```

## Checked

2026-11-08. Checked against the Helm 4 function-list and install/dry-run documentation. Confirmed helm template returns an empty lookup and --dry-run=server performs a real one. Removed unsourced claims.

Method: documentation only; no commands were run.
