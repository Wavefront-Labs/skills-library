---
id: computing-software.cloud-infrastructure-engineering.aws.elastic-beanstalk-docker-platforms
name: elastic-beanstalk-docker-platforms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-beanstalk, eb-docker, docker-compose, dockerrun]
level: practitioner
status: docs-checked
description: "Deploy containers on Elastic Beanstalk: Docker vs ECS-managed platform branches, Dockerrun.aws.json versions, and authenticating to ECR, ECR Public and private registries."
sources: ["https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/docker-configuration.remote-repo.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker_ecs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker platforms on Elastic Beanstalk

## 1. Platform branches
| Branch | Notes |
|---|---|
| Docker (AL2 and AL2023) | Dockerrun.aws.json v1 for environments without Docker Compose; v3 for Docker Compose environments |
| ECS managed Docker (ECS running on AL2 and AL2023) | multiple containers per instance, defined in Dockerrun.aws.json v2; v2 works only on ECS managed platforms |
All Amazon Linux AMI (AL1) platform branches were set to retired on July 18, 2022. AWS recommends migrating "Multi-container Docker on AL1" to the ECS running on AL2023 branch; the page says no source code changes are required.

## 2. ECS managed branch
- Beanstalk creates one ECS cluster per environment, a task definition generated from Dockerrun.aws.json v2, a task on every instance (a new task when an instance is added), the ECS agent in a container, and log volumes `awseb-logs-containername` at `/var/log/containers/containername`.
- Images must be prebuilt in a public or private online repository. Building from a Dockerfile during deployment is not supported on this branch. Specify images by name in v2.
- If an ECS task fails, some containers do not start and Beanstalk does not roll back; redeploy the current or a previous version (console: application versions, Deploy).

## 3. Authenticating to image repositories
- **ECR**: Beanstalk authenticates with the environment's instance profile. Attach the managed policy `AmazonEC2ContainerRegistryReadOnly` (all repositories in the account), or a custom policy for one repository with `ecr:GetAuthorizationToken` on `*` plus pull actions on the repository ARN. Docker platform: `"Image": {"Name": "<account-id>.dkr.ecr.<region>.amazonaws.com/<repo>:latest", "Update": "true"}`. ECS managed platform: the `image` key of a container definition.
- **ECR Public**: authentication is optional but gives higher rate limits and reliability. Add `ecr-public:GetAuthorizationToken` and `sts:GetServiceBearerToken` to the instance profile. Not supported in China (`cn-*`) or GovCloud (`us-gov-*`) Regions, which use unauthenticated pulls. Use the `public.ecr.aws/registry-alias/repository-name:tag` format.
- **Private registry via Secrets Manager** (needs Docker and ECS managed platforms released on or after January 13, 2026): store `{"username":...,"password":...}` as a JSON secret; in `.ebextensions` use namespace `aws:elasticbeanstalk:application:environmentsecrets` to map env vars (e.g. `USER`, `PASSWD`) to `<secret-arn>:username` and `<secret-arn>:password`; add a prebuild hook script that runs `docker login -u $USER --password-stdin` at both `.platform/hooks/prebuild/` and `.platform/confighooks/prebuild/`. The ECS managed platform uses the native ECS secrets syntax instead.
- **Private registry via Dockerrun.aws.json**: create the auth file with `docker login [registry-server-url]`, upload it as `.dockercfg` to a secure S3 bucket in the same Region as the environment, grant `s3:GetObject` to the instance profile role, and reference `"Authentication": {"Bucket": ..., "Key": ...}` in Dockerrun.aws.json.

## Method
Rewritten from the three cited Elastic Beanstalk pages. Compose port mapping, `.env` handling, nginx customisation and log paths were not on those pages and were removed.

## Checked
Checked 2026-11-08 against the three cited Elastic Beanstalk Developer Guide pages (Docker overview, authenticating with image repositories, ECS managed Docker platform branch).
Method: docs-only read of cited pages, 2026-11-08
