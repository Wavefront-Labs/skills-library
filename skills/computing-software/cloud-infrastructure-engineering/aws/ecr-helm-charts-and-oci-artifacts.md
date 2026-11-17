---
id: computing-software.cloud-infrastructure-engineering.aws.ecr-helm-charts-and-oci-artifacts
name: ecr-helm-charts-and-oci-artifacts
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecr, helm-ecr, helm, oci-artifacts, oras, notation-signing, referrers]
level: practitioner
status: docs-checked
description: "Store Helm charts in ECR as OCI artifacts: helm registry login, helm push and install from oci:// URLs, repository naming and checking the artifact media type."
sources: ["https://docs.aws.amazon.com/AmazonECR/latest/userguide/push-oci-artifact.html", "https://helm.sh/docs/topics/registries/", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-creation-templates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm charts and OCI artifacts in ECR

## Helm (ECR docs: Helm 3.9 or later for EKS compatibility)
```bash
REG=111122223333.dkr.ecr.eu-west-1.amazonaws.com
aws ecr create-repository --repository-name charts/orders        # repo name = <prefix>/<chart name>
aws ecr get-login-password --region eu-west-1 | helm registry login --username AWS --password-stdin $REG
helm package charts/orders          # -> orders-1.3.0.tgz (version from Chart.yaml)
helm push orders-1.3.0.tgz oci://$REG/charts
helm install orders oci://$REG/charts/orders --version 1.3.0
helm show values oci://$REG/charts/orders --version 1.3.0
```
- `helm push` takes the registry reference without chart name or tag (`oci://$REG/charts` above); Helm infers the repository basename from the chart name and the tag from the chart version. Some registries need the repository or namespace created first; the ECR docs example pushes to the bare registry URL with a repository named like the chart.
- Charts are referenced by full `oci://` URL in pull, show, template and install; Helm does not use `helm repo add` for OCI registries.
- ECR authentication tokens are valid for 12 hours and are per registry, so log in again from CD jobs.
- To create repositories on first push, use repository creation templates (see the ECR user guide page on templates for create-on-push).
- Signing artifacts, ORAS pushes and lifecycle handling of referrers are not covered here; follow the ECR signing and lifecycle pages.

## Verify
- [ ] `helm pull oci://$REG/charts/orders --version 1.3.0` works from the CD system's role.
- [ ] `aws ecr describe-images --repository-name charts/orders` shows `artifactMediaType` `application/vnd.cncf.helm.config.v1+json`.

## Checked
2026-10-27. Documentation: Amazon ECR User Guide (pushing a Helm chart to a private repository) and Helm docs (OCI-based registries), read this date. Confirmed: helm registry login with username AWS and get-login-password, 12-hour token, helm package and helm push to an oci:// reference, Helm 3.9 or later for EKS compatibility, describe-images artifactMediaType for Helm, Helm infers chart name and tag, oci:// supported by pull/push/show/template/install. Removed unconfirmed ORAS, Notation, Flux/Argo CD, referrer lifecycle, 403 and replication claims.
Method: documentation only; no commands were run.
