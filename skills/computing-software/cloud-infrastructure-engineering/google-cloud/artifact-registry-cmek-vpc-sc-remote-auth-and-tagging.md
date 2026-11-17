---
id: computing-software.cloud-infrastructure-engineering.google-cloud.artifact-registry-cmek-vpc-sc-remote-auth-and-tagging
name: artifact-registry-cmek-vpc-sc-remote-auth-and-tagging
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, artifact-registry, artifact-registry-cmek, artifact-registry-vpc-sc, artifact-registry-upstream-auth, remote-repo-credentials, image-tagging-strategy, artifact-registry-labels, cleanup-policies]
level: practitioner
status: docs-checked
description: "Harden Artifact Registry: CMEK repositories, VPC Service Controls, authenticated remote (pull-through) repositories, immutable tags, digest deploys and cleanup policies."
sources: ["https://docs.cloud.google.com/artifact-registry/docs/cmek", "https://docs.cloud.google.com/artifact-registry/docs/securing-with-vpc-sc", "https://docs.cloud.google.com/artifact-registry/docs/repositories/remote-repo", "https://docs.cloud.google.com/artifact-registry/docs/repositories/cleanup-policy", "https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/repositories/create", "https://artifactregistry.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Artifact Registry: CMEK, VPC-SC, remote auth and tagging

## 1. CMEK (set at creation only)
```bash
PN=$(gcloud projects describe <P> --format='value(projectNumber)')
gcloud kms keys add-iam-policy-binding ar-key --keyring=<KR> --location=europe-west2 \
  --member=serviceAccount:service-$PN@gcp-sa-artifactregistry.iam.gserviceaccount.com --role=roles/cloudkms.cryptoKeyEncrypterDecrypter
gcloud artifacts repositories create apps --repository-format=docker --location=europe-west2 \
  --kms-key=projects/<KP>/locations/europe-west2/keyRings/<KR>/cryptoKeys/ar-key --immutable-tags
```
- You choose the key when you create the repository; you cannot later switch to Google default encryption or to a different key.
- The key location must match the repository location. Grant the role to the Artifact Registry service agent and to the account that creates repositories. If the service agent does not exist yet, create it with `gcloud beta services identity create --service=artifactregistry.googleapis.com`.
- Disabling or destroying the key makes artifact data inaccessible; readers and viewers can still see metadata (names, versions, tags). Revoke the role from the service agent before disabling a key.
- Organisation policy `constraints/gcp.restrictNonCmekServices` can make Artifact Registry refuse non-CMEK repositories; `constraints/gcp.restrictCmekCryptoKeyProjects` limits which projects' keys are allowed. Cloud KMS Autokey is an alternative to creating keys by hand.

## 2. Inside VPC Service Controls
Add `artifactregistry.googleapis.com` to the perimeter's restricted services. Consequences:
- GKE private clusters in the perimeter can pull images in the perimeter and Google-provided images. Services that need Artifact Registry (Binary Authorization, Artifact Analysis, GKE, Cloud Run) must be in the perimeter too.
- Cached Docker Hub images on `mirror.gcr.io` are outside the perimeter unless you add an egress rule for the Artifact Registry Docker cache (operation `DockerRead` on `artifactregistry.googleapis.com`).
- Reach Artifact Registry through the normal Google API domains, `restricted.googleapis.com` (199.36.153.4/30) or `private.googleapis.com` (199.36.153.8/30).
- For `gcr.io` repositories hosted on Artifact Registry, ingress and egress rules must use identity type `ANY_IDENTITY`.
- With a perimeter, also enable the Access Context Manager API before creating remote repositories.

## 3. Remote repositories with upstream credentials
```bash
printf '%s' "$DOCKERHUB_TOKEN" | gcloud secrets create dockerhub-token --data-file=-
gcloud artifacts repositories create dockerhub --repository-format=docker --location=europe-west2 \
  --mode=remote-repository --remote-docker-repo=DOCKER-HUB \
  --remote-username=<USER> --remote-password-secret-version=projects/<P>/secrets/dockerhub-token/versions/1
```
- Enable the Secret Manager API and give Artifact Registry's service agent access to the secret (see "Configure authentication to remote repository upstreams" in the remote repository docs).
- You can add authentication to an unauthenticated remote repository later, but not remove it from an authenticated one.
- An Artifact Registry upstream must be a standard-mode repository, and its service agent needs read access (`roles/artifactregistry.serviceAgent` on the upstream when it is in another project).
- Clients pull through `LOCATION-docker.pkg.dev/PROJECT/REPOSITORY/IMAGE`.
- Virtual repositories front several repositories through an upstream policy file (`--upstream-policy-file`); higher `priority` values are searched first, so leave gaps between values.

## 4. Tagging and cleanup
- Tag with immutable, meaningful values: `1.4.2`, `git-<sha>`. Deploy by **digest** (`@sha256:...`) everywhere; tags are for humans.
- `--immutable-tags` (Docker only) prevents tags being deleted or moved to another digest and tagged images being deleted. Cleanup policies cannot delete tagged artifacts in such a repository.
```json
[{"name":"delete-untagged-30d","action":{"type":"Delete"},"condition":{"tagState":"untagged","olderThan":"30d"}},
 {"name":"keep-recent-20","action":{"type":"Keep"},"mostRecentVersions":{"keepCount":20}}]
```
- Durations take `s`, `m`, `h` or `d`. A delete policy needs a name, an action and at least one condition. A keep policy uses either conditions or `mostRecentVersions`, not both. If an artifact matches a delete and a keep policy, it is kept. Dry runs and active runs execute in a periodic background job, so changes take effect within about a day.
- `gcloud artifacts repositories set-cleanup-policies apps --location=europe-west2 --policy=cleanup.json --dry-run` first.

## Gotchas
- Cleanup deletes what matches; protect release tags with keep policies.
- Repository labels (`--labels KEY=VALUE`) help organise repositories.

## Verify
- [ ] `gcloud artifacts repositories describe apps --location=<R> --format='value(kmsKeyName,dockerConfig.immutableTags)'`.
- [ ] Pushing an existing tag with different content fails; dry-run cleanup lists only expected versions.

## Checked
2026-10-28. Confirmed against the CMEK, VPC Service Controls, remote repository and cleanup policy pages, the gcloud `repositories create` and `set-cleanup-policies` references, the virtual repository page (priorities, `--upstream-policy-file`) and the Artifact Registry v1 discovery document (`kmsKeyName`, `dockerConfig.immutableTags`, `CleanupPolicy`, `mostRecentVersions.keepCount`). Removed: the claim that CI outside the perimeter cannot push (and the private pool advice), the `*.pkg.dev` DNS instruction, the anonymous rate-limit remark, an exact `library/nginx` pull path, an unconfirmed Secret Manager role name, and the Dockerfile LABEL note.
Method: documentation only; no commands were run.
