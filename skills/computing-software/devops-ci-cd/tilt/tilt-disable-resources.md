---
id: computing-software.devops-ci-cd.tilt.tilt-disable-resources
name: tilt-disable-resources
category: computing-software
field: devops-ci-cd
product: tilt
tags: [disable-resources, tilt]
level: practitioner
status: docs-checked
description: "Enable and disable Tilt resources on the fly with tilt args, tilt enable/disable, the Tilt UI, or config.clear_enabled_resources in the Tiltfile."
sources:
  - "https://docs.tilt.dev/disable_resources.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disabling resources

Goal: run only the resources you need, and toggle others without interrupting your flow. Available in Tilt v0.24.0+.

Disabling a resource stops the running process (if any) and deletes any objects owned by it, equivalent to `tilt down` on that resource. Enabling creates, builds, deploys, and starts processes for it.

## tilt args

Resources named in args are enabled; the rest of those defined in the Tiltfile are disabled and shown in the UI.

```shell
# enable only the resources named 'frontend' and 'glitch'
$ tilt up frontend glitch
```

Edit args by running `tilt args` with a new set (replaces the existing ones), or with none to open the current args for editing:

```shell
$ tilt args bounding-box muxer max-object-detector
```

Toggling in the UI does not change the value of `tilt args`. If args do not change between edits, Tilt treats it as a no-op, even if you toggled resources in the UI.

## Tilt UI

- Detail View: a "Disable Resource" button near the logs; logs stay visible for disabled resources, with an "Enable Resource" button.
- Table View: select multiple resources via the checkbox column and use the bulk action buttons.

Disabled resources are listed at the bottom of resource groups (or the whole list). UI toggling ignores resource dependencies: disabling A does not disable B that depends on A.

## CLI

```shell
tilt enable frontend storage
tilt enable --only frontend storage   # disables all others
tilt enable --all
tilt disable frontend storage
tilt disable --all
```

## Tiltfile

To start with every resource disabled, visible in the UI so you can enable what you need:

```python
config.clear_enabled_resources()
```

See the Tiltfile config guide for groups of resources.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/disable_resources.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
