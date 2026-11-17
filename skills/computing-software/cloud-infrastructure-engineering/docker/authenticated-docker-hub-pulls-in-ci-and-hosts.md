---
id: computing-software.cloud-infrastructure-engineering.docker.authenticated-docker-hub-pulls-in-ci-and-hosts
name: authenticated-docker-hub-pulls-in-ci-and-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, rate-limit, authenticated-pulls, docker-login, docker-hub, personal-access-token, imagepullsecrets]
level: practitioner
status: docs-checked
description: "Avoid Docker Hub pull limits by authenticating everywhere images are pulled: CI runners, buildx builders, Docker hosts and Kubernetes nodes, using read-only access tokens."
sources: ["https://docs.docker.com/docker-hub/usage/", "https://docs.docker.com/security/for-developers/access-tokens/", "https://docs.docker.com/reference/cli/docker/login/", "https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authenticated Docker Hub pulls

Unauthenticated Docker Hub pulls are limited to 100 per 6 hours per IPv4 address or IPv6 /64 subnet, so
shared NAT (CI runners, office networks, cloud NAT gateways) hits the limit fast. Authenticated Personal
accounts get 200 per 6 hours; Pro, Team and Business are unlimited, subject to fair use. Confirm the current
table in the Docker Hub usage documentation, because limits change.

## Token

Create a **Personal Access Token** (or an Organization Access Token) with the lowest permission that covers
the job. For a PAT the repository permission is **Repo Public Read-only** (the default: public images only)
or **Repo Read-only** (public plus private repositories you can access). Organization access tokens use
scopes such as Image Pull. Never use the account password in automation.

## CI

```yaml
# GitHub Actions: before any build or docker pull
- uses: docker/login-action@v4
  with:
    username: ${{ vars.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

```yaml
# GitLab CI
before_script:
  - echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
```

Base images pulled **during a build** (`FROM node:22`) need credentials too, so log in in the same
environment that runs the build.

## Docker hosts

```bash
echo "$TOKEN" | docker login -u svc-pull --password-stdin
```

`docker login` stores the credentials in the `config.json` of the user running the CLI. Without a credential
helper they are only base64-encoded, which Docker describes as less secure, so protect the runner. Log in as
the user that runs `docker pull` or Compose. With Docker Swarm, deploy with `--with-registry-auth` so
workers receive the credentials.

## Kubernetes nodes

```bash
kubectl create secret docker-registry dockerhub   --docker-server=https://index.docker.io/v1/   --docker-username=svc-pull --docker-password="$TOKEN" -n app
kubectl patch serviceaccount default -n app -p '{"imagePullSecrets":[{"name":"dockerhub"}]}'
```

The Kubernetes documentation uses `https://index.docker.io/v1/` as the Docker Hub server. Alternatively
authenticate a mirror or pull-through cache once and point nodes at it, which avoids secrets in every
namespace.

## Check remaining quota

```bash
TOKEN=$(curl -s --user "$HUB_USER:$HUB_SECRET" "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
curl -s --head -H "Authorization: Bearer $TOKEN" https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest | grep -i ratelimit
```

A HEAD request returns the limit headers without counting against the limit; a GET emulates a real pull and
counts.

## Gotchas

- With the exception of `GITHUB_TOKEN`, secrets are not passed to the runner when a workflow is triggered
  from a forked repository, so those builds pull anonymously. Use a mirror for them.
- Third-party platforms may use one IPv4 address or IPv6 /64 subnet for many users; even authenticated pulls
  from it can hit Docker Hub's abuse rate limit.
- Pull attribution: pulls from authenticated users go to a personal or organization namespace depending on
  domain affiliation and membership, so authenticate to be attributed correctly.

## Checked

2026-10-26. Documentation release: docker/docs main (Docker Hub usage, pull limits and access token reference pages), docker/cli login reference, docker/login-action README (latest release v4.7.0, 2026-10-23), Kubernetes website docs and GitHub Docs, checked 2026-10-26. Confirmed: 100 / 200 / unlimited pull limits per 6 hours, IPv4 or IPv6 /64 basis, PAT repository permission names (Repo Public Read-only default, Repo Read-only), docker/login-action major version v4 and its username/password inputs, docker login storing base64-encoded credentials in config.json, Swarm --with-registry-auth, kubectl secret docker-server value for Docker Hub, serviceaccount patch from the Kubernetes docs, rate-limit header check with HEAD not counting, forked-workflow secrets rule, abuse rate limit note. Removed unconfirmed claims: buildx reading the client config for docker-container builders, root's config for systemd services, keychain storage on Docker Desktop, and pull_request_target advice. Fixed: the PAT scope name and the login-action major version.

Method: documentation only; no commands were run.
