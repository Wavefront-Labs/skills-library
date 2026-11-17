---
id: computing-software.cloud-infrastructure-engineering.aws.ecr-cross-region-and-cross-account-replication
name: ecr-cross-region-and-cross-account-replication
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecr, ecr-replication, registry-replication, cross-region, cross-account, registry-policy, containers]
level: practitioner
status: docs-checked
description: "Replicate ECR images across regions and accounts: replication rules with repository filters, destination registry policies, creation templates and replica checks."
sources: ["https://docs.aws.amazon.com/AmazonECR/latest/userguide/replication.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-permissions-create-replication.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/service-quotas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECR cross-region and cross-account replication

**Why:** pull images locally in every region (faster, no cross-region transfer per pull, DR
when the build region is down) and push once from CI.

## 1. Replication configuration (source registry)
```bash
aws ecr put-replication-configuration --replication-configuration '{
 "rules": [{
   "destinations": [{"region": "eu-west-1", "registryId": "<ACCOUNT_ID>"},
                    {"region": "us-west-2", "registryId": "<PROD_ACCOUNT_ID>"}],
   "repositoryFilters": [{"filter": "prod/", "filterType": "PREFIX_MATCH"}]}]}'
aws ecr describe-registry --query replicationConfiguration
```
- Registry-level limits (not adjustable): up to 25 rules, up to 25 unique destinations across all rules, up to 100 filters per rule. The only filter type is `PREFIX_MATCH` (repository name prefix).
- The repository name is identical in every destination; most images replicate in under 30 minutes.
- Cross-Region replication needs both accounts opted in to the Region, and does not work across AWS partitions.
- Only content pushed or restored **after** replication is configured replicates; use replication backfill for existing images.
- Destination repositories are created automatically with default settings (or using
  **repository creation templates** to set tag mutability, encryption, repository permissions and lifecycle policy).

## 2. Cross-account destination
Only the destination account needs a registry permissions policy; the source repositories need no policy. Without `ecr:CreateRepository` you must create same-named repositories in the destination yourself. Destination account registry permissions:
```bash
aws ecr put-registry-policy --region us-west-2 --policy-text '{
 "Version":"2012-10-17","Statement":[{"Sid":"AllowReplicationFromBuild",
  "Effect":"Allow","Principal":{"AWS":"arn:aws:iam::<BUILD_ACCOUNT_ID>:root"},
  "Action":["ecr:CreateRepository","ecr:ReplicateImage"],
  "Resource":"arn:aws:ecr:us-west-2:<PROD_ACCOUNT_ID>:repository/*"}]}'
```

## 3. Check status
```bash
aws ecr describe-image-replication-status --repository-name prod/api --image-id imageTag=1.4.2
```
Statuses per destination: `IN_PROGRESS`, `COMPLETE`, `FAILED`. Failed `CreateRepository` or `ReplicateImage` calls appear in CloudTrail.

## Gotchas
- Repository settings (tag mutability, encryption, permissions, lifecycle) are not replicated by default; set them in the destination through repository creation templates.
- Repository policies, IAM policies and lifecycle policies are not replicated.
- Replication performs no deletes: deleting an image in the source leaves the replica.
- Replication happens once per push: a chain us-west-2 to us-east-1 to us-east-2 does not forward the image to us-east-2.
- With tag immutability on in the destination, replicating an existing tag leaves the replicated image untagged.

## Verify
- [ ] Push a new tag; `describe-image-replication-status` shows `COMPLETE` for all destinations within minutes.
- [ ] ECS/EKS in the destination region pull from the local registry URI.
- [ ] Destination repos have the intended lifecycle/immutability settings.

## Checked
2026-10-27. Documentation: Amazon ECR User Guide (replication, registry permissions for cross-account replication, service quotas pages, read this date). Confirmed: 25 rules, 25 unique destinations, 100 filters per rule (corrected from the draft's 10 rules); destination-only registry policy with ecr:ReplicateImage and ecr:CreateRepository; only content pushed after configuration replicates; repository settings only via creation templates; no deletes; no partition crossing. Confirmed from the ECR API model (botocore ecr 2015-09-21): ReplicationStatus enum IN_PROGRESS/COMPLETE/FAILED and filter type PREFIX_MATCH. Removed unconfirmed claims about pull-through-cache repositories and KMS key choice.
Method: documentation only; no commands were run.
