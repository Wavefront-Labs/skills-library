---
id: computing-software.cloud-infrastructure-engineering.zot.sign-and-attach-artifacts-workflow
name: sign-and-attach-artifacts-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, cosign-sign, regctl-artifact, referrers, artifact-tree, supply-chain]
level: practitioner
status: docs-checked
description: "Push an image to Zot, attach an artifact such as an SBOM with regctl, sign both with cosign using OCI 1.1 referrers, and view the artifact tree."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/workflow.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/building-ci-cd-pipeline.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Assumes Zot at `localhost:8080`.

1. Tell regctl the registry is plain HTTP: `regctl registry set --tls=disabled localhost:8080`
2. Copy an image:
   `skopeo copy --format=oci --dest-tls-verify=false docker://busybox:latest docker://localhost:8080/busybox:latest`
3. Attach an artifact to it:
   `regctl artifact put --artifact-type application/yaml -f artifact.yaml --subject localhost:8080/busybox:latest`
   With no `--subject` the artifact is independent, not linked to an image.
4. Show the tree and grab the referrer digest: `regctl artifact tree localhost:8080/busybox:latest`
5. Create keys with `cosign generate-key-pair`, then sign using referrers mode:
   `cosign sign -y --key cosign.key --registry-referrers-mode=oci-1-1 localhost:8080/busybox:latest`
   and sign the artifact via `localhost:8080/busybox@<referrer-digest>`.
6. Re-run the tree: the image shows two direct referrers (the artifact and its signature) and the artifact has its own signature as a second-level referrer.

CI/CD variant: build with `stacker build -f <stackerfile.yaml>`, publish with `stacker publish --url <url> --username <user> --password <password>` or `skopeo copy --format=oci oci:<oci-dir>/image:tag docker://<zot-server>/image:tag`, sign with `cosign sign --key cosign.key <zot-server>/image:tag`. The article pins example tool versions; check current ones.

## Checked

2026-11-04. Confirmed against the provenance workflow page (regctl, skopeo, cosign commands and the two-direct-referrers tree) and the CI/CD pipeline page (stacker, skopeo and cosign examples).

Method: documentation only; no commands were run.
