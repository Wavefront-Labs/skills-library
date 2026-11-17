---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.promoting-versioned-artifacts-and-release-tags
name: promoting-versioned-artifacts-and-release-tags
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, environment-promotion, artifact-promotion, release-tags, promotion-pipeline]
level: practitioner
status: draft
description: "Promote the same immutable artifact (module version, collection, EE image, AMI) through environments using git release tags, and avoid rebuilding per environment."
sources: ["HashiCorp - Terraform recommended practices, environments (https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices)", "Semantic Versioning (https://semver.org/)", "Git tagging (https://git-scm.com/book/en/v2/Git-Basics-Tagging)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Promoting versioned artifacts and release tags

## Principle
Build once, promote the **same** artifact. Environments differ only in configuration data (inventories, tfvars), never in code built separately per environment.

| Artifact | Identifier | Promotion means |
|---|---|---|
| Terraform module | git tag `v1.8.0` / registry version | env stack bumps `version = "1.8.0"` |
| Ansible collection | `acme.platform:2.3.1` in hub | env requirements pin moves |
| Execution environment | image digest `sha256:...` | controller EE / navigator config updated |
| AMI / golden image | AMI ID + version tag | env variable updated |
| Playbook repo | git tag `release-2026.10.2` | AAP project branch/ref per env |

## Release tags
```bash
git tag -a v2.3.1 -m "Release 2.3.1" && git push origin v2.3.1
```
- Tags are immutable references; environment configs point at tags, not branches.
- Optional environment pointer tags/branches (`env/staging`, `env/prod`) moved by the pipeline record what is deployed where; protect them so only CI can move them.
- AAP: project per environment with `scm_branch` set to the release tag, or a single project with "allow branch override" and the tag in the job template.

## Pipeline
1. Merge → build & test → publish artifact `2.3.1`.
2. Deploy to staging by updating staging's pin to `2.3.1` (PR or automated commit).
3. Gate (tests, approval) → same change for prod.
The prod PR diff is just a version bump: easy to review and to roll back (revert the pin).

## Gotchas
- `latest` tags or floating branches in prod break reproducibility and rollback.
- Rebuilding an EE "for prod" from the same definition yields a different image (base image drift); promote by digest.

## Verify
- [ ] For each environment you can name the exact artifact versions deployed, from git alone.
