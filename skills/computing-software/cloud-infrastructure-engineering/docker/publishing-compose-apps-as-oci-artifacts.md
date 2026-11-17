---
id: computing-software.cloud-infrastructure-engineering.docker.publishing-compose-apps-as-oci-artifacts
name: publishing-compose-apps-as-oci-artifacts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, compose-publish, compose-oci, oci-artifacts, image-pinning, release]
level: advanced
status: docs-checked
description: "Publish a Compose application to a registry with docker compose publish: digest pinning, environment handling, what blocks publishing, and consuming it with oci://."
sources: ["https://docs.docker.com/reference/cli/docker/compose/publish/", "https://docs.docker.com/compose/how-tos/oci-artifact/", "https://docs.docker.com/compose/trust-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing Compose apps as OCI artifacts

`docker compose publish` pushes the Compose application to an OCI-compliant registry as an
OCI artifact, so others can run it with `docker compose -f oci://... up`. The Docker docs
feature banner says this needs Docker Compose 2.34.0 or later.

## Publish
```bash
docker login reg.example.com
docker compose build && docker compose push            # images first
docker compose publish --resolve-image-digests reg.example.com/stacks/shop:1.4.0
docker compose -f compose-base.yml -f compose-production.yml publish reg.example.com/stacks/shop:1.4.0
```
Flags from the `publish` reference:
| Flag | Effect |
|---|---|
| `--resolve-image-digests` | Pin image tags to digests |
| `--with-env` | Include environment variables in the published artifact |
| `-y` / `--yes` | Assume "yes" to all prompts (non-interactive publishing) |
| `--oci-version` | OCI image/artifact specification version (determined automatically by default) |
| `--app` | Published compose application (includes referenced images) |

Compose checks for sensitive data in the configuration and shows the environment variables
for confirmation; declining stops the publish before anything is sent. The OCI artifact page
lists limitations: you cannot publish a configuration with services containing bind mounts,
with services that contain only a `build` section, or one that includes local files with
`include` (publish the included files too and reference them as remote includes).
Overrides, `extends` and `include` are otherwise supported.

## Consume
```bash
docker compose -f oci://docker.io/username/my-compose-app:latest config
docker compose -f oci://docker.io/username/my-compose-app:latest up -d
```
When you run an application from an OCI artifact, Compose may ask you to confirm the
interpolation variables with their values and sources, the environment variables the
application uses, and any other remote resources it includes. Compose then reports the local
directory where the artifact's resources were downloaded. Review these prompts as described
in the Compose trust model.

## Release practice
- Version stacks and avoid reusing tags; use `--resolve-image-digests` so consumers get the
  exact images.
- Keep secrets out of the artifact: check what `--with-env` would include before publishing.

## Gotchas
- Older Compose versions lack `publish`; check `docker compose publish --help`.
- Variables not embedded in the artifact must be supplied by the consumer (shell
  environment, `--env-file`).

## Checked
Date 2026-10-23. Documentation release: Compose v5.6.1 CLI reference and Docker docs
(docker/docs main). Method: documentation only; no commands were run.
Confirmed in the `publish` reference and the OCI artifact how-to: flag list and descriptions,
the 2.34.0 requirement, sensitive-data and environment-variable confirmation prompts,
publishing limitations (bind mounts, build-only services, local `include`), `oci://` usage,
and the consumer prompts. Corrected: an earlier claim that `include`d files are published
along with the artifact. Removed: registry compatibility lists, cosign signing advice and the
`-p shop` project-name example.
