---
id: computing-software.cloud-infrastructure-engineering.aws.ecr-docker-login-credential-helper-and-token-expiry
name: ecr-docker-login-credential-helper-and-token-expiry
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecr, credential-helper, docker-login, get-login-password, ecr-auth, imagepullsecrets]
level: practitioner
status: docs-checked
description: "Authenticate Docker, containerd and Kubernetes to ECR: get-login-password, the 12-hour token, amazon-ecr-credential-helper, minimum IAM and 'no basic auth credentials'."
sources: ["https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html", "https://github.com/awslabs/amazon-ecr-credential-helper", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/security_iam_id-based-policy-examples.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECR authentication: docker login, credential helper and token expiry

## Docker login
```bash
aws ecr get-login-password --region eu-west-1 | \
  docker login --username AWS --password-stdin 111122223333.dkr.ecr.eu-west-1.amazonaws.com
```
- The token is valid for **12 hours** and is per registry (account + region).
- Authenticate to each registry separately; repeat the command per registry. If login errors, upgrade the AWS CLI.

## Credential helper
Install `amazon-ecr-credential-helper` (`docker-credential-ecr-login` binary), then `~/.docker/config.json`:
```json
{"credHelpers":{"111122223333.dkr.ecr.eu-west-1.amazonaws.com":"ecr-login",
                "public.ecr.aws":"ecr-login"}}
```
or `"credsStore": "ecr-login"` to use it for all Amazon ECR registries (the helper README documents both forms). It currently does not support MFA.

## IAM
Pull:
```json
{"Effect":"Allow","Action":"ecr:GetAuthorizationToken","Resource":"*"},
{"Effect":"Allow","Action":["ecr:BatchGetImage","ecr:GetDownloadUrlForLayer","ecr:BatchCheckLayerAvailability"],
 "Resource":"arn:aws:ecr:eu-west-1:111122223333:repository/app/*"}
```
Push adds `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload`, `ecr:PutImage`.
The documented examples use `Resource: "*"` for `ecr:GetAuthorizationToken`. The token's permissions match those of the principal that requested it. For cross-account pulls also grant the principal in the repository policy.

## Kubernetes and others
- An `imagePullSecret` built from a `get-login-password` token stops working after 12 hours, so it needs scheduled refresh on any cluster that uses one.
- The per-runtime setup for EKS, ECS and Lambda is covered in their own guides; check those before relying on node or task roles.

## Verify
- [ ] `docker pull <registry>/app:tag` works on a fresh host with only the credential helper configured.
- [ ] CI uses role credentials, not stored passwords; any pull secret has a refresh job.

## Checked
2026-10-27. Documentation: Amazon ECR User Guide private registry authentication and identity-based policy examples; amazon-ecr-credential-helper README (GitHub). Confirmed: get-login-password piped to docker login with username AWS; 12-hour token; credHelpers and credsStore config forms; helper has no MFA support; GetAuthorizationToken example uses Resource *. Removed unconfirmed error-message wording, ECR Public login line, and unsourced EKS/containerd/Podman claims.
Method: documentation only; no commands were run.
