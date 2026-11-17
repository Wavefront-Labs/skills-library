---
id: computing-software.devops-ci-cd.gitlab-ci.environment-names-slugs-and-folders
name: environment-names-slugs-and-folders
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, ci-environment-slug, environments, review-apps]
level: practitioner
status: docs-checked
description: "Name dynamic GitLab environments with folder prefixes and CI_ENVIRONMENT_SLUG so URLs, namespaces and DNS stay valid; slug length rules and collisions."
sources: ["https://docs.gitlab.com/ci/environments/", "https://docs.gitlab.com/ci/variables/predefined_variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment naming, CI_ENVIRONMENT_SLUG and folders

```yaml
review:
  script: ./deploy --namespace "review-$CI_ENVIRONMENT_SLUG" --host "$CI_ENVIRONMENT_SLUG.review.example.com"
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_ENVIRONMENT_SLUG.review.example.com
    on_stop: stop_review
```

## Folders
A static prefix in the name, such as `review/`, groups all environments with that prefix
in the UI: `review/feature-x` sits in folder `review`.

## Slugs
- `CI_ENVIRONMENT_SLUG`: the simplified environment name, suitable for DNS, URLs and
  Kubernetes labels; available when `environment:name` is set. The slug is truncated to
  **24 characters**, and a random suffix is added automatically to uppercase environment names.
- `CI_COMMIT_REF_SLUG`: `CI_COMMIT_REF_NAME` lowercased, shortened to 63 bytes, everything
  except `0-9` and `a-z` replaced with `-`, no leading or trailing `-`. Different branch names
  can map to the same slug (`feature/a_b` and `feature/a-b` both become `feature-a-b`).
- Prefer `CI_ENVIRONMENT_SLUG` for hostnames and namespaces.

## Gotchas
- Some characters cannot be used in environment names; see the `environment` keyword reference.
- Changing the naming pattern leaves the old environments behind; stop them (the `on_stop` job
  with `action: stop`) or delete them.
- A stop job that needs repository files should run in merge request pipelines so runners can
  fetch the repository after the feature branch is deleted.

## Verify
- [ ] Environments page shows the folder; URL opens; namespace name equals the slug.

## Checked

2026-10-28. Confirmed against the GitLab predefined variables page (CI_ENVIRONMENT_SLUG truncated to 24 characters with a random suffix on uppercase names; CI_COMMIT_REF_SLUG rules) and the dynamic environments page (static prefix groups environments, `name`/`url` with the slug variables, `on_stop` and `action: stop`, stop jobs in merge request pipelines). Corrected: the suffix applies to uppercase names, not to every truncated slug. Removed: the allowed-character list for `environment:name`, the variable-expansion claim, and the DNS label remark (not in the fetched pages).

Method: documentation only; no commands were run.
