---
id: computing-software.devops-ci-cd.helm.pull-command
name: pull-command
category: computing-software
field: devops-ci-cd
product: helm
tags: [pull, untar, verify, download-chart, prov, version-constraint]
level: intro
status: docs-checked
description: "Download a chart with helm pull to inspect, modify, verify or repackage it without installing."
sources:
  - "https://helm.sh/docs/helm/helm_pull/"
  - "https://helm.sh/docs/topics/charts/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm pull [chart URL | repo/chartname]` downloads a chart from a repository or registry. The docs recommend it for fetching packages to inspect, modify or repackage, and for cryptographic verification without installing.

```bash
helm pull repo/app --version ^2.0.0 --untar --untardir ./vendor
helm pull oci://registry.example.com/charts/app --version 1.2.3
helm pull repo/app --verify --keyring /path/to/pubring.gpg
```

Flags:

- `--version` takes an exact version or a range (for example `^2.0.0`); `--devel` includes pre-releases.
- `--untar` expands the archive; `--untardir` names the destination directory (default `.`).
- `-d, --destination` is where to write the chart; if both destination and untardir are given, untardir is appended.
- `--verify` requires the chart to have a provenance file and to pass verification. Failure means the chart is not saved locally.
- `--prov` fetches the provenance file without verifying it.
- `--repo URL` locates the chart without a configured repo; `--username`, `--password`, `--pass-credentials` pass credentials.
- `--ca-file`, `--cert-file`, `--key-file`, `--insecure-skip-tls-verify`, `--plain-http` configure transport.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_pull/ (synopsis, --verify failure behaviour, --prov, --untardir and --destination defaults, --repo and transport flags). Removed: the claim about vendoring dependencies into `charts/`.
Method: documentation only; no commands were run.

