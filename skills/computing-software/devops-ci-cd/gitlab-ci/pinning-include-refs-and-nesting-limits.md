---
id: computing-software.devops-ci-cd.gitlab-ci.pinning-include-refs-and-nesting-limits
name: pinning-include-refs-and-nesting-limits
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, include-ref, include-nesting, include-integrity, include-limits, template-versioning]
level: practitioner
status: docs-checked
description: "Pin project includes to tags or SHAs so template changes cannot break or hijack pipelines, use integrity hashes for remote includes, and stay within include limits."
sources: ["https://docs.gitlab.com/ci/yaml/#includeproject", "https://docs.gitlab.com/ci/yaml/includes/", "https://docs.gitlab.com/ci/yaml/#includeintegrity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pinning include refs and nesting limits

## 1. Pin project includes
```yaml
include:
  - project: platform/ci-templates
    ref: v3.4.1                      # tag; or a full commit SHA for immutability
    file:
      - /templates/build.yml
      - /templates/deploy.yml
```
Without `ref`, GitLab uses the template project's **default branch HEAD** — every merge to the
templates repo changes every consumer pipeline instantly, including a malicious one.
- Tags can be moved; SHAs cannot. Protect `v*` tags in the template project.

## 2. Remote includes
```yaml
include:
  - remote: https://example.com/ci/scan.yml
    integrity: sha256-L3/GAoKaw0Arw6hDCKeKQlV1QPEgHYxGBHsH4zG1IY8=
```
`integrity` (SRI hash) fails the pipeline if the file changes. Without it, remote includes are
unpinned code execution. Compute: `curl -s URL | openssl dgst -sha256 -binary | openssl base64 -A`.

## 3. Limits
- Max includes per pipeline (nested ones count, the same file twice counts twice): 150 by
  default; GitLab Self-Managed admins can change the maximum.
- The time limit to resolve all included files is 30 seconds.
- Included files are merged in order (nested includes first), then the main file is merged over them.
  Hash maps merge at any depth; arrays such as `rules` are not merged and the top-level file wins.
- Rerunning a job does not refetch includes; rerunning a pipeline does.

## Verify
- [ ] Every `project:` include has a `ref:`; every `remote:` include has `integrity:`.
- [ ] Merging a breaking change to templates main does not affect consumer pipelines.

## Checked

2026-10-31. Confirmed against the GitLab CI YAML reference and the includes page: include:project ref defaults to the project HEAD and may be a branch, tag or commit SHA, include:integrity takes a sha256 hash and fails the pipeline on mismatch, the 150 include limit (nested and duplicates counted, self-managed maximum changeable), the 30 second resolve limit, merge order and deep merge rules, rerun behaviour, and the advice to use protected branches and tags for a project you own.
Removed: the ci_max_includes setting name, the Renovate claim, the nested local-path claim, and the pipeline editor debug section.

Method: documentation only; no commands were run.
