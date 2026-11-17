---
id: computing-software.it-support-helpdesk.intune-mdm.win32-packaging-with-intunewinapputil
name: win32-packaging-with-intunewinapputil
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, intunewin-packaging, intunewinapputil, win32-app, silent-install, return-codes, app-deployment]
level: practitioner
status: docs-checked
description: "Package Win32 apps for Intune with IntuneWinAppUtil: source folder rules, parameters, install and uninstall commands, restart behaviour, return codes and 32/64-bit context."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-prepare"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-add"
  - "https://github.com/microsoft/Microsoft-Win32-Content-Prep-Tool"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# win32-packaging-with-intunewinapputil

Intune deploys classic installers as `.intunewin` packages made with the Microsoft Win32 Content Prep Tool
(`IntuneWinAppUtil.exe`). Apps must install silently: Intune does not support interactive installs, and workarounds such
as serviceui.exe are unsupported. An app is capped at 30 GB.

## Build the package
1. One folder per app holding only that app's setup files. The tool compresses every file and subfolder in the `-c` folder,
   so keep the tool itself outside it. Put referenced files in a subfolder and use relative paths (for example
   `licenses\license.txt`).
2. Run the tool:
   ```
   IntuneWinAppUtil -c <setup_folder> -s <setup_file> -o <output_folder> -q
   ```
   - `-c` setup folder, `-s` setup file (setup.exe or setup.msi), `-o` output folder, `-h` help.
   - `-q` quiet: no prompts, overwrites existing output, creates the output folder. `-qq` also removes console output.
   - `-v` shows the tool version (version 1.8.2 and later). `-a <catalog_folder>` bundles catalog files for Windows S mode.
   - Run it with no parameters and it prompts for each value. For an MSI setup file it reads the information Intune needs.
   - Prerequisite: .NET Framework 4.7.2. Use the latest tool version; older packages trigger a warning in Intune.
3. The `.intunewin` contains compressed and encrypted source files plus the decryption information; store it as carefully as
   the source files.

## Program settings (Apps > All apps > Create > Windows app (Win32))
- **Installer type**: Command line, or PowerShell script (max 50 KB; runs in the installer's context).
- **Install command**: the full command line with the vendor's silent switch, for example `msiexec /p "MyApp123.msp"` or
  `ApplicationName.exe /quiet`. Check switches with the vendor.
- **Uninstall command**: full command line, for example `msiexec /x "{12345A67-89B0-1234-5678-000001000000}"`. Environment
  variable expansion is not supported in it; wrap the command in a script inside the package if you need variables.
- `powershell.exe` in these fields launches 32-bit PowerShell; use `%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe` for 64-bit.
- **Installation time required**: default 60 minutes, maximum 1440.
- **Install behavior**: System (all users) or User. For Entra registered devices, select System.
- **Device restart behavior**: determine from return codes; no specific action (suppress restarts for MSI); app install may
  force a restart (hard reboot triggers a restart in 120 minutes); or Intune forces a restart.
- **Return codes**: defaults are added at creation and editable; types are Failed, Hard reboot, Soft reboot, Retry (three
  attempts, five minutes apart) and Success.
- Requirements rules (file, registry, script) and detection rules (MSI, file, registry, script) are covered in
  win32-detection-and-requirement-rules.

## 32-bit vs 64-bit
File and registry rules and scripts have a 32-bit option: "Associated with a 32-bit app on 64-bit clients" (default No =
64-bit) and "Run script as 32-bit process on 64-bit clients" (default No). 32-bit clients always use 32-bit.

## Gotchas
- Paths with spaces need quotes in commands.
- Win32 apps are not removed if the device is unenrolled, so restrict assignment to corporate managed devices.

## Verify
On a pilot device the app installs silently, detection reports installed, and the uninstall assignment removes it.

## Checked
Date: 2026-11-08. Read in full: "Prepare Win32 app content for upload" (updated 2026-04-14), "Add, assign, and monitor a
Win32 app" (Program and Requirements sections), and the Content Prep Tool GitHub README (v1.8.7). Removed as unconfirmed:
the specific msiexec switch set and TRANSFORMS example, PSAppDeployToolkit and ServiceUI advice, the default return code
numbers (1707, 3010, 1641, 1618), the claim that IME runs installs as a 64-bit process, psexec testing, the
"update requires a changed detection rule" note, and the Delivery Optimization comment.
Method: documentation only; no commands were run.
