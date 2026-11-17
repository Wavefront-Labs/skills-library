---
id: computing-software.cybersecurity-defensive.wazuh.active-response-custom-scripts
name: active-response-custom-scripts
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [custom-active-response, stdin-json, stateful, check-keys, launcher-cmd, pyinstaller]
level: advanced
status: docs-checked
description: "Write a custom Wazuh active response script: the JSON message on stdin, stateless versus stateful add/delete, check_keys handshake, newline rule, and Windows packaging."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/active-response/custom-active-response-scripts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scripts receive a JSON message on STDIN with `version`, `origin` (`name`, `module`), `command` (`add` or `delete`) and `parameters` (`extra_args`, `alert`, `program`).

Stateless scripts handle only `add`. Stateful scripts also handle `delete` to revert the action after the timeout, which needs a `<timeout>` value. Stateful scripts write a JSON message with `"command":"check_keys"` to STDOUT and then read `continue` or `abort` from STDIN.

Deadlock trap: STDIN reads stop at a newline and STDOUT messages must end with one, otherwise a deadlock can occur.

Linux/macOS setup: place the script in `/var/ossec/active-response/bin` (macOS `/Library/Ossec/active-response/bin`), `chmod 750`, `chown root:wazuh`, restart the agent. On the server define `<command>` with `<name>`, `<executable>` and `<timeout_allowed>yes</timeout_allowed>`, then `<active-response>` with `<disabled>`, `<command>`, `<location>local</location>`, `<rules_id>` and `<timeout>`, and restart `wazuh-manager`.

Windows: Python must be installed with PATH enabled. Either compile with PyInstaller to `custom-ar.exe`, or use `launcher.cmd` with `<extra_args>custom-ar.py</extra_args>`; the launcher needs `<PYTHON_ABSOLUTE_PATH>` set.

The sample `custom-ar.py` keys on rule ID, creates `ar-test-result.txt` on `add`, deletes it on `delete`, and logs to `/var/ossec/logs/active-responses.log`.

## Checked

2026-11-03. Confirmed against the Wazuh page "Custom active response scripts": JSON fields on STDIN, stateless vs stateful add/delete, check_keys then continue/abort, the newline deadlock warning, Linux/macOS paths and chmod 750/chown root:wazuh, the command and active-response blocks, Windows PyInstaller and launcher.cmd routes (`<extra_args>`, `<PYTHON_ABSOLUTE_PATH>`), and the sample script behaviour. Nothing removed.

Method: documentation only; no commands were run.
