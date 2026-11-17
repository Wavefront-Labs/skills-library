---
id: computing-software.devops-ci-cd.gitlab-ci.gitlab-pages-deployments
name: gitlab-pages-deployments
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, gitlab-pages, pages-keyword, pages-publish, pages-parallel-deployments, pages-access-control]
level: practitioner
status: docs-checked
description: "Publish static sites with GitLab Pages: the pages job, publish directory, parallel deployments with path_prefix, expiry and unique domains."
sources: ["https://docs.gitlab.com/user/project/pages/", "https://docs.gitlab.com/ci/yaml/#pages", "https://docs.gitlab.com/user/project/pages/parallel_deployments/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitLab Pages deployments

## 1. Minimal
```yaml
pages:
  stage: deploy
  image: node:22
  script:
    - npm ci && npm run build      # outputs to dist/
  pages:
    publish: dist                   # default is public/
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```
The `pages.publish` path is appended to `artifacts:paths` automatically from GitLab 17.10; when
`publish` is not set, the `public` directory is used.

## 2. Parallel deployments (preview per MR; Premium, Ultimate)
```yaml
pages-preview:
  script: npm run build              # pass the /mr-<iid>/ base path to your build tool
  pages:
    publish: dist
    path_prefix: "mr-$CI_MERGE_REQUEST_IID"
    expire_in: 1 week
  environment: { name: "pages/mr-$CI_MERGE_REQUEST_IID", url: $CI_PAGES_URL }
  rules: [{ if: $CI_PIPELINE_SOURCE == "merge_request_event" }]
```
Build tools must know the base path or assets 404. Parallel deployments expire after 24 hours by
default (`pages.expire_in` changes it, `never` disables expiry). A `path_prefix` such as `documents`
overrides a same-named path of the main deployment, and the last Pages job to finish for a given
prefix is the one deployed.

## 3. Settings that matter
- New projects use Pages **unique domains** by default, so projects in a group do not share
  cookies; clear *Use unique domain* to opt out.
- Pages hosts static sites only: server-side processing (`.php`, `.asp`) is not supported.
- Access control, custom domains, redirects and size limits: see the GitLab Pages docs for your version.

## 4. Gotchas
- A stopped, expired or deleted deployment returns a 404 at its URL until another deployment with the same URL configuration is created.

## Verify
- [ ] Deploy → Pages shows the active deployment and URL; asset paths load with the correct base.

## Checked
2026-10-31. Confirmed in the GitLab docs pages for Pages, parallel deployments and the CI/CD YAML reference: tiers, `pages.publish` default and 17.10 artifacts behaviour, `path_prefix`, `expire_in`, 24-hour parallel-deployment expiry, unique-domain default, static-only support.
Removed (not found in the fetched pages): `pages:deploy` step name, access-control menu path, custom-domain TXT record name, `_redirects` details, the 1 GB limit, `404.html` and pre-compression advice, the `--base` flag.
Method: documentation only; no commands were run.
