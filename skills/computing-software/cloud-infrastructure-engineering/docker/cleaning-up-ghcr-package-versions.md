---
id: computing-software.cloud-infrastructure-engineering.docker.cleaning-up-ghcr-package-versions
name: cleaning-up-ghcr-package-versions
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, ghcr, ghcr-cleanup, delete-package-versions, retention, github-packages, untagged-images]
level: practitioner
status: docs-checked
description: "Prune GHCR container versions: untagged and old tags via actions/delete-package-versions or the REST API, protecting multi-arch children and signatures from deletion."
sources: ["https://github.com/actions/delete-package-versions", "https://docs.github.com/en/rest/packages/packages", "https://docs.github.com/en/packages/learn-github-packages/deleting-and-restoring-a-package"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cleaning up GHCR package versions

Every push of a moving tag (`main`, `latest`) can leave an older, untagged version behind in the
package. Prune them deliberately, because deletion is only reversible for 30 days.

## The multi-arch trap
A multi-platform image is a list of per-architecture images referenced from a single manifest
(GitHub Docs, "Labelling container images"). Before running any "delete untagged" job on a
repository that publishes multi-platform images, check that the job does not delete versions the
tagged index still references; a pull for one platform would then fail. Test on a throwaway
package first, and prefer a tool that understands indexes.

## Workflow with delete-package-versions
```yaml
name: ghcr-cleanup
on:
  schedule: [{ cron: "0 3 * * 0" }]
  workflow_dispatch:
jobs:
  clean:
    runs-on: ubuntu-24.04
    permissions: { packages: write }
    steps:
      - uses: actions/delete-package-versions@v5
        with:
          package-name: app
          package-type: container
          min-versions-to-keep: 50
          ignore-versions: '^(v\d+\.\d+\.\d+|latest|main)$'
```
- `package-type` is `container` for v5 or newer of the action (`docker` was the v4 value).
- `min-versions-to-keep` keeps the N latest versions and deletes the rest; it cannot be combined
  with `num-old-versions-to-delete`.
- `ignore-versions` takes a regex matched against the *version name*. Check what name your
  container versions carry before relying on it to protect release tags.
- `delete-only-untagged-versions: 'true'` (container packages only) deletes just untagged
  versions, optionally keeping N via `min-versions-to-keep`.
- The action deletes at most 100 versions per run.

## REST API by hand
```bash
gh api -H "Accept: application/vnd.github+json" \
  /orgs/ORG/packages/container/app/versions --paginate
gh api -X DELETE /orgs/ORG/packages/container/app/versions/PACKAGE_VERSION_ID
```
`per_page` defaults to 30 (max 100). Deleted versions can be restored within 30 days, and only if the
package namespace is still available (package settings or the restore endpoint,
`POST .../versions/PACKAGE_VERSION_ID/restore`).

## Gotchas
- For container packages the repository needs the **Admin** role under package settings >
  "Manage Actions access" for the workflow token to delete (README of the action).
- A public package cannot be deleted through the API if any version has more than 5,000 downloads
  (a specific public version likewise, if it has more than 5,000 downloads); contact GitHub Support.
- If you sign images, make sure your cleanup keeps the signature and attestation artifacts; check
  how your signing tool stores them before pruning.

## Checked
Checked 2026-10-28 against the README of actions/delete-package-versions and GitHub Docs (REST API
endpoints for packages, "Deleting and restoring a package", "Working with the Container registry"):
inputs and their combination rules, `container` vs `docker` package type, the 100-versions-per-run
cap, endpoint paths, `per_page`, the 30-day restore window, the 5,000-download limit and the Admin
role requirement. Removed because the pages do not state them: the exact "manifest unknown"
failure, the claim that `min-versions-to-keep` counts untagged children, the named community
cleanup action, the `sha256-<digest>.sig` tag convention and the jq field path.
Method: documentation only; no commands were run.
