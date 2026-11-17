---
id: computing-software.cloud-infrastructure-engineering.kubernetes.helm-chart-authoring
name: helm-chart-authoring
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, helm, helm3, helm-chart, chart-yaml, values-yaml, values-schema-json, go-templates, sprig, helpers-tpl, named-templates, helm-template, helm-lint, helm-unittest, chart-testing, ct, helm-hooks, library-chart, subcharts, oci-registry, helm-push, semver, kustomize, packaging]
level: practitioner
status: verified
description: "Author maintainable Helm charts: chart layout, _helpers.tpl naming, values design with values.schema.json, safe templating idioms, hooks, library charts, testing and OCI publishing."
sources: ["Helm docs - Chart Template Guide", "Helm docs - Chart Best Practices", "Helm docs - Chart Hooks", "Helm docs - Registries (OCI)", "helm-unittest README", "helm/chart-testing README"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm chart authoring — charts other people can safely install

**Goal:** a chart whose defaults work, whose values are validated, whose output is
predictable under `helm template`, and that upgrades without surprise. Deploying charts via
GitOps is covered in `computing-software.devops-ci-cd.argo-cd.gitops-app-of-apps-and-sync`.

## 1. Layout
```
mychart/
  Chart.yaml            # apiVersion: v2, name, version (chart SemVer), appVersion (image)
  values.yaml           # every key documented with a comment
  values.schema.json    # JSON Schema; helm install/upgrade/lint/template validate against it
  templates/
    _helpers.tpl        # named templates only, no output
    deployment.yaml service.yaml serviceaccount.yaml hpa.yaml NOTES.txt
    tests/test-connection.yaml
  charts/               # vendored dependencies (helm dependency build)
```
Bump `version` on every chart change; `appVersion` tracks the app. Start from `helm create`
and delete what you do not need — it ships good helper conventions.

## 2. Helpers and naming
```gotemplate
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride -}}{{ .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else -}}{{ printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}{{- end -}}
{{- end -}}
{{- define "mychart.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
```
- Names truncate at 63 chars (DNS label limit).
- **Selector labels must never change between chart versions** — Deployment selectors are
  immutable, so adding a label there breaks every upgrade. Put `helm.sh/chart` and version
  labels only in metadata labels, not selectors.

## 3. Templating idioms
- `{{- toYaml .Values.resources | nindent 12 }}` for passthrough blocks; `nindent` not `indent`
  after a newline-trimmed action.
- `{{ .Values.x | quote }}` for strings that YAML might coerce (`"on"`, `"0123"`, `"1.10"`).
- `{{ required "image.repository is required" .Values.image.repository }}` for mandatory values.
- `{{- with .Values.nodeSelector }}nodeSelector: {{- toYaml . | nindent 8 }}{{- end }}` —
  remember `.` is rebound inside `with`/`range`; use `$` for the root.
- `tpl` lets users put templates in values; use sparingly, it makes output hard to reason about.
- Config-change rollouts: annotate the pod template with
  `checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}`.
- `lookup` returns empty under `helm template` and `--dry-run` (client-side), so any logic
  depending on it renders differently in CI than in the cluster.

## 4. Values design
- Mirror Kubernetes field names (`resources`, `affinity`, `tolerations`, `podSecurityContext`)
  so users can paste upstream YAML.
- Prefer maps over lists for things users override: Helm **replaces lists wholesale** on
  merge, so `-f prod.yaml` with one `env` entry wipes the defaults.
- Booleans as `enabled:` toggles per component; never require users to blank a value to disable.
- Write `values.schema.json` with `required`, `type` and `additionalProperties: false` on
  top-level objects to catch typos like `replicaCont`. With the root set to `additionalProperties: false`, every key
  in `values.yaml` (including `global`, subchart keys and the `helm create` defaults such as `tolerations`) must
  be declared, or `helm template` fails with `Additional property ... is not allowed` (run on Helm 4.3.1).
- No secrets in default values. Support `existingSecret: <name>` to reference a pre-made Secret.

## 5. Hooks and tests
- `helm.sh/hook: pre-upgrade,pre-install` for migrations, with
  `helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded`.
- Hook resources are **not managed** by the release afterwards (not deleted on uninstall
  unless the policy says so) and a failing hook fails the release.
- `helm test <RELEASE>` runs pods annotated `helm.sh/hook: test`.
- Unit test rendered output with the `helm-unittest` plugin; lint and install-test changed
  charts in kind with `ct lint-and-install` (chart-testing).

## 6. Dependencies and library charts
- Declare in `Chart.yaml` `dependencies:` with `condition: postgresql.enabled`; run
  `helm dependency update` and commit `Chart.lock`.
- Parent values reach a subchart under its name key (`postgresql.auth...`); `global:` is shared.
- `type: library` charts hold shared named templates and render nothing on their own —
  the right way to share helpers across many in-house charts.

## 7. Publish
```bash
helm lint ./mychart --strict
helm template rel ./mychart -f ci-values.yaml | kubeconform -strict -summary
helm package ./mychart && helm push mychart-1.4.0.tgz oci://registry.example.com/charts
helm install rel oci://registry.example.com/charts/mychart --version 1.4.0
```

## Gotchas
- CRDs in `crds/` are installed once and **never upgraded or deleted** by Helm; ship CRD
  changes separately.
- `helm upgrade --reuse-values` keeps old values and ignores new defaults — surprising
  after a chart upgrade; `--reset-then-reuse-values` (Helm 3.14+, confirmed in the 3.14.0 source) is safer.
- Whitespace: a missing `-` in `{{-` produces blank lines or broken indentation that only fails at apply.
- Resources renamed between chart versions are deleted and recreated — downtime and, for
  PVC templates, potential data loss.
- Rollback-on-failure flag naming has shifted across Helm versions (`--atomic` in 4.3.1 and 3.x); check `helm upgrade --help`.

## Verify
- [ ] `helm lint --strict` and schema validation pass; a typo'd values key fails.
- [ ] `helm template` output passes `kubeconform` against the target Kubernetes version.
- [ ] `helm upgrade` from the previous chart version succeeds with no resource recreated.
- [ ] Overriding one list item via `-f` behaves as documented.
- [ ] `helm-unittest` covers each `if`/`with` branch in templates.
