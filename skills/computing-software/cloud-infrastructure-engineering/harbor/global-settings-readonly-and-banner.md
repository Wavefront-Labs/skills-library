---
id: computing-software.cloud-infrastructure-engineering.harbor.global-settings-readonly-and-banner
name: global-settings-readonly-and-banner
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [read-only, project-creation, banner-message, retain-pull-time, harbor]
level: intro
status: docs-checked
description: "Set Harbor read-only mode, restrict project creation, keep image pull time during scans, and show a UI banner."
sources:
  - https://goharbor.io/docs/main/administration/general-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global settings live under Administration, Configuration, System Settings.

**Read-only registry.** In read-only mode Harbor still allows `docker pull` but prevents `docker push` and deletion of repositories and tags. A push is refused with `denied: The system is in read only mode. Any modification is prohibited.` Use it during maintenance and backups.

**Project Creation.** The drop-down sets who can create projects: **Everyone** or **Admin Only** (users with the Harbor system administrator role).

**Retain image last pull time on scanning.** By default a vulnerability scanner such as Trivy updates an image last pull time when it scans the image. That distorts Tag Retention rules that are based on pull time. Enable this option to stop scans updating the pull time.

**Banner message.** Shows a custom message at the top of the UI to every user, anonymous users included. Fields:
- **Message Content**: required.
- **Message Type**: each type has its own style.
- **Closable**: whether users can dismiss it temporarily.
- **Duration**: required; runs from 0:00 of the start date to 0:00 of the end date.

## Checked

2026-11-03. Read-only behaviour and denial message, Project Creation options, the retain pull time option and banner fields were read against the Harbor docs page Configure Global Settings. Removed: the closing remark about the authentication tab (not on the page).

Method: documentation only; no commands were run.
