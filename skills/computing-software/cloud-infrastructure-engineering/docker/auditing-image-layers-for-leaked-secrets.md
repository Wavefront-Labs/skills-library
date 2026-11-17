---
id: computing-software.cloud-infrastructure-engineering.docker.auditing-image-layers-for-leaked-secrets
name: auditing-image-layers-for-leaked-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, layer-inspection, layer-secrets-audit, whiteout, trufflehog, trivy-secret, image-history]
level: advanced
status: docs-checked
description: "Find secrets hidden in earlier image layers (deleted files survive behind whiteouts) with docker save, trufflehog/trivy, history args and provenance."
sources: ["https://github.com/opencontainers/image-spec/blob/main/layer.md#whiteouts", "https://github.com/trufflesecurity/trufflehog#docker", "https://trivy.dev/latest/docs/scanner/secret/", "https://docs.docker.com/reference/cli/docker/image/history/", "https://docs.docker.com/build/metadata/attestations/slsa-provenance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing image layers for leaked secrets

`RUN rm secret.txt` adds a **whiteout** file (`.wh.secret.txt`) in a new layer. The OCI image spec
defines a whiteout as the prefix `.wh.` plus the basename of the path to delete. The merged
filesystem hides the file, but the original layer still contains it and anyone with pull
access can extract it.

## 1. Quick scanners
```bash
trivy image --scanners secret myapp:1.4
trufflehog docker --image myapp:1.4 --results=verified
```
- Trivy's `--scanners` accepts `vuln`, `misconfig`, `secret` and `license` (default `vuln,secret`).
  Its secret page says Trivy tries to detect the base image and skip those layers for secret
  scanning; use `--debug` to see base layers if a secret is not found. The page does not say
  that deleted files in your own layers are reported, so confirm that with a planted test secret.
- TruffleHog's `docker` source takes `--image` (repeatable) and accepts a registry reference,
  `docker://name:tag` for the local daemon, or `file://path.tar` for an image saved as a tarball.

## 2. Manual layer walk
Save the image with `docker save -o img.tar myapp:1.4` (it writes a tar archive containing all
parent layers), unpack it, and list the entries of each layer tarball with `tar -t`, searching
for names such as `.env`, `.pem`, `id_rsa`, `.npmrc`, `credentials` and `.git/`. The cited pages
do not document the archive layout, so inspect it rather than assuming file names.
- Entries named `.wh.<name>` show something was deleted in that layer; look for `<name>` in an
  earlier layer and extract it to confirm.
- `.wh..wh..opq` is an opaque whiteout: it hides all siblings in the lower layers.
- The dive tool (`wagoodman/dive`) lets you browse each layer's contents and shows files
  changed, added or removed per layer.

## 3. Metadata, not just files
```bash
docker history --no-trunc --format '{{.CreatedBy}}' myapp:1.4 | grep -iE 'token|pass|secret|key='
docker buildx imagetools inspect reg.example.com/myapp:1.4 --format '{{json .Provenance}}'
```
`docker history` supports `--no-trunc` and a Go template with the `.CreatedBy` placeholder.
With provenance `mode=max`, build argument values are included in the attestation (Docker's
docs warn about this and say to use secret mounts instead of build arguments for secrets);
`min` mode omits them.

## If you find one
1. Rotate the credential. Deleting tags does not revoke what was already pulled or cached.
2. Fix the build (secret mounts, `.dockerignore`), rebuild, push.
3. Delete old digests from every registry and pull-through cache; purge CI cache refs.
4. Add `trivy image --scanners secret --exit-code 1` to CI (`--exit-code` sets the exit code
   used when security issues are found).

## Gotchas
- Multi-stage builds only protect you if the secret never enters the **final** stage.

## Checked

Checked 2026-11-09 against the OCI image-spec layer page (whiteouts and opaque whiteout), the Trivy secret scanner page and the `trivy image` CLI reference (`--scanners`, `--exit-code`), the TruffleHog README (docker source, `--results=verified`), the `docker image history`, `docker image save` and `docker buildx imagetools inspect` references, the Docker SLSA provenance page (mode=max exposes build argument values) and the dive README. Removed: the claim that Trivy scans every layer including deleted files (its page says base layers are skipped), the old `--only-verified` flag (not in the README), the manifest.json jq loop and containerd layout notes (archive layout not documented in the cited pages), the claim that cache export with `mode=max` includes earlier stages, and the claim that dive is not for CI.

Method: docs-checked 2026-11-09 against the pages listed above; no commands were run.
