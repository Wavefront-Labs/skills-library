---
id: computing-software.cloud-infrastructure-engineering.aws.ecr-multi-architecture-images
name: ecr-multi-architecture-images
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecr, multi-arch-images, manifest-list, docker-buildx, graviton, oci-image-index]
level: practitioner
status: docs-checked
description: "Build and push multi-architecture (amd64 + arm64) images to ECR with buildx or CodeBuild, inspect manifest lists, and handle scanning, lifecycle and signing for them."
sources: ["https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-multi-architecture-image.html", "https://docs.docker.com/build/building/multi-platform/", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-manifest-formats.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-architecture images in ECR

A multi-arch image is a **manifest list** (OCI image index) pointing to one image manifest
per platform. Per the ECR docs, a manifest list can be pulled or referenced in an ECS task
definition or EKS pod spec like any other ECR image. A manifest list is optional.

## 1. Build and push with buildx
```bash
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 111122223333.dkr.ecr.eu-west-1.amazonaws.com
docker buildx create --name multi --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t 111122223333.dkr.ecr.eu-west-1.amazonaws.com/app:1.4.2 --push .
```
- Docker documents three strategies: QEMU emulation, a builder with multiple native nodes, or cross-compilation in multi-stage builds. Official BuildKit releases bundle QEMU emulators, so manual QEMU install is only needed if emulation fails.

## 2. Combine per-arch images (native builds)
ECR docs prerequisites: Docker CLI experimental features turned on (for `docker manifest`), the repository exists, and the images are pushed before you create the manifest.
```bash
# after pushing app:1.4.2-amd64 and app:1.4.2-arm64 from native builders
docker manifest create 111122223333.dkr.ecr.eu-west-1.amazonaws.com/app:1.4.2 \
  111122223333.dkr.ecr.eu-west-1.amazonaws.com/app:1.4.2-amd64 \
  111122223333.dkr.ecr.eu-west-1.amazonaws.com/app:1.4.2-arm64
docker manifest push 111122223333.dkr.ecr.eu-west-1.amazonaws.com/app:1.4.2
```

## 3. Inspect
```bash
docker manifest inspect 111122223333.dkr.ecr.eu-west-1.amazonaws.com/app:1.4.2
aws ecr batch-get-image --repository-name app --image-ids imageTag=1.4.2 \
  --accepted-media-types application/vnd.oci.image.index.v1+json application/vnd.docker.distribution.manifest.list.v2+json \
  --query 'images[0].imageManifest' --output text | jq '.manifests[].platform'
```
`docker manifest inspect` shows the size and digest of each referenced image manifest. Test lifecycle, scanning and signing behaviour for manifest lists in a scratch repository before relying on them; this skill does not state those behaviours.

## Verify
- [ ] `docker manifest inspect` lists linux/amd64 and linux/arm64 under the tag.
- [ ] The same tag runs on an x86 and a Graviton host/task.
- [ ] A lifecycle preview in a scratch repository does not expire child images you need.

## Checked
2026-10-27. Documentation: Amazon ECR User Guide (pushing a multi-architecture image) and Docker docs (multi-platform builds), read this date. Confirmed: docker manifest create/inspect/push flow and its prerequisites (experimental CLI, images pushed first), manifest list usable in ECS task definitions and EKS pod specs, buildx --platform linux/amd64,linux/arm64, QEMU bundled with BuildKit and the three build strategies. Confirmed from the ECR API model: BatchGetImage takes acceptedMediaTypes. Removed unconfirmed claims about lifecycle, scanning, signing, Lambda, CodeBuild ARM_CONTAINER and imagetools.
Method: documentation only; no commands were run.
