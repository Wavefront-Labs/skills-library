---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-startup-timeout-and-pulls
name: quadlet-startup-timeout-and-pulls
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, timeoutstartsec, image-pull, oneshot, startup-timeout, systemd, build]
level: practitioner
status: docs-checked
description: "Prevent Quadlet unit failures when image pulls or builds exceed systemd's 90-second start limit with pre-pulling or TimeoutStartSec, including the oneshot exception."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop slow pulls and builds from killing the service.

When a Quadlet unit starts, Podman may need to pull or build images. That can take far longer than systemd's default 90-second service start limit and cause the unit to fail. Two fixes: pre-pull the required images, or raise the service's start timeout with `TimeoutStartSec`.

The page's snippet extends the timeout to 15 minutes; add it to the Quadlet file:

```
[Service]
TimeoutStartSec=900
```

Exception: for units with `Type=oneshot` the startup timeout is disabled by default (infinity). Since `.volume`, `.network`, `.build`, `.image` and `.artifact` units default to oneshot, a timeout there must be set explicitly if you want one. See systemd.service(5) for details of `TimeoutStartSec`.


Two ways to avoid the failure, side by side. Pre-pull: have the image present before the unit starts, or define an `.image` Quadlet and reference it from the container so the pull happens in its own oneshot unit. Raise the timeout: `TimeoutStartSec=900` in the `[Service]` section gives 15 minutes. For `Type=oneshot` units such as `.build`, the default is infinity, so no change is needed unless you want a limit.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed. Wording tightened where the page is softer than the draft.
Method: documentation only; no commands were run.
