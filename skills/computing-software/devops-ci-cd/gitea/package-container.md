---
id: computing-software.devops-ci-cd.gitea.package-container
name: package-container
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-container-registry, gitea, oci-image, docker-login, image-naming, container-push-pull]
level: practitioner
status: docs-checked
description: "Use the Gitea container registry with docker: login with a token, the registry/owner/image naming convention, case-insensitive tags, push and pull."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/packages/container.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea container registry

Publishes OCI-compliant images for a user or organization; works with Docker and Helm charts. Examples use `docker`.

## Login
```shell
docker login gitea.example.com
```
With 2FA or OAuth, use a personal access token in place of the password.

## Naming
`{registry}/{owner}/{image}` where registry is your Gitea domain. Valid for owner `testuser`: `gitea.example.com/testuser/myimage`, `.../my-image`, `.../my/image`.
```shell
docker build -t {registry}/{owner}/{image}:{tag} .
docker tag {some-existing-image}:{tag} {registry}/{owner}/{image}:{tag}
```
**Tags are case-insensitive**: `image:tag` and `image:Tag` are the same.

## Push and pull
```shell
docker push gitea.example.com/testuser/myimage:latest
docker pull gitea.example.com/testuser/myimage:latest
```
In Actions, `GITEA_TOKEN` cannot push to the package registry; use a personal access token (see `gitea-actions-vs-github`).

## Checked
2026-11-03. Login, naming, case-insensitive tags and push/pull confirmed against the Gitea docs page container.md; the GITEA_TOKEN limitation confirmed against comparison.md (raw markdown, gitea/docs main branch). Removed: access-rule, cleanup-rule, always-keeps-latest, private-owner pull and /v2 proxy claims, and the package-permission note, none of which are on those pages.
Method: documentation only; no commands were run.
