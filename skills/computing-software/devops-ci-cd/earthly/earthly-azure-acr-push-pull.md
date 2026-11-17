---
id: computing-software.devops-ci-cd.earthly.earthly-azure-acr-push-pull
name: earthly-azure-acr-push-pull
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, azure-acr, az-acr-login, acrpush, service-principal, secret, save-image, push]
level: practitioner
status: docs-checked
description: "Push and pull Azure Container Registry images from Earthly: az acr login, the AcrPush role, service principal login with RUN --secret, and the 401 fix."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/registries/azure-acr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Push and pull Azure ACR images with Earthly

Goal: build an image and push it to Azure Container Registry (example registry `helloearthly`).

## Earthfile

No special handling; use `SAVE IMAGE --push`:

```
FROM alpine:3.18

build:
    RUN echo "Hello from Earthly!" > motd
    ENTRYPOINT cat motd
    SAVE IMAGE --push helloearthly.azurecr.io/hello-earthly:with-love
```

## Log in

ACR does not issue permanent credentials; it uses your Azure AD credentials. As an individual user log in first:

```
az acr login --name helloearthly
```

The ACR credential helper then keeps credentials current provided it is invoked again before they expire (config shows `"credsStore": "acr-linux"` in `.docker/config.json`). Service Principals and admin accounts also work; the admin account method is not recommended for production.

## Permissions and service principals

You need at least the `AcrPush` role. Service principals do not need `az acr login`; log in directly with docker:

```
RUN --secret AZ_USERNAME=earthly-technologies/azure/ci-cd-username \
    --secret AZ_PASSWORD=earthly-technologies/azure/ci-cd-password \
    docker login helloearthly.azurecr.io --username $AZ_USERNAME --password $AZ_PASSWORD
```

## Run and pull

Push with the `--push` flag: `earthly --push +build`.

Pull without special handling:

```
FROM earthly/dind:alpine-main

run:
    WITH DOCKER --pull helloearthly.azurecr.io/hello-earthly:with-love
        RUN docker run helloearthly.azurecr.io/hello-earthly:with-love
    END
```

Run with `earthly -P +run`.

## Gotcha

401 (authentication required): re-run `az acr login --name ...`. Azure recommends running it at the beginning of each automated script, so do it in CI runs too.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: guides/registries/azure-acr.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
