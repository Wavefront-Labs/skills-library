---
id: computing-software.collaboration-platform-administration.zulip.install-from-git
name: install-from-git
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [install-from-git, zulip-main, git-deployment]
level: practitioner
status: docs-checked
description: "Deploy Zulip from a Git clone instead of a tarball, usually to run main for an unreleased feature or new OS support, and upgrade later."
sources: ["https://zulip.readthedocs.io/en/latest/production/deployment.html", "https://zulip.readthedocs.io/en/latest/production/install.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing Zulip from Git

You can install a development snapshot by cloning the repository instead of unpacking a release tarball:

```
sudo apt install git
git clone https://github.com/zulip/zulip.git zulip-server-git
```

Then continue with Step 2 of the normal installation instructions: run the installer as root with the usual options such as `--certbot`, `--email` and `--hostname`. The installer moves the code tree into the zulip user's `deployments` directory and points `current` at it.

The common reason is to run `main` for a feature not yet in a release, often support for a new base OS version. The project has dedicated notes on how `main` works and the support story for it, and on upgrading to future releases afterwards. A Git installation can later be upgraded with the documented upgrade-from-a-Git-repository procedure.

The maintainers state they are glad to investigate problems found installing from `main`. Such failures are rare and reports help keep the next major release's install experience reliable.

## Checked

Confirmed against the Installing Zulip from Git and installer details sections of the deployment page and Step 2 of the install page. Removed the best-effort support claim and the closing advice about recording commits and moving back to releases (not on the pages).

Method: docs-checked 2026-11-09 against docs/production/deployment.md and docs/production/install.md in the zulip/zulip repository (main), the sources of the cited pages.
