---
id: computing-software.devops-ci-cd.helm.repository-index-yaml
name: repository-index-yaml
category: computing-software
field: devops-ci-cd
product: helm
tags: [index-yaml, repo-index, chart-repository, merge, url, digest]
level: practitioner
status: docs-checked
description: "What a chart repository is, the index.yaml format, and generating or merging it with helm repo index."
sources:
  - https://helm.sh/docs/topics/chart_repository/
  - https://helm.sh/docs/helm/helm_repo_index/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A chart repository is an HTTP server that serves an `index.yaml` file and, usually, the packaged charts and provenance files. Anything that answers GET requests with YAML and tar files works: a GCS or S3 bucket, GitHub Pages, or your own web server. The docs say that if you are considering a new repository you may want an OCI registry instead.

Example layout:

```text
charts/
  index.yaml
  alpine-0.1.2.tgz
  alpine-0.1.2.tgz.prov
```

`index.yaml` has `apiVersion: v1`, an `entries` map from chart name to a list of versions, and a `generated` timestamp. Each version entry holds the contents of `Chart.yaml` plus `created`, `digest` and `urls`. The package need not live on the same server as the index.

A valid repository must have an index file, and `helm repo add` will not add a repository without a valid `index.yaml`. Charts must be packaged and versioned with SemVer 2.

Generate it with `helm repo index [DIR]`:

- It reads the packaged charts in the directory and writes `index.yaml` there.
- `--url` sets the absolute URL of the chart repository for the chart URLs.
- `--merge FILE` merges the generated index into the given index; local charts take priority over existing ones.
- `--json` outputs JSON.
- Without `--merge` the command rebuilds `index.yaml` from scratch, including only charts it finds locally.

Workflow: `helm package chart-name/`, move the `.tgz` into a directory, run `helm repo index DIR --url https://example.com/charts` (add `--merge` to extend an existing remote index), then upload the revised `index.yaml`, the chart and any provenance file. Clients run `helm repo add NAME URL` (with `--username`/`--password` for HTTP basic auth, or `--insecure-skip-tls-verify` for a self-signed certificate) and `helm repo update` for later changes. `helm repo add` and `update` fetch `index.yaml` into the Helm cache directory, which is where `helm search` reads from.

Plain web server hosting: serve the directory, let `index.yaml` be fetched without authentication, and serve YAML with content type `text/yaml` or `text/x-yaml`.

## Checked

2026-11-08. Checked against the Helm chart repository topic and helm repo index pages, read in full. Removed unsourced claims.

Method: documentation only; no commands were run.
