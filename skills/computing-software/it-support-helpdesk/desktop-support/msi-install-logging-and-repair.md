---
id: computing-software.it-support-helpdesk.desktop-support.msi-install-logging-and-repair
name: msi-install-logging-and-repair
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, application-installation, msi-logging, msiexec, error-1603, product-code, msi-repair, installer-cleanup, app-repair]
level: practitioner
status: docs-checked
description: "Debug failing Windows installers: msiexec logging, the 1603/1618/1619/1638 and success exit codes, and uninstall or repair by product code."
sources:
  - "https://learn.microsoft.com/en-us/windows/win32/msi/command-line-options"
  - "https://learn.microsoft.com/en-us/windows/win32/msi/error-codes"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# msi-install-logging-and-repair

Goal: get from "install failed" to the exact failing step, and uninstall or repair apps
by product code.

## Log and run
`msiexec` takes a package path or a ProductCode. Use `/i` to install, `/x` to uninstall,
`/f` with a modifier to repair, `/l` with flags to write a log and `/q` for quiet modes.
Do not combine `/i`, `/x`, `/f`, `/j`, `/a`, `/p` in one call; `/l` and `/q` combine with
them. Look up the exact `/l` flag letters and `/q` modes on the command-line options page
before scripting them. Read the log from the bottom up to find the failing action.

## Exit codes that matter
| Code | Meaning (Windows Installer error codes page) |
|---|---|
| 0 | ERROR_SUCCESS |
| 3010 | ERROR_SUCCESS_REBOOT_REQUIRED: install completed, restart needed |
| 1641 | ERROR_SUCCESS_REBOOT_INITIATED: installer started a restart; indicates success |
| 1603 | ERROR_INSTALL_FAILURE: fatal error during installation |
| 1618 | ERROR_INSTALL_ALREADY_RUNNING: another installation is in progress |
| 1619 | ERROR_INSTALL_PACKAGE_OPEN_FAILED: package could not be opened; check it exists and is reachable |
| 1638 | ERROR_PRODUCT_VERSION: another version of the product is already installed |

## Gotchas
- 1618: wait for the other install to finish, then retry.
- 1638: remove or configure the installed version first (Microsoft points to Add/Remove
  Programs), or use an upgrade package.
- Installs running as SYSTEM may not reach user-only network paths; that is a common reason
  a package "cannot be opened" (1619).
- Wrappers around an MSI (setup.exe) have their own switches; read the vendor's docs.

## Checked
2026-11-01. Confirmed on Microsoft Learn "Command-Line Options" (msiexec options /i /x /f /l /q,
combination rules) and "Windows Installer Error Codes" (0, 3010, 1641, 1603, 1618, 1619, 1638
names and meanings). Removed: Return value 3 search tip, 1720/1722/1920/1925 meanings,
logging policy registry value, Win32_InstalledWin32Program query, /fa and /fomus meanings,
/qn and /norestart usage, PendingFileRenameOperations, MSI installer-folder warning, exe
wrapper switches.
Method: documentation only; no commands were run.
