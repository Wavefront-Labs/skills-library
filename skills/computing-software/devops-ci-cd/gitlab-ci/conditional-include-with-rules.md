---
id: computing-software.devops-ci-cd.gitlab-ci.conditional-include-with-rules
name: conditional-include-with-rules
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, include-rules, conditional-include, include-wildcards, include-exists]
level: practitioner
status: docs-checked
description: "Include CI configuration conditionally with include:rules (if, exists, changes), which variables are usable there, and wildcard local includes for split configs."
sources: ["https://docs.gitlab.com/ci/yaml/includes/#use-rules-with-include", "https://docs.gitlab.com/ci/yaml/#includerules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional include with rules

## 1. Patterns
```yaml
include:
  - local: ci/frontend.yml
    rules:
      - exists: [package.json]
  - local: ci/release.yml
    rules:
      - if: $CI_COMMIT_TAG
  - local: ci/docs.yml
    rules:
      - changes: [docs/**/*]
  - project: platform/ci-templates
    file: /security/sast.yml
    rules:
      - if: $SKIP_SAST != "true"
  - local: ci/jobs/*.yml          # wildcard path (* and ** are supported with include:local)
```

## 2. Which variables work in include:rules:if
Only certain variables can be used with `include:rules` (the include docs, section "Use rules with include", say so and list them). Check that list before relying on a project, group or trigger variable in an include rule.

## 3. Semantics
- Rules with `include` support only `rules:if`, `rules:exists` and `rules:changes`.
- A skipped include removes all its jobs — any other job that `needs` them breaks pipeline
  creation (use `needs:optional`).

## 4. Alternatives
- Components with `inputs` are better than variable-gated includes for reusable templates.
- For "only build what changed" in monorepos, combine with child pipelines per directory.

## Verify
- [ ] Pipeline editor → Validate (simulate branch vs tag) shows release jobs only on tags.
- [ ] Full configuration view omits excluded files' jobs.

## Checked

2026-10-28. Confirmed on the GitLab include docs: include:rules supports rules:if, rules:exists, rules:changes; wildcard paths (* and **) work with include:local; needs:optional resolves pipeline creation failures for excluded jobs. Removed: the list of usable variables, the claim about `when`, and the semantics of changes/exists (not stated on the fetched pages).
Method: documentation only; no commands were run.
