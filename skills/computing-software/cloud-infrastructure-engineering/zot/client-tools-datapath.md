---
id: computing-software.cloud-infrastructure-engineering.zot.client-tools-datapath
name: client-tools-datapath
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, skopeo, regctl, oras, crane, helm-oci]
level: intro
status: docs-checked
description: "Push and pull images, artifacts and Helm charts to Zot with skopeo, regclient, oras, helm and crane, including TLS and login options."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/user-guides/user-guide-datapath.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Examples use a plain-HTTP registry at `localhost:5000`.

skopeo:
```
skopeo --insecure-policy copy --dest-tls-verify=false --multi-arch=all --format=oci docker://busybox:latest docker://localhost:5000/busybox:latest
```
Pull by swapping source and destination (`--src-tls-verify=false`, `oci:/oci/images:busybox:latest`). Auth flags: `--src-creds`/`--dest-creds username:password`.

regclient:
```
regctl registry set --tls=disabled localhost:5000
regctl image copy ocidir://path/to/golang:1.20 localhost:5000/tools
regctl repo ls localhost:5000
regctl tag ls localhost:5000/tools
```

oras (artifacts):
```
oras push --plain-http localhost:5000/hello-artifact:v2 --config config.json:application/vnd.acme.rocket.config.v1+json artifact.txt:text/plain
oras pull --plain-http localhost:5000/hello-artifact:v2
oras attach --artifact-type 'signature/example' localhost:5000/hello-artifact:v2 ./signature.json:application/json
oras discover -o tree localhost:5000/hello-artifact:v2
oras login -u myUsername -p myPassword localhost:5000
```

helm (charts as OCI):
```
helm push zot-1.2.3.tgz oci://localhost:5000/zot-chart
helm pull oci://localhost:5000/zot-chart/zot --version 1.2.3
helm registry login -u myUsername localhost:5000
```

crane: `crane --insecure push|pull|copy`, `crane ls localhost:5000/alpine`, `crane digest localhost:5000/alpine:latest`, `crane auth login -u myUsername localhost:5000`.

## Checked

All client tool examples confirmed.

Method: docs-checked 2026-11-09 against zot docs user-guides/user-guide-datapath.md (read in full).
