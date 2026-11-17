---
id: computing-software.devops-ci-cd.flux.image-policy-selection
name: image-policy-selection
category: computing-software
field: devops-ci-cd
product: flux
tags: [imagepolicy, semver, numerical, alphabetical, filtertags]
level: sme
status: docs-checked
description: "Choose the latest image tag with ImagePolicy semver, alphabetical or numerical rules and regex tag filters with extract."
sources:
  - https://fluxcd.io/flux/components/image/imagepolicies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An ImagePolicy picks the latest tag from an ImageRepository. `.spec.imageRepositoryRef.name` names the repository, and `.spec.policy` is required with one of:

- `semver.range`: highest version fitting the constraint, for example `'>=1.0.0'`, which selects the latest stable version.
- `alphabetical.order`: the last tag in sorted order (`asc` default, or `desc`).
- `numerical.order`: the last tag when sorted numerically (`asc` default, or `desc`).

`.spec.filterTags.pattern` is a regex; only matching tags are considered. `.spec.filterTags.extract` pulls a value out of each matching tag (via a named group) and passes that to the policy instead of the full tag; if unset, the matching tags are used as they are.

Latest release candidate:

```yaml
spec:
  imageRepositoryRef:
    name: podinfo
  filterTags:
    pattern: '.*-rc.*'
  policy:
    semver:
      range: '^1.x-0'
```

Tags of the form `RELEASE.<RFC3339-TIMESTAMP>`, sorted alphabetically on the extracted timestamp:

```yaml
spec:
  imageRepositoryRef:
    name: minio
  filterTags:
    pattern: '^RELEASE\.(?P<timestamp>.*)Z$'
    extract: '$timestamp'
  policy:
    alphabetical:
      order: asc
```

The selected tag appears in `.status.latestRef`.

## Checked

2026-11-08: read the image-reflector-controller ImagePolicy spec (docs/spec/v1/imagepolicies.md in the fluxcd/image-reflector-controller repo, the source of the fluxcd.io page) in part: the policy, filter tags and status sections, via search plus targeted reads. Confirmed: semver, alphabetical and numerical rules and their asc default, filterTags pattern and extract, the release-candidate example, and status.latestRef. Removed: the timestamped CI tag example, the advice on building tags in CI and the flux CLI command, which are not in the spec; replaced the example with the spec's RELEASE one.

Method: documentation only; no commands were run.
