---
id: computing-software.it-support-helpdesk.apple-device-management.first-boot-automation
name: first-boot-automation
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, provisioning, first-boot-automation, first-boot, swiftdialog]
level: practitioner
status: docs-checked
description: "Design a hands-free Mac provisioning flow: run a main policy after enrolment and show progress to the user with swiftDialog."
sources:
  - https://github.com/swiftDialog/swiftDialog/wiki
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# first-boot-automation

Goal: a repeatable zero-touch Mac build.
- Skip Setup Assistant panes you do not need in the enrolment profile, and create the end user with your chosen identity tool or Setup Assistant.
- Trigger one main provisioning policy when enrolment completes, and have it call smaller policies in a fixed order.
- Show progress with swiftDialog: `dialog --title "Setting up" --message "Installing..." --progress`. In swiftDialog, `--title` and `--message` set the text, `--progress` enables an interactive progress bar (it takes an optional integer) and `--progresstext` sets the text under it. The tool installs at `/usr/local/bin/dialog`.
- Install order that tends to work: security agent, VPN, productivity apps, then updates.
- Log each step to a file so a failed run can be diagnosed.
Practice: test on both wired and Wi-Fi, time the full run, and show a clear error with a contact number if any step fails, rather than leaving the user watching a stalled bar.
Gotcha: avoid user interaction until the desktop is up.
Verify:
- Fresh Mac completes without manual steps.
- Log file lists each policy result.

## Checked
2026-11-08. Checked the swiftDialog wiki home page and its command-line options page: `--title`, `--message`, `--progress [int]`, `--progresstext`, and the `/usr/local/bin/dialog` path. Removed (no readable source): the prestage local-admin and Jamf Connect statements, `jamf policy -event`, the claim that DEPNotify is retired, and the Apple deployment guide source (it loads only as a guide welcome page). The install order and testing advice are practice guidance.

Method: documentation only; no commands were run.
