---
id: computing-software.cloud-infrastructure-engineering.aws.ecr-registries-scanning-and-lifecycle
name: ecr-registries-scanning-and-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecr, container-registry, image-scanning, lifecycle-policy, pull-through-cache, cross-region-replication, immutable-tags, inspector, registry-policy, repository-policy, repository-creation-templates, ecr-login]
level: practitioner
status: docs-checked
description: "Run Amazon ECR: tag immutability, enhanced scanning via Inspector, lifecycle policies and previews, pull-through caches, replication, repository policies and VPC endpoints."
sources: ["https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning-basic.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning-enhanced.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning-enhanced-enabling.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/lifecycle_policy_parameters.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/lpp_creation.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/pull-through-cache.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/pull-through-cache-creating-rule.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/replication.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-permissions.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policy-examples.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-creation-templates.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon ECR - a registry that scans, prunes and replicates itself

**Goal:** images are pushed once with immutable tags, scanned, kept only as long as they are
useful, and pullable from every account and Region that runs them.
(Generic registry practice: `computing-software.cloud-infrastructure-engineering.docker.registry-management`.)

## 1. Repositories and tag immutability
```bash
aws ecr create-repository --repository-name name --image-tag-mutability IMMUTABLE --region us-east-2
aws ecr put-image-tag-mutability --repository-name name --image-tag-mutability IMMUTABLE_WITH_EXCLUSION \
  --image-tag-mutability-exclusion-filters filterType=WILDCARD,filter=latest --region us-east-2
```
- With immutability on, pushing an existing tag returns `ImageTagAlreadyExistsException`.
  Plain `IMMUTABLE` affects all tags; exclusion filters (wildcard `*` allowed) carve out tags
  that may still be overwritten. In the console the same idea appears as a Mutable or Immutable
  tag exclusion box.
- Deploy by digest or a unique tag (such as a git sha).
- Repository encryption cannot be changed after the repository is created.
- Pull-through-cache repositories need mutable tags for ECR to refresh cached images
  (see section 4).
- Repository creation templates apply settings (tag mutability, encryption, repository policy,
  lifecycle policy, resource tags) to repositories ECR creates for you through pull through
  cache, create on push or replication. A template matches by namespace prefix (a `/` is
  implied at the end; `ROOT` matches repositories with no other template; the longest matching
  prefix wins). Its "applied for" values are `PULL_THROUGH_CACHE`, `CREATE_ON_PUSH` and
  `REPLICATION`. Templates do not affect existing repositories. When no template matches an
  image push to a repository that does not exist, ECR does not create the repository.
  Without a template, repositories created by pull through cache or replication get defaults:
  mutable tags, AES-256, no repository or lifecycle policy. A repository creation role is
  required when the template uses tags or KMS.

## 2. Authentication
```bash
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
```
- An authorization token carries the permissions of the IAM principal that fetched it, works for
  any registry that principal can access, and is valid for 12 hours. Repeat the login for each
  registry.
- The ECR Docker credential helper is the alternative to repeated logins; it does not support
  MFA currently.
- Callers need `ecr:GetAuthorizationToken` through an IAM policy before they can push or pull.

## 3. Scanning
- **Basic**: AWS-native OS-package CVE scanning. Repositories can be set to scan on push; others
  are manual. An image can be scanned once per 24 hours (initial push scan counts), up to 100,000
  images per 24 hours in a registry. A completed scan sends an event to EventBridge.
- **Enhanced** (Amazon Inspector integration): scans operating system and programming-language
  packages, and shows how images are used on EKS and ECS (last used, number of clusters). ECR adds
  no charge but Inspector bills for scanning (see Inspector pricing). Inspector creates a
  service-linked role when you enable it.
- Enable per Region at registry level; filters choose continuous scan or scan on push per
  repository:
```bash
aws ecr put-registry-scanning-configuration --scan-type ENHANCED --region us-east-2 \
  --rules '[{"repositoryFilters":[{"filter":"prod","filterType":"WILDCARD"}],"scanFrequency":"CONTINUOUS_SCAN"},{"repositoryFilters":[{"filter":"*","filterType":"WILDCARD"}],"scanFrequency":"SCAN_ON_PUSH"}]'
```
  With no rules ECR continuously scans all repositories. A filter without a wildcard matches any
  repository name containing it. If a repository matches both a scan-on-push and a continuous
  filter, continuous wins. Repositories matching no filter are not scanned, and manual scans are
  not supported once enhanced scanning is on.
- When you first turn on enhanced scanning only images pushed in the last 14 days are recognised;
  older ones show `SCAN_ELIGIBILITY_EXPIRED` until pushed again. The re-scan duration is set in
  Inspector (default: until the image is deleted or enhanced scanning is disabled).
- ECR sends an EventBridge event (`ECR Scan Resource Change`, action `SCAN_FREQUENCY_CHANGE`) when a
  repository's scan frequency changes; Inspector emits events for the initial scan completing and
  for findings created, updated or closed.
- Scanning does not fix anything: rebuild on a patched base image.

## 4. Lifecycle policies
```json
{"rules":[
 {"rulePriority":1,"description":"keep last 50 release tags","selection":{"tagStatus":"tagged","tagPrefixList":["v"],"countType":"imageCountMoreThan","countNumber":50},"action":{"type":"expire"}},
 {"rulePriority":2,"description":"untagged after 7d","selection":{"tagStatus":"untagged","countType":"sinceImagePushed","countUnit":"days","countNumber":7},"action":{"type":"expire"}},
 {"rulePriority":3,"description":"everything else 30d","selection":{"tagStatus":"any","countType":"sinceImagePushed","countUnit":"days","countNumber":30},"action":{"type":"expire"}}
]}
```
- Every rule needs a unique `rulePriority`; a rule with `tagStatus` `any` must have the highest
  number (evaluated last). A lower number is higher priority.
- All rules are evaluated together, then applied by priority. An image is expired by exactly one
  rule or none; a lower-priority rule cannot act on an image a higher-priority rule matched.
- `tagStatus` is `tagged`, `untagged` or `any`. `tagged` needs `tagPatternList` (wildcards, at most four `*`
  per string) or `tagPrefixList`, not both; with several tags only images carrying all of them
  match. `untagged` must omit both.
- `countType`: `imageCountMoreThan` (no `countUnit`), `sinceImagePushed`, `sinceImagePulled` and
  `sinceImageTransitioned` (these take `countUnit: days`). `countNumber` must be a positive integer.
  Actions are `expire` or `transition` (to the `archive` storage class).
- Expiry happens within 24 hours of an image meeting the criteria, oldest first. The documented
  safeguard is the lifecycle policy preview (console: Edit test rules, Save and run test, then
  Apply as lifecycle policy). Review what it would expire before applying.
- An image referenced by a manifest list is not expired or archived until the manifest list is.
- Lifecycle policies act only in the Region they were created in; with replication, create the
  policy in each destination Region and account.

## 5. Pull-through cache
```bash
aws ecr create-pull-through-cache-rule --ecr-repository-prefix docker-hub \
  --upstream-registry-url registry-1.docker.io \
  --credential-arn arn:aws:secretsmanager:<REGION>:<ACCOUNT_ID>:secret:ecr-pullthroughcache/<NAME>
```
- Upstreams without authentication: Amazon ECR Public, Kubernetes registry (`registry.k8s.io`)
  and Quay. With a Secrets Manager secret: Docker Hub, Azure Container Registry, GitHub Container
  Registry, GitLab Container Registry (SaaS only) and Chainguard. ECR to ECR uses an IAM role
  (needed when accounts differ).
- The secret name must start with `ecr-pullthroughcache/` and be in the same account and Region as
  the rule.
- Pull `<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<prefix>/<upstream-path>:<tag>`; ECR creates
  the repository and caches the image. A pull after the 24-hour validation window expires makes
  ECR check upstream and update the cache; within the window it serves the cache. If the update fails the last cached image is served.
- Multi-architecture pulls fetch the manifest list and every image in it; pull by digest or an
  architecture-specific tag to fetch one.
- Turning on tag immutability stops ECR from updating cached images that reuse a tag. Pushing
  directly to a cache repository is unsupported.
- The first pull may need a route to the internet even when an interface VPC endpoint is used.
  AWS Lambda cannot pull container images through a pull through cache rule.
- Cache-created repositories support replication and scanning like any other repository.

## 6. Permissions and replication
- **Repository policy** is a resource policy on one repository. Example: pull needs
  `ecr:BatchGetImage` and `ecr:GetDownloadUrlForLayer`; push adds `ecr:BatchCheckLayerAvailability`,
  `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload` and `ecr:PutImage`.
  The grantee account must have the repository's Region enabled.
- **Registry policy** grants registry-level actions such as replication, pull-through-cache rule
  creation and repository creation. Prefer listing specific actions over `ecr:*`.
- **Replication** (cross-Region and cross-account) is configured in registry settings. Cross-account
  needs a registry policy only in the destination account allowing the source account
  `ecr:ReplicateImage` and `ecr:CreateRepository`; without `ecr:CreateRepository` the destination
  repositories must already exist with the same names. Source repositories need no policy.
  - Only content pushed or restored after replication is configured is replicated (use replication
    backfill for older images). Repository names are unchanged.
  - Up to 25 rules and 25 unique destinations per registry; up to 100 filters per rule. A
    repository prefix filter limits what replicates.
  - Replication happens once per push (no chaining a to b to c). Most images replicate in under 30
    minutes. It never deletes. Repository policies and lifecycle policies are not replicated; use
    repository creation templates for settings.
  - Not supported across AWS partitions; both accounts must have opted in to the Regions.
  - A replicated image whose tag already exists in an immutable destination repository is replicated
    without that tag.

## 7. VPC endpoints
- Interface endpoints `com.amazonaws.<REGION>.ecr.api` (API calls) and `com.amazonaws.<REGION>.ecr.dkr`
  (Docker push and pull) plus an S3 gateway endpoint, because ECR stores layers in S3.
  Enable the private DNS name; the endpoint security group must allow inbound 443 from the
  subnet. Fargate platform 1.4.0 or later and ECS on EC2 need both ECR endpoints and the S3
  gateway endpoint.

## Gotchas
- Lifecycle expiry is based on tags, count and age, so keep enough history that tags in use stay
  in scope, and test with the preview.
- `ecr:GetAuthorizationToken` comes from the puller's IAM policy, not the repository policy.
- Not covered here (no cited page): image signing with cosign or AWS Signer, and ECR Public
  quotas. Check the user guide before relying on them.

## Verify
- [ ] Pushing the same tag twice fails with `ImageTagAlreadyExistsException`.
- [ ] A lifecycle preview lists only the images you expect to lose.
- [ ] A consumer account can pull but not push (test both).
- [ ] A cached base image appears under the cache prefix as a repository of its own.

## Checked
Confirmed against the ECR User Guide pages listed in `sources`: tag mutability and exclusion filters,
registry authentication, basic and enhanced scanning, lifecycle policy properties and evaluation
rules, pull through cache, replication and registry permissions, repository policy examples,
repository creation templates and VPC endpoints.
Removed as not stated in those pages: cosign and AWS Signer signing, OCI artifact storage,
repository counts per Region, the CannotPullContainerError scale-out claim, Docker Hub rate limit
claim, ECR Public unlimited-pulls claim, Security Hub routing, `--force` repository delete, and the
`scanOnPush` create-repository flag.
Method: docs-only read of cited pages, 2026-11-08
