---
id: computing-software.devops-ci-cd.gitlab-ci.container-registry-auth-with-ci-variables
name: container-registry-auth-with-ci-variables
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, ci-registry-password, ci-registry-image, ci-job-token-registry, deploy-token-registry, dependency-proxy-auth]
level: intro
status: docs-checked
description: "Authenticate to the GitLab container registry in CI with CI_REGISTRY_* job-token variables, cross-project pulls via the job token allowlist, and deploy tokens for clusters."
sources: ["https://docs.gitlab.com/user/packages/container_registry/authenticate_with_container_registry/", "https://docs.gitlab.com/ci/jobs/ci_job_token/", "https://docs.gitlab.com/user/project/deploy_tokens/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry auth with CI_REGISTRY variables

## 1. Predefined variables
| Variable | Value |
|---|---|
| `CI_REGISTRY` | registry server address, `<host>[:<port>]`, for example `registry.gitlab.example.com` |
| `CI_REGISTRY_IMAGE` | base address for the project's images, `<host>[:<port>]/<project_full_path>` |
| `CI_REGISTRY_USER` | per-job user with read-write access to the project's registry |
| `CI_REGISTRY_PASSWORD` | the same value as `CI_JOB_TOKEN`, valid only while the job runs |

The registry variables exist only when the container registry is enabled.
```bash
echo "$CI_REGISTRY_PASSWORD" | docker login "$CI_REGISTRY" -u "$CI_REGISTRY_USER" --password-stdin
docker push "$CI_REGISTRY_IMAGE/api:$CI_COMMIT_SHORT_SHA"     # image names must follow the registry naming convention
```

## 2. Pulling another project's images
The job token has read and write access to the registry of the project that runs the job; the
CI/CD job token allowlist controls access to other projects' registries. The target project
lists the pulling project under **Settings > CI/CD > Job token permissions** (the setting was
renamed to *CI/CD job token allowlist* in GitLab 17.3).

## 3. Outside CI (Kubernetes pulls, other systems)
Create a **deploy token** with the `read_registry` scope (read-only access to the project's
registry images). By default a deploy token does not expire; you can set an expiry date. A
deploy token named exactly `gitlab-deploy-token` is exposed to CI jobs as `CI_DEPLOY_USER` /
`CI_DEPLOY_PASSWORD`, which GitLab recommends for long-lived registry access:
```bash
kubectl create secret docker-registry gitlab-pull -n app \
  --docker-server="$CI_REGISTRY" --docker-username="$CI_DEPLOY_USER" --docker-password="$CI_DEPLOY_PASSWORD"
```
Never put `CI_REGISTRY_PASSWORD` into a pull secret: it is valid only while the job runs.

## 4. Dependency proxy
Pull images through the Dependency Proxy with the group image prefix:
`image: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}/node:22`. Credentials are `CI_DEPENDENCY_PROXY_USER` and `CI_DEPENDENCY_PROXY_PASSWORD`; the server is `CI_DEPENDENCY_PROXY_SERVER`.

## Verify
- [ ] Push works with no stored credential; pod pulls work after the job ended.

## Checked

2026-10-31. Confirmed against the GitLab predefined variables page, the container registry authentication page, the CI/CD job token page and the deploy tokens page: `CI_REGISTRY*` descriptions, the `CI_JOB_TOKEN` equivalence and lifetime, allowlist behaviour and the 17.3 rename, `read_registry` scope, default no expiry, `gitlab-deploy-token` and `CI_DEPLOY_*`, Dependency Proxy variables. Removed: the fixed `gitlab-ci-token` username for `CI_REGISTRY_USER`, the 3-level path limit, the error text, ImagePullBackOff and rate-limit claims, and the automatic proxy auth claim (not in the pages).

Method: documentation only; no commands were run.
