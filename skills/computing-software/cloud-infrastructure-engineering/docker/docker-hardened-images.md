---
id: computing-software.cloud-infrastructure-engineering.docker.docker-hardened-images
name: docker-hardened-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, base-image, docker-hardened-images, dhi, minimal-images, slsa, vex, nonroot]
level: practitioner
status: docs-checked
description: "Adopt Docker Hardened Images (DHI): runtime vs dev variants, nonroot defaults, multi-stage migration, and verifying SBOM, VEX and provenance attestations."
sources: ["https://docs.docker.com/dhi/", "https://docs.docker.com/dhi/explore/available/", "https://docs.docker.com/dhi/migration/checklist/", "https://docs.docker.com/dhi/how-to/verify/", "https://docs.docker.com/dhi/how-to/scan/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Hardened Images (DHI)

DHI are Docker-maintained, minimal-by-design images built to SLSA Build Level 3, shipped with
signed SBOMs, VEX documents and provenance. Debian-based (glibc) and Alpine-based (musl)
variants exist. The DHI Community images are pulled from `dhi.io` after `docker login dhi.io`;
organisation catalog access (mirrored repositories) depends on your plan, so check the DHI docs.

## Variants and tags
| Variant | Contents | Use |
|---|---|---|
| runtime (default tag) | no shell, no package manager, runs as nonroot | final stage |
| `-dev` / `sdk` | shell, package manager, root user | build stages, debugging |
| `-fips` (some images) | FIPS 140 validated crypto modules | regulated environments |

Example tags from the docs: `3.9.23-debian12`, `3.9.23-alpine3.21`, `3.9.23-debian12-dev`,
`3.13-fips`, `3.9.23-debian12-fips`.

## Migration pattern
```dockerfile
# syntax=docker/dockerfile:1
FROM dhi.io/python:3.13-dev AS build
WORKDIR /app
RUN python -m venv /app/venv
ENV PATH=/app/venv/bin:$PATH
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM dhi.io/python:3.13
WORKDIR /app
COPY --from=build /app /app
ENV PATH=/app/venv/bin:$PATH
ENTRYPOINT ["python", "-m", "myapp"]
```
Migration checklist (DHI docs):
- Install packages only in `dev` build stages (`apk` or `apt`) and copy artifacts to the
  runtime stage; drop steps that install ca-certificates (included).
- Runtime images have no shell: move `RUN`/`SHELL` steps to build stages, use exec form.
- Default user is nonroot (UID 65532): make files readable/writable by it.
- Listen on port 1025 or higher (privileged ports fail for nonroot on Kubernetes or Docker
  Engine older than 20.10).
- Check the image's entry point with `docker inspect` and adjust `ENTRYPOINT`/`CMD`.

## Verify what you pull
```bash
docker scout attest list dhi.io/<image>:<tag>          # SBOM, provenance, VEX attestations
docker scout cves dhi.io/<image>:<tag>                 # VEX-aware results
docker scout vex get dhi.io/<image>:<tag> --output vex.json
grype dhi.io/<image>:<tag> --vex vex.json
trivy image --scanners vuln --vex vex.json dhi.io/<image>:<tag>
```
The verify page also documents `cosign` for verifying attestation signatures.

## Gotchas
- Scanners without VEX support report CVEs that DHI marks not affected. Grype uses `--vex`;
  Trivy takes a local VEX file or VEX Hub (`--vex repo`, recommended by the docs).
- Debug with `docker debug` or a `-dev` tag, not by adding a shell to the runtime stage.

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23) DHI pages: what, available,
get-started, migration checklist, verify, scan. Confirmed: SLSA Build Level 3, variants and
tag examples, `dhi.io` login, nonroot UID 65532, port and ca-certificates guidance, the
scout/grype/trivy commands. Removed as unconfirmed: the "vendor SLA" claim, "Debian- or
Alpine-based only" exclusivity, `-fips` cosign admission-policy advice, mirrored-repository
credentials advice.
Method: documentation only; no commands were run.
