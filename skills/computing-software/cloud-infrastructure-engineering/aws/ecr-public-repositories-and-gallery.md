---
id: computing-software.cloud-infrastructure-engineering.aws.ecr-public-repositories-and-gallery
name: ecr-public-repositories-and-gallery
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecr, ecr-public-gallery, ecr-public, public-ecr-aws, pull-through-cache, docker-hub-rate-limits]
level: practitioner
status: docs-checked
description: "Publish and consume images on ECR Public: catalog data for the gallery, registry alias, anonymous vs authenticated pull limits, and pull-through cache for mirrors."
sources: ["https://docs.aws.amazon.com/AmazonECR/latest/public/public-repositories.html", "https://docs.aws.amazon.com/AmazonECR/latest/public/public-repository-create.html", "https://docs.aws.amazon.com/AmazonECR/latest/public/public-service-quotas.html", "https://docs.aws.amazon.com/AmazonECR/latest/public/public-registry-settings.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/pull-through-cache.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECR Public repositories and the gallery

## Publish
```bash
aws ecr-public create-repository --repository-name mytool --region us-east-1 \
  --catalog-data file://catalog.json
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
docker tag mytool:1.2.0 public.ecr.aws/<alias>/mytool:1.2.0
docker push public.ecr.aws/<alias>/mytool:1.2.0
```
- The examples use `us-east-1`; the console flow lets you choose the Region for a public repository, so confirm supported Regions before relying on one.
- Registry alias: a default alias is assigned after your first public repository is created; you can request a custom alias, and if approved both aliases work. Avoid `aws`, `amazon` or AWS service names in the request.
- Catalog data fields (`description` max 1,024 characters, `aboutText` and `usageText` max 25,600, `architectures`, `operatingSystems`, `logoImageBlob` max 512,000 bytes) show on gallery.ecr.aws. Content types act as search filters. The logo is publicly visible only for verified (AWS Marketplace certified) accounts.

## Consume
- Public repositories are open to pull from without login.
- Default quotas read on the ECR Public quotas page this date: unauthenticated pulls 1 per second (not adjustable), authenticated pulls 10 per second (adjustable), pulls to ECS, Fargate or EC2 resources 10 per second (not adjustable). Unauthenticated customers are limited to 500 GB of data per month (not adjustable). Re-read the page for current numbers.

## Mirror into private ECR (pull-through cache)
```bash
aws ecr create-pull-through-cache-rule --ecr-repository-prefix ecr-public \
  --upstream-registry-url public.ecr.aws
docker pull 111122223333.dkr.ecr.eu-west-1.amazonaws.com/ecr-public/docker/library/nginx:1.27
```
- The ECR docs list these upstreams: ECR Public, Kubernetes registry and Quay (no authentication); Docker Hub, Azure Container Registry, GitHub Container Registry, GitLab Container Registry (SaaS only) and Chainguard (Secrets Manager secret); and Amazon ECR (IAM role).
- For authenticated upstreams, `create-pull-through-cache-rule` takes `--upstream-registry` and `--credential-arn`; check the CLI reference before scripting.

## Gotchas
- A public repository is open to pull from and is visible on the ECR Public Gallery; do not push anything you would not publish.
- Public repositories are controlled with IAM policies and repository policies (see the ECR Public guide for what the repository policy covers).

## Verify
- [ ] Gallery page shows description, usage and architectures.
- [ ] Anonymous `docker pull` works; CI pulls via pull-through cache in the private registry.

## Checked
2026-10-27. Documentation: Amazon ECR Public User Guide (public repositories, creating a repository, registry settings, service quotas) and Amazon ECR User Guide pull through cache page, read this date. Confirmed: quota values quoted above; catalog data fields and limits from the ECR Public API model (botocore ecr-public 2020-10-30); alias behaviour; pull-through upstream list; CreatePullThroughCacheRule parameters ecrRepositoryPrefix, upstreamRegistryUrl, upstreamRegistry and credentialArn from the ECR API model. Removed the us-east-1-only claim (console lets you pick a Region), the lifecycle claim and unsourced bullets.
Method: documentation only; no commands were run.
