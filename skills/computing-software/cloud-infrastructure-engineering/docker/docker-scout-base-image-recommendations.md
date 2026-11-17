---
id: computing-software.cloud-infrastructure-engineering.docker.docker-scout-base-image-recommendations
name: docker-scout-base-image-recommendations
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-scout, base-image, scout-recommendations, base-image-recommendation, scout-cves, scout-compare, scout-quickview, base-image-refresh]
level: practitioner
description: "Use docker scout recommendations, quickview and compare to pick a base image refresh or change that removes the most CVEs, and read what the output does and does not tell you."
sources: ["https://docs.docker.com/reference/cli/docker/scout/recommendations/", "https://docs.docker.com/reference/cli/docker/scout/compare/", "https://docs.docker.com/reference/cli/docker/scout/cves/", "https://github.com/docker/scout-action", "https://docs.docker.com/scout/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker Scout base image recommendations

**Goal:** answer "which base image should I move to, and how many CVEs does that remove"
with data rather than folklore.

## Commands
```sh
docker scout quickview myapp:1.4                 # CVE summary of image and its base
docker scout recommendations myapp:1.4           # refresh + change options for the base
docker scout recommendations myapp:1.4 --only-refresh   # base image refresh recommendations only
docker scout recommendations myapp:1.4 --only-update    # base image update recommendations only
docker scout compare myapp:1.4 --to myapp:1.5    # CVE/package diff between two images
docker scout cves --only-fixed --only-severity critical,high myapp:1.4
```
`recommendations` accepts images, OCI layout directories, tarball archives (as created by
`docker save`) and local directories or files, with the prefixes `image://` (default; local image,
falling back to a registry lookup), `local://`, `registry://`, `oci-dir://`, `archive://` and `fs://`.
Other useful options: `--platform`, `--org`, `--output` (write the report to a file) and `--ref` (for
tarballs holding multiple references).

## Reading the output
Two sections:
- **Refresh base image** — recommendations to refresh the base image you already use
  (`--only-refresh` shows only these).
- **Change/update base image** — alternative base images (`--only-update` shows only update
  recommendations). These are suggestions, not tested migrations: a different distribution or
  libc, or a newer major release, can change behaviour, so test before adopting.

Compare the vulnerability counts by severity and the package counts the report shows for each
option.

## In CI
```yaml
- uses: docker/scout-action@v1
  with:
    command: cves,recommendations
    image: ${{ env.IMAGE }}
    only-severities: critical,high
    exit-code: true
```
The action's `command` input takes a comma-separated list and runs the commands in order,
stopping the step if one exits non-zero. `only-severities` filters CVEs by severity; `exit-code`
(default `false`) makes the action return exit code `2` if vulnerability changes are detected;
`write-comment` (default `true`) writes the Scout output as a pull request comment.

## Gotchas
- Vulnerability counts differ between scanners; compare deltas from the same tool rather than
  absolutes across tools.
- A recommendation is about the base image's vulnerabilities and packages; test your application
  (native dependencies in particular) before changing the base.
- `docker scout cache prune` exists to clear Scout's local cache if results look stale.

## Verify
After rebasing, `docker scout compare old --to new` shows the expected CVE reduction and no
new packages you did not intend; `docker scout quickview new` shows the base now matched to
the intended tag.

## Checked

Date: 2026-10-24. Documentation release: `docker scout recommendations`, `cves`, `compare` references and docker/scout-action README (docker/docs, docker/scout-action main).
Confirmed: recommendations options (`--only-refresh`, `--only-update`, `--platform`, `--org`, `--output`, `--ref`), supported artifact
types and prefixes, `cves` options `--only-fixed` and `--only-severity`, `compare --to`, the scout-action inputs and
defaults (`command`, `only-severities`, `exit-code` default false returning exit code 2 on detected vulnerability changes,
`write-comment` default true), and the `cache prune` command. Corrected: the action's `exit-code` returns 2 when
vulnerability changes are detected (not "fails on unfixed critical/high CVEs"), and `--tag` is not a base-image override.
Removed: free-tier limits, the base detection and provenance explanation, Renovate and size-threshold advice,
and the CVE-source statement, none of which the checked pages state.

Method: documentation only; no commands were run.
