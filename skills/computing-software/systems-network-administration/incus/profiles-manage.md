---
id: computing-software.systems-network-administration.incus.profiles-manage
name: profiles-manage
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, profile, default-profile, devices, precedence, profile-edit]
level: practitioner
status: docs-checked
description: "Create, edit and apply Incus profiles: profile set/device add/edit commands, apply and remove on instances, ordering precedence and the default profile."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/profiles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiles

```
incus profile list
incus profile show <profile>
incus profile create <profile>
incus profile set <profile> <key>=<value>
incus profile device add <profile> <device> <type> <key>=<value>
incus profile device set <profile> <device> <key>=<value>
incus profile edit <profile> < profile.yaml
incus profile add <instance> <profile>
incus profile remove <instance> <profile>
incus launch <image> <name> --profile a --profile b
```

- Profiles hold options, devices and device options; they apply to containers and VMs (unsuitable options are ignored silently).
- Multiple profiles apply in the order given; the last to set a key wins. Instance-level config always overrides profiles.
- With no profile specified, `default` is used: it defines a network interface and a root disk (the page's example shows `eth0` on `incusbr0`). It cannot be renamed or removed.
- Editing a profile updates every instance using it.
- `incus config show <instance>` lists `profiles`; add `--expanded` to see inherited options.

## Checked

2026-11-04: confirmed against the Incus profiles page (profile commands, ordering and override rules, ignored unsuitable options, default profile, YAML edit, live propagation to instances). Softened the default profile contents to match the page, which gives them only as an example.

Method: documentation only; no commands were run.
