---
id: computing-software.devops-ci-cd.helm.debugging-templates
name: debugging-templates
category: computing-software
field: devops-ci-cd
product: helm
tags: [debugging, debug, dry-run, template, lint, get-manifest, render-errors, troubleshooting]
level: practitioner
status: docs-checked
description: "Debug failing charts with helm lint, helm template, install --dry-run --debug and get manifest."
sources:
  - "https://helm.sh/docs/chart_template_guide/debugging/"
  - "https://helm.sh/docs/helm/helm_template/"
  - "https://helm.sh/docs/helm/helm_lint/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Four commands cover most template debugging.

- `helm lint ./chart` checks well-formedness; `--strict` fails on warnings, `--set`/`-f` render with your values, `--with-subcharts` also lints dependencies.
- `helm template RELEASE ./chart` renders locally and prints the YAML (the debugging guide suggests `helm template --debug`). `-s templates/x.yaml` (`--show-only`) prints only the manifests from that template. Values that would be looked up in-cluster are faked, and no server-side validity testing is done.
- `helm install --dry-run --debug RELEASE ./chart` also renders locally without installing, but checks whether conflicting resources are already running on the cluster. `--dry-run=client` makes no cluster connection; `--dry-run=server` allows cluster connections and runs any `lookup` in the chart against the server.
- `helm get manifest RELEASE` shows what templates are installed on the server.

The rendered YAML goes to the Kubernetes API server, which may reject it for reasons other than formatting. When your YAML fails to parse but you want to see what was generated, comment out the problem section in the template with YAML `#` comments (for example `# {{ .Values.foo | quote }}`) and re-run `helm install --dry-run --debug`: the output is returned with the comments intact.

Debugging `lookup`: run with `--debug`; when a lookup returns empty, Helm logs the apiVersion, kind, namespace and name, with "lookup: resource not found" for a single-object lookup or "lookup: resource list not found" for a list lookup. Common causes: the resource does not exist, RBAC denies access, `helm template` was run without cluster access (use `--dry-run=server` to connect), or a wrong apiVersion, kind, namespace or name.

## Checked

2026-11-08. Read the Debugging Templates page, helm template and helm lint pages. Removed unsupported tricks (HELM_DEBUG, error message meanings, kubectl dry-run, non-zero exit, template vs install parse behaviour); added the documented dry-run client/server behaviour, comment trick and lookup debugging.

Method: documentation only; no commands were run.
