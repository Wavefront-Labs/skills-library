---
id: computing-software.devops-ci-cd.helm.show-and-get-commands
name: show-and-get-commands
category: computing-software
field: devops-ci-cd
product: helm
tags: [show, get, values, manifest, hooks, notes, metadata, inspect-release]
level: practitioner
status: docs-checked
description: "Inspect charts with helm show and releases with helm get: values, manifest, hooks, notes, metadata and revision selection."
sources:
  - "https://helm.sh/docs/helm/helm_show_values/"
  - "https://helm.sh/docs/helm/helm_get_values/"
  - "https://helm.sh/docs/helm/helm_get_all/"
  - "https://helm.sh/docs/helm/helm_get_manifest/"
  - "https://helm.sh/docs/helm/helm_get_hooks/"
  - "https://helm.sh/docs/helm/helm_get_notes/"
  - "https://helm.sh/docs/helm/helm_get_metadata/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Two command families answer different questions.

`helm show` inspects a chart (directory, archive, URL or reference) before you install it:

- `helm show values CHART` prints `values.yaml`; `--jsonpath` filters the output.
- `helm show chart CHART` prints `Chart.yaml`.
- `helm show crds CHART` prints the CustomResourceDefinition files.
- `helm show all CHART` prints everything.

`helm show values` accepts `--version`, `--devel`, `--repo`, `--verify` and `--keyring`.

`helm get` reads what an installed release recorded:

- `helm get values RELEASE` shows user-supplied values; `-a, --all` dumps computed values.
- `helm get manifest RELEASE` shows the generated Kubernetes manifest.
- `helm get hooks RELEASE` shows hooks, separated by `---`.
- `helm get notes RELEASE` shows the rendered NOTES.txt.
- `helm get metadata RELEASE` shows release metadata; `-o` accepts table, json or yaml.
- `helm get all RELEASE` combines notes, hooks, supplied values and the manifest; `--template` formats with a Go template such as `{{.Release.Name}}`.

Every `get` subcommand takes `--revision N` to read an earlier revision.

## Checked

2026-11-03. Confirmed against the helm show values and helm get values, all, manifest, hooks, notes and metadata reference pages on helm.sh (synopses, --revision on each, -a, -o, --template, --jsonpath, hooks separator). Removed: the `oci://` and "all accept" claims for show subcommands other than `values`, the dependency-resources remark, the diff advice and the typical-flow paragraph.
Method: documentation only; no commands were run.

