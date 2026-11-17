---
id: computing-software.cloud-infrastructure-engineering.kubernetes.helmfile-multi-release-environments
name: helmfile-multi-release-environments
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, helmfile, helm, environments, helm-diff, helm-secrets, gitops]
level: practitioner
status: docs-checked
description: "Manage many Helm releases across environments with Helmfile: repositories, environments, layered values, needs ordering, diff/apply in CI, selectors, and v1 templating rules."
sources: ["https://helmfile.readthedocs.io/en/latest/", "https://github.com/helmfile/helmfile/blob/main/docs/cli.md", "https://github.com/helmfile/helmfile/blob/main/docs/configuration.md", "https://github.com/helmfile/helmfile/blob/main/docs/templating.md", "https://github.com/databus23/helm-diff"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helmfile for multi-release environments

## Layout
```
helmfile.yaml.gotmpl
environments/{dev,prod}.yaml
values/{common,dev,prod}/<release>.yaml(.gotmpl)
```
```yaml
# helmfile.yaml.gotmpl
environments:
  dev:  {values: [environments/dev.yaml]}
  prod: {values: [environments/prod.yaml]}
---
repositories:
- name: jetstack
  url: https://charts.jetstack.io
- name: bitnami
  url: registry-1.docker.io/bitnamicharts
  oci: true

releases:
- name: cert-manager
  namespace: cert-manager
  chart: jetstack/cert-manager
  version: <pinned-chart-version>
  values: [values/common/cert-manager.yaml]
- name: api
  namespace: shop
  chart: ./charts/api
  installed: {{ .Values.apiEnabled | default true }}
  values:
  - values/common/api.yaml
  - values/{{ .Environment.Name }}/api.yaml.gotmpl
  secrets:
  - values/{{ .Environment.Name }}/api-secrets.yaml   # decrypted by the helm-secrets plugin
```
In Helmfile v1, templating applies to `helmfile.yaml.gotmpl` and to values files ending `.gotmpl`;
plain `.yaml` values files are used as-is. `HELMFILE_RENDER_YAML=true` forces a plain
`helmfile.yaml` to be rendered as a template (a v0-to-v1 migration aid).
The `---` separates environment loading from the parts that use `.Values`.

## Commands
```bash
helmfile -e prod deps           # lock chart versions (helmfile.lock)
helmfile -e prod diff           # needs the helm-diff plugin
helmfile -e prod apply          # runs diff; if there are changes, runs sync
helmfile -e prod sync           # helm upgrade --install for each release
helmfile -e prod -l name=api apply     # selector; a release name works as a label
helmfile -e prod template > rendered.yaml   # for review, kubeconform, or GitOps rendering
helmfile -e prod destroy        # uninstalls and purges all releases
```
CI pattern: `diff` on pull requests (post output), `apply` on merge. Keep secret values out of
logged output.

## Practices
- Pin every `version:`; run `helmfile deps` and commit `helmfile.lock`.
- `needs:` declares ordering dependencies between releases (see the release reference).
- `installed: false` uninstalls the release on sync: deliberate removal path.
- Keep environment differences in values, not in conditional release blocks.
- Hooks (events `prepare`, `preapply`, `presync`, `preuninstall`, `postuninstall`, `postsync`, `cleanup`) for CRD installs or one-off migrations, sparingly.

## Helmfile vs GitOps controllers
Helmfile is push-based: no drift correction. Common pairing: Argo CD or Flux deploys,
Helmfile renders (`helmfile template`) or bootstraps the GitOps controller itself.

## Verify
- [ ] `helmfile -e prod diff` is empty right after `apply` (idempotent, no perpetual diffs
  from random values such as generated passwords).

## Checked

2026-10-25, against the helmfile repository docs (cli.md, configuration.md, templating.md, hooks.md, index.md) on main. Confirmed: `.gotmpl` templating rule and `HELMFILE_RENDER_YAML`, `--environment/-e` and `--selector/-l` with `name=` labels, `oci: true` repositories, `installed` semantics, `apply` = diff then sync, `deps` and `helmfile.lock`, helm-diff and helm-secrets plugins, hook event names. Removed as unconfirmed: the `needs` value format and DAG/parallelism claim, `--suppress-secrets` on diff/apply, the SOPS remark.

Method: documentation only; no commands were run.
