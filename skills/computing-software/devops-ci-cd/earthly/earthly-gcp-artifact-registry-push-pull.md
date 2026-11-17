---
id: computing-software.devops-ci-cd.earthly.earthly-gcp-artifact-registry-push-pull
name: earthly-gcp-artifact-registry-push-pull
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, gcp, artifact-registry, gcloud, configure-docker, save-image, push, service-account]
level: practitioner
status: docs-checked
description: "Push and pull GCP Artifact Registry images from Earthly: gcloud auth configure-docker, required Reader and Writer roles, service account key login, and GCR differences."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/registries/gcp-artifact-registry.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Push and pull GCP Artifact Registry images with Earthly

Goal: build an image and push it to Artifact Registry. Assumes `gcloud` is installed, the Artifact Registry API is enabled and a repository named `hello-earthly` exists.

## Earthfile

No special handling; use `SAVE IMAGE --push`:

```
FROM alpine:3.18

build:
    RUN echo "Hello from Earthly!" > motd
    ENTRYPOINT cat motd
    SAVE IMAGE --push <region>-docker.pkg.dev/<project>/hello-earthly/hello-earthly:with-love
```

## Credential helper

Artifact Registry does not issue permanent credentials; it derives Docker credentials from your Google credentials. `gcloud` has a built-in helper and can update your `.docker/config.json`:

```bash
gcloud auth configure-docker <region>-docker.pkg.dev
```

A sample resulting entry:

```
{
   "credHelpers": {
       "<region>-docker.pkg.dev": "gcloud"
 }
}
```

## Permissions

Add the `Artifact Registry Reader` and `Artifact Registry Writer` roles. For the older GCR, the needed permissions are based on GCP storage permissions; the guide used `Storage Admin` with GCR.

Service accounts work too. Instead of `gcloud init`, log in with the Google-provided key:

```
RUN gcloud auth activate-service-account --key-file /test/key.json
```

## Run and pull

Remember the push flag: `earthly --push +build`.

Pulling needs no special handling:

```
FROM earthly/dind:alpine-main

run:
    WITH DOCKER --pull <region>-docker.pkg.dev/<project>/hello-earthly/hello-earthly:with-love
        RUN docker run <region>-docker.pkg.dev/<project>/hello-earthly/hello-earthly:with-love
    END
```

Run it with `earthly -P +run`.

## Note on GCR

Artifact Registry succeeds Container Registry (GCR); most of this applies to GCR with some small tweaks, as listed in Google transition documentation.

## Checked

2026-11-07. Read docs/guides/registries/gcp-artifact-registry.md in full. Prerequisites, Earthfile, credential helper, roles, service account login, push and pull examples and GCR note match. Nothing removed.
Method: documentation only; no commands were run.
