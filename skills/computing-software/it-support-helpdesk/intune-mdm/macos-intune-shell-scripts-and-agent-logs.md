---
id: computing-software.it-support-helpdesk.intune-mdm.macos-intune-shell-scripts-and-agent-logs
name: macos-intune-shell-scripts-and-agent-logs
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, macos-shell-scripts-intune, intune-macos-agent-logs, custom-attributes, intune-agent, macos-management]
level: practitioner
status: docs-checked
description: "Deploy shell scripts and custom attributes to Macs with Intune, and collect the Intune macOS agent logs to troubleshoot script and app deployment failures."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/macos-shell-scripts"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/lob-apps-macos-dmg"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macos-intune-shell-scripts-and-agent-logs

## Shell scripts
- Add a script under the macOS platform's shell scripts in the Intune admin center. Options:
  - **Run script as signed-in user**: No (default) runs as root.
  - **Hide script notifications**: by default users see an "IT is configuring your computer"
    notification.
  - **Script frequency**: how often it runs. Scripts can still run more often than chosen if
    the disk is full, the storage location is tampered with, the local cache is deleted or
    the Mac restarts.
  - **Max number of times to retry**: runs again on a non-zero exit code (zero is success);
    Not configured (default) means no retry.
- Scripts running longer than 60 minutes are stopped and reported as failed.
- Run status is reported only when it changes from the last report.
- Scripts assigned to user groups apply to any user logging in to the Mac.

## Custom attributes
- Devices > By platform > macOS > Organize devices > Custom attributes for macOS > Add.
- The script must echo the attribute value, and the output type must match the data type
  chosen in the custom attribute profile.

## Collecting logs
- Use **Collect logs** on the device and give full absolute paths separated only by a
  semicolon, no spaces or newlines. Allowed extensions: .log, .zip, .gz, .tar, .txt, .xml,
  .crash, .rtf. Limit: 60 MB compressed or 25 files, whichever comes first.
- Logs are collected at the next agent check-in, which usually occurs every 8 hours.
- Collected logs are stored in Azure storage for 30 days and downloaded from the admin center.
- The agent logs in `/Library/Logs/Microsoft/Intune` and `~/Library/Logs/Microsoft/Intune`
  are collected too. Missing files or wrong extensions are listed in `LogCollectionInfo.txt`.
- Errors such as 0X87D300D1 mean a log file over the size limit or a path that does not exist.

## Pitfalls
- Running as root, `$HOME` and `~` point to root's home, not the user's.
- Test scripts locally on a Mac before assigning.

## Verify
Script status shows Success, custom attribute values appear on the device, and the collected
agent logs show the script run with exit code 0.

## Checked
2026-11-01. Confirmed against the Learn shell scripts page: run-as, notifications, frequency
exceptions, retry, 60-minute limit, custom attributes path, log collection limits, extensions,
8-hour check-in, 30-day retention, agent log folders and error code. Removed: 200 KB script
size, log file name globs, agent kill command, install.log, Collect diagnostics claim, "bad
interpreter" and agent app name.
Method: documentation only; no commands were run.
