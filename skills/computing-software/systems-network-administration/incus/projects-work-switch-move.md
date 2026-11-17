---
id: computing-software.systems-network-administration.incus.projects-work-switch-move
name: projects-work-switch-move
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, project, switch, target-project, move, default-profile, root-device]
level: practitioner
status: docs-checked
description: "Work across Incus projects: list, switch, use --project, move instances with --target-project, and fix the 'No root device could be found' error with an isolated default profile."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/projects_work.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working with projects

```
incus project list              # current project marked "(current)"; --format changes output
incus project switch <project>
incus list --project my-project
incus move my-instance my-instance --project default --target-project my-project
```

- You only see and target projects you have permission for.
- The target project must not already hold an instance of that name.
- A new project with default settings isolates profiles (`features.profiles=true`), so creating an instance fails with "No root device could be found."
- Fix: copy the default project's default profile:

```
incus profile show default --project default | incus profile edit default
```

## Checked

2026-11-04: confirmed against the Incus working-with-projects how-to (project list and switch, `--project`, `--target-project` move, permission scoping, isolated profiles error and the profile copy fix). Nothing removed.

Method: documentation only; no commands were run.
