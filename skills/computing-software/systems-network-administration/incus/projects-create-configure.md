---
id: computing-software.systems-network-administration.incus.projects-create-configure
name: projects-create-configure
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, project, features-images, features-profiles, restricted, limits, project-set]
level: practitioner
status: docs-checked
description: "Create and configure Incus projects: project create --config, features.images and features.profiles isolation, restricted=true, set/unset/edit, and the empty-project rule."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/projects_create.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create and configure projects

```
incus project create my-project
incus project create my-project-shared-images --config features.images=false
incus project create my-restricted-project --config restricted=true --config restricted.backups=allow
incus project set my-project limits.containers=5
incus project unset my-project limits.containers
incus project edit my-project
```

- `features.images=false` isolates instances but still uses the default project's images.
- `restricted=true` blocks security-sensitive features such as container nesting; `restricted.backups=allow` keeps backups available.
- `features.profiles` defaults to `true`, so the project cannot use the `default` project's default profile and has no root disk. Add one with `incus profile device add`.
- `unset` resets to the default, which may differ from the value given at creation.
- Enabled features cannot change while the project contains instances; some options need an empty project.

## Checked

2026-11-04: confirmed against the Incus create-and-configure-projects how-to (create examples, `features.images=false`, `restricted` options, isolated profiles and missing root disk, set/unset/edit, unset default caveat, empty-project rules). Nothing removed.

Method: documentation only; no commands were run.
