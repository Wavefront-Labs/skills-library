---
id: computing-software.devops-ci-cd.helm.notes-txt
name: notes-txt
category: computing-software
field: devops-ci-cd
product: helm
tags: [notes-txt, post-install-notes, usage-notes, templates-dir, release-output]
level: intro
status: docs-checked
description: "Write templates/NOTES.txt for post-install usage notes, how it is rendered, and how to read it back with helm get notes."
sources:
  - "https://helm.sh/docs/chart_template_guide/notes_files/"
  - "https://helm.sh/docs/helm/helm_get_notes/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A file `templates/NOTES.txt` is a plain-text template. After install or upgrade Helm prints it to the terminal, so use it to tell users how to reach the application, find a generated password or run the first command.

```text
Thank you for installing {{ .Chart.Name }}.

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}
  $ helm get all {{ .Release.Name }}
```

Details:

- NOTES.txt is rendered like any template, so all objects and functions are available.
- It is printed at the end of `helm install` and `helm upgrade`, and when viewing `helm status`.
- Retrieve it later with `helm get notes RELEASE_NAME`; `--revision` selects a revision.
- `helm install` and `helm upgrade` have `--hide-notes` to suppress it in the output, and `--render-subchart-notes` to render subchart notes along with the parent.
- Keep it brief and point to the README for detail. Creating one is strongly recommended but not required.

## Checked

2026-11-08. Read the NOTES.txt page, helm get notes and the Charts topic page in full, plus helm install and upgrade options. Removed unsupported claims (not sent to cluster, helm template skips notes, subcharts never printed, best-practices guide branching); added --hide-notes, --render-subchart-notes and --revision.

Method: documentation only; no commands were run.
