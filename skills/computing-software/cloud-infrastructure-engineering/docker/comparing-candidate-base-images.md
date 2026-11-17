---
id: computing-software.cloud-infrastructure-engineering.docker.comparing-candidate-base-images
name: comparing-candidate-base-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, base-image, base-image-comparison, scout-compare, trivy, syft, image-size, cve]
level: practitioner
status: docs-checked
description: "Choose between base images with evidence: compressed layer size, package count, fixable CVE counts by severity, platforms, and docker scout compare, quickview and recommendations."
sources: ["https://docs.docker.com/reference/cli/docker/scout/compare/", "https://docs.docker.com/reference/cli/docker/scout/quickview/", "https://docs.docker.com/reference/cli/docker/scout/recommendations/", "https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/", "https://trivy.dev/latest/docs/target/container_image/", "https://trivy.dev/docs/latest/configuration/filtering/", "https://trivy.dev/docs/latest/configuration/reporting/", "https://oss.anchore.com/docs/reference/syft/cli/", "https://github.com/anchore/syft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparing candidate base images

Decide with numbers, not reputation. Build the real app on each candidate where possible;
base-only numbers miss what your packages pull in.

## Criteria table to fill
| Criterion | How to measure |
|---|---|
| Compressed pull size | `docker buildx imagetools inspect --raw <img>` prints the raw JSON manifest; for a single-platform manifest each entry in `layers` has a `size`. A multi-platform tag returns a manifest list, so inspect the per-platform manifest it points to |
| Local size | `docker image ls <img>` (SIZE column) |
| Package count | `syft <img> -o json \| jq '.artifacts \| length'` |
| CVEs (critical/high, fixable) | `trivy image --format json --severity CRITICAL,HIGH --ignore-unfixed <img>` or `docker scout cves --only-severity critical,high --only-fixed <img>` |
| libc / shell / package manager | `docker run --rm --entrypoint sh <img> -c 'ldd --version; ls /bin'` (fails on images that ship no shell, which is itself a finding) |
| Platform coverage | `docker buildx imagetools inspect <img>` lists each manifest with its `Platform:` |
| Provenance / SBOM attestations | `docker buildx imagetools inspect <img> --format '{{json .Provenance}}'` and `--format '{{json .SBOM}}'` |
| Update cadence and EOL | the image publisher's own release notes |

## Script
```bash
for img in node:22-bookworm node:22-bookworm-slim node:22-alpine; do
  docker pull "$img" >/dev/null
  docker image ls "$img"
  syft "$img" -o json | jq '.artifacts | length'
  trivy image --format json --severity CRITICAL,HIGH --ignore-unfixed "$img" \
    | jq '[.Results[]?.Vulnerabilities[]?] | length'
done
```
Docker Scout side-by-side:
```bash
docker scout compare --to node:22-bookworm node:22-bookworm-slim
docker scout quickview node:22-alpine
docker scout recommendations myapp:latest     # base image refresh and update recommendations
```
`docker scout compare` is marked experimental, and its page says it is intended to compare
two versions of the same image (for example a new build against the one in production), so
treat a cross-distro comparison as a rough guide. `quickview` summarises the image's
vulnerabilities and those from its base image; `recommendations` shows base image refresh and
update recommendations, and takes `--only-refresh` or `--only-update`.

## Reading the numbers
- Count **fixable** critical/high: `--ignore-unfixed` (Trivy) and `--only-fixed` (Scout) both
  restrict output to vulnerabilities with a fix.
- Fewer packages beats fewer CVEs today: CVE counts change as advisories are published, the
  package list does not.
- Images with a different libc, no shell or no package manager shift cost into compatibility
  and debugging; include that in the decision, not just size.
- Run the app's test suite on the winner; size wins that break DNS or locale handling are not wins.

## Record the decision
Write the table and date into an ADR next to the Dockerfile; revisit on major runtime bumps
or when the chosen base nears EOL.

## Checked
Date: 2026-11-07
Pages read: docker scout compare, quickview and recommendations CLI pages (full); buildx imagetools inspect
(description, options, `--format` field list, the Provenance and `--raw` examples; the other long JSON
examples skimmed, not read line by line); Trivy filtering page (`--severity`, `--ignore-unfixed`, JSON
`Results`/`Vulnerabilities` structure) and reporting page (`--format json`); Trivy container image page
(sections searched for `image` usage; it does not itself document `--format`/`--severity`);
Syft CLI reference (`syft scan <img> -o json` example; the bare `syft <img>` form is from the Syft README) and the Syft JSON format guide (`artifacts` key, large page searched not read in full);
docker scout cves page (option rows only: `--only-severity`, `--only-fixed`); docker run `--entrypoint`
option; docker image ls page (SIZE column).
Trimmed: the `docker image inspect -f '{{.Size}}'` and `{{.Config.User}}` templates and the Default-user row
(field names not on any cited page), `cosign verify`, endoflife.date, Trivy `-q`, Alpine "musl" and
distroless "no shell" asides, and the Chainguard image in the loop (no cited page). Added a note that
`docker scout compare` is experimental and aimed at same-image comparisons. The Syft README was read in full.
Method: documentation only; no commands were run.
