---
id: computing-software.cloud-infrastructure-engineering.docker.ecr-and-artifact-registry-pull-through-caches
name: ecr-and-artifact-registry-pull-through-caches
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, pull-through-cache, registry-mirror, ecr-pull-through, artifact-registry-remote, aws-ecr, gcp-artifact-registry, rate-limits]
level: advanced
description: "Cache upstream images in AWS ECR pull-through cache rules or GCP Artifact Registry remote repositories: rule creation, credentials secret naming, the 24-hour refresh."
sources: ["https://docs.aws.amazon.com/AmazonECR/latest/userguide/pull-through-cache.html", "https://docs.cloud.google.com/artifact-registry/docs/repositories/remote-repo", "https://learn.microsoft.com/en-us/azure/container-registry/artifact-cache-overview"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ECR and Artifact Registry pull-through caches

## AWS ECR pull-through cache
```sh
# Upstream credentials live in Secrets Manager. The secret name must use the
# ecr-pullthroughcache/ prefix, in the same account and Region as the rule.
aws secretsmanager create-secret --name ecr-pullthroughcache/<NAME> \
  --secret-string '<CREDENTIAL_JSON>'
aws ecr create-pull-through-cache-rule --ecr-repository-prefix <PREFIX> \
  --upstream-registry-url <UPSTREAM_REGISTRY> \
  --credential-arn <SECRET_ARN>
```
Pull through your private registry URI with the prefix:
```sh
docker pull <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<PREFIX>/<UPSTREAM_PATH>:<TAG>
```
- The first pull creates the repository and caches the image in your private registry; the default settings apply unless a repository creation template matches.
- Use a repository creation template to define settings for repositories ECR creates on your behalf.
- For later pulls of a tag, ECR checks the upstream for a newer version at least once every 24 hours (it serves the cache without contacting upstream inside that window).
- Pushing directly into a pull-through-cache repository is not supported.

## GCP Artifact Registry remote repository
```sh
gcloud artifacts repositories create <REPO> --repository-format=docker \
  --location=<LOCATION> --mode=remote-repository \
  --remote-docker-repo=DOCKER-HUB
```
`--remote-docker-repo` takes a preset such as `DOCKER-HUB` or a custom upstream; see the remote repository page for the credential flags.

## Azure
ACR "artifact cache" rules: `az acr cache create -r myacr -n hub-nginx -s docker.io/library/nginx -t nginx`.

## Gotchas
- These are not transparent mirrors: image references change, so rewrite FROM lines and manifests.

## Verify
After a pull, `aws ecr describe-repositories` lists the auto-created repository under your prefix.

## Checked
2026-10-28. Confirmed against the ECR pull through cache page (secret `ecr-pullthroughcache/` prefix, same account and Region, repository creation on first pull, creation templates, at-least-24-hour refresh, no direct pushes), the Artifact Registry remote repository page (`--remote-docker-repo`, `DOCKER-HUB`) and `check_commands.py` (all aws and gcloud commands and flags exist). Corrected the refresh interval (was "at most once" per 24 h). Removed unconfirmed claims: IAM action names, `library/` path rule, virtual repositories, Kyverno, containerd `hosts.toml`, lifecycle remarks, example account IDs and credentials.
Method: documentation only; no commands were run.
