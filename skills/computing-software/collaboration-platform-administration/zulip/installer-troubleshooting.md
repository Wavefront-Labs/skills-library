---
id: computing-software.collaboration-platform-administration.zulip.installer-troubleshooting
name: installer-troubleshooting
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [install-troubleshooting, install-log, su-zulip]
level: intro
status: docs-checked
description: "Troubleshoot a failed Zulip install: rerun the idempotent installer, read install.log and errors.log, and handle su zulip password prompts."
sources: ["https://zulip.readthedocs.io/en/latest/production/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting the Zulip installer

The installer is idempotent. If it fails, correct the cause and simply run it again.

Every run logs a transcript to `/var/log/zulip/install.log`. Keep it handy, and attach a copy to any bug report.

If an error appears after `scripts/setup/install` finished, inspect the bottom of `/var/log/zulip/errors.log` for a traceback, then use the troubleshooting guidance for services and supervisor.

The `zulip` user password: by default the `zulip` account has no password. It is meant to be reached with `su zulip` from root, or through SSH keys or a password if you choose to set them up. Most people prompted for a password after `su zulip` had already switched to the `zulip` user earlier in the session, so they can skip the step.

When asking for help, post a new topic in the production help channel of the project's community server. Include:

- What you were trying to do, and the problems met.
- The relevant logs in code blocks, not screenshots: the full traceback from the bottom of `errors.log`, or `install.log`.
- Your Zulip Server version, or the two versions of an upgrade.

Community support is best-effort but free and interactive for most questions; paid options include phone support from the core engineering team.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/troubleshooting.html (zulip.readthedocs.io, latest). Removed: the pre-rerun checklist.

Method: documentation only; no commands were run.
