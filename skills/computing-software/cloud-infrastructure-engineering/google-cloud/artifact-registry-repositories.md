---
id: computing-software.cloud-infrastructure-engineering.google-cloud.artifact-registry-repositories
name: artifact-registry-repositories
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, artifact-registry, container-registry, gcr-migration, remote-repositories, virtual-repositories, standard-repositories, cleanup-policies, immutable-tags, docker-credential-helper, pkg-dev, maven-repository, npm-repository, python-repository, apt-yum-repository, go-modules, helm-oci, artifact-registry-iam, vulnerability-scanning-ar]
level: practitioner
status: docs-checked
description: "Artifact Registry as the package source: standard, remote and virtual repos; auth from CI and runtimes; cleanup policies, immutable tags, GCR migration."
sources: ["https://cloud.google.com/artifact-registry/docs/overview", "https://cloud.google.com/artifact-registry/docs/repositories/remote-overview", "https://cloud.google.com/artifact-registry/docs/repositories/virtual-repo", "https://cloud.google.com/artifact-registry/docs/repositories/cleanup-policy", "https://cloud.google.com/artifact-registry/docs/docker/authentication", "https://cloud.google.com/artifact-registry/docs/transition/transition-from-gcr", "https://cloud.google.com/artifact-registry/docs/access-control"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Artifact Registry repositories

**Goal:** one regional registry per environment that caches upstream packages, holds your
builds immutably, is readable only by the right workloads, and does not grow forever.

## 1. Repository types and layout
| Type | Purpose |
|---|---|
| **Standard** | your own artifacts |
| **Remote** | caches dependencies from upstream public sources (for example Docker Hub, Maven Central, npm, PyPI) so you can scan and control them; upstream credentials can be supplied |
| **Virtual** | groups remote and private repositories behind a single endpoint; a priority on each repository controls the search order |
```bash
gcloud artifacts repositories create img --repository-format=docker --location=europe-west1 \
  --kms-key=projects/<KMS_PROJECT>/locations/<LOCATION>/keyRings/<RING>/cryptoKeys/<KEY> --immutable-tags --description="app images"
gcloud artifacts repositories create dockerhub --repository-format=docker --location=europe-west1 --mode=remote-repository \
  --remote-docker-repo=DOCKER-HUB --remote-username=<USER> --remote-password-secret-version=projects/<PROJECT>/secrets/dockerhub/versions/1
gcloud artifacts repositories create all --repository-format=docker --location=europe-west1 --mode=virtual-repository \
  --upstream-policy-file=upstreams.json
```
- Location is a region or a multi-region; check the remote-repository and cleanup pages for multi-region caveats.
- With immutable tags enabled, tagged artifacts can't be deleted (so cleanup policies cannot delete them); deploy by digest anyway.
- The upstream-policy file lists the member repositories with a priority each; see the virtual repository page for the exact format.

## 2. Auth
- `gcloud auth configure-docker europe-west1-docker.pkg.dev` registers the credential helper. Without gcloud, `docker login` with user `oauth2accesstoken` and an access token, or `_json_key_base64` with a base64 key (avoid long-lived keys); see the Docker authentication page.
- Runtimes need `roles/artifactregistry.reader` on the repository (or project) to pull.
- Roles: `artifactregistry.reader`, `.writer`, `.repoAdmin`, `.admin`; see the access-control page for what each allows. Grant per repository in production.

## 3. Keep it tidy and safe
```bash
gcloud artifacts repositories set-cleanup-policies img --location=europe-west1 --policy=cleanup.json --no-dry-run
```
Cleanup policies are Delete or Keep policies. A Delete policy uses a `condition` (for example `tagState`, `tagPrefixes`, `olderThan`); a Keep policy retaining a number of versions uses `mostRecentVersions` with `keepCount` instead of a `condition`. Use dry run first (see the cleanup-policy page) before enabling deletion.

## 4. Migrate from Container Registry (gcr.io)
`gcloud artifacts docker upgrade migrate --projects=<PROJECT>` sets up `gcr.io` repositories in Artifact Registry: it creates a repository for each Container Registry host in the project and redirects `gcr.io` to them. Pushes and pulls on `pkg.dev` require the repository to exist already. Registry permissions move from Cloud Storage buckets to repository IAM, so review IAM during the transition.

## Gotchas
- Remote repositories pull from the upstream on first use; upstream rate limits can still apply.
- Creating a repository is a separate step from pushing to it on `pkg.dev`.

## Verify
- [ ] A pull through the remote repository works and a later pull is served from the cache.
- [ ] A tagged image cannot be deleted in an immutable-tags repository.
- [ ] A dry-run of the cleanup policy lists only the versions you intend to delete.
- [ ] A workload in another project pulls with only `artifactregistry.reader` on the repository.

## Checked
2026-10-31. Confirmed against the Artifact Registry overview, remote and virtual repository, cleanup policy, Docker authentication, transition-from-Container-Registry and access-control pages: repository types and the virtual-repo priority, role names, `configure-docker`, `oauth2accesstoken` and `_json_key_base64`, the Delete/Keep policy fields (`mostRecentVersions`, `keepCount`, `tagPrefixes`, `olderThan`), immutable tags blocking deletion, gcr.io redirection and the migrate behaviour. The `gcloud artifacts` commands passed the command checker.
Removed as unconfirmed: format and mode enum lists, language-tool setup lines (pip, npm, Maven, Go), `gcrane`, bucket role names, priority-direction rule, `cleanupPolicyDryRun`, hostname and "any EU region" claims, Helm login, example cleanup JSON values.
Method: documentation only; no commands were run.
