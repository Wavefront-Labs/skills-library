---
id: computing-software.devops-ci-cd.semaphore-ui.install-snap-deprecated
name: install-snap-deprecated
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [snap, snapcraft, installation, admin-user, semaphore-ui]
level: intro
status: docs-checked
description: "Install the deprecated Semaphore snap, create the first admin user and read its configuration."
sources:
  - https://semaphoreui.com/docs/admin-guide/installation/snap
  - https://semaphoreui.com/docs/admin-guide/configuration/snap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install Semaphore with snap (deprecated)

Goal: run Semaphore from the snap package. The docs mark this method as deprecated.

```bash
sudo snap install semaphore
```

The UI is on port 3000 (the docs print an https URL, but TLS is not configured by default), but no login exists yet. Stop the service, create an admin, start again:

```bash
sudo snap stop semaphore
sudo semaphore user add --admin \
  --login john --name=John --email=john@example.com --password=12345
sudo snap start semaphore
```

Check the service:

```bash
sudo snap services semaphore
```

Expected row: `semaphore.semaphored  enabled  active`.

Configuration is held in snap config: `sudo snap get semaphore` lists the options, `sudo snap set semaphore port=4444` changes one, and `sudo snap restart semaphore` applies it. The configuration reference lists the available options.

Gotchas:
- Use a strong password and change it from the web UI afterwards, because command-line passwords end up in shell history.
- Ansible running inside a snap or container is isolated; implicit localhost fact gathering can fail (see the troubleshooting skill).
- The method is deprecated; pick another installation method for new installs.

Verify: `snap services semaphore` reports active and the new admin can sign in.

## Checked

2026-11-04: checked against the snap installation and snap configuration pages. Added snap set, get and restart; the method is documented as deprecated.

Method: documentation only; no commands were run.
