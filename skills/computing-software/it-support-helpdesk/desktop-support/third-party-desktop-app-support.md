---
id: computing-software.it-support-helpdesk.desktop-support.third-party-desktop-app-support
name: third-party-desktop-app-support
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, vc-redist, java-runtime, application-hang, file-associations, acrobat-support, software-activation]
level: practitioner
status: draft
description: "Keep third-party desktop apps working: VC++ and .NET runtimes, Java-dependent apps, hung applications, default apps and file associations, Acrobat issues and licence activation."
sources:
  - "https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist"
  - "https://learn.microsoft.com/en-us/windows/configuration/default-apps/"
  - "https://helpx.adobe.com/acrobat/kb/troubleshoot-acrobat-reader-crash-issues.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# third-party-desktop-app-support

## Runtimes
- "MSVCP140.dll / VCRUNTIME140.dll missing", side-by-side errors (event 33 SideBySide):
  install the **latest supported Visual C++ Redistributable** (x64 and x86; 32-bit apps
  need x86 even on 64-bit Windows). `winget install Microsoft.VCRedist.2015+.x64`.
- .NET: .NET Framework 3.5 for old apps (`DISM /Online /Enable-Feature
  /FeatureName:NetFx3`, may need install media source on WSUS-managed PCs); modern apps
  need the specific .NET Desktop Runtime major version (`dotnet --list-runtimes`).
- **Java**: identify the version the app needs (vendor docs, `java -version`). Oracle
  Java licensing changed (2023 per-employee model); prefer OpenJDK builds (Microsoft,
  Eclipse Temurin) unless the vendor requires Oracle. Multiple versions: the app's
  launcher or `JAVA_HOME` decides; Java web start/applets need OpenWebStart or vendor
  replacement.

## Hung applications
- "Not responding": wait 1-2 minutes on large files; check Task Manager for CPU/disk
  activity by the process.
- Capture before killing if it recurs: Task Manager > right-click > **Create dump
  file**; event 1002 (Application Hang) in the Application log names the module.
- Common causes: network drive or printer unreachable (hangs on File > Open/Print),
  add-ins (Office: start with `/safe`), antivirus scanning, GPU acceleration (disable
  hardware acceleration in the app).
- Resource Monitor > CPU > right-click process > **Analyze wait chain** shows what it is
  waiting on.

## Default apps and file associations
- User choice: Settings > Apps > Default apps. Windows protects associations with a
  hash; scripts writing the registry directly are reset ("an app default was reset").
- Enterprise: export a reference with
  `Dism /Online /Export-DefaultAppAssociations:<OUTPUT_DIR>\assoc.xml`, edit, deploy via GPO
  "Set a default associations configuration file" or Intune
  (ApplicationDefaults/DefaultAssociationsConfiguration). Applies at sign-in to new and
  existing users (re-applies each logon with the policy).
- PDF to Acrobat vs Edge: the most common request; set in the associations XML.

## Acrobat / PDF reader issues
- Crashes on open: disable **Protected Mode** and **Enhanced Security** temporarily to
  test (Edit > Preferences > Security (Enhanced)); repair install (Help > Repair
  Installation); reset preferences by renaming
  `%APPDATA%\Adobe\Acrobat\DC` folder.
- Acrobat sign-in/licence prompts: named-user licensing requires the user's Adobe ID
  from the Admin Console; shared device licensing for labs.
- Printing PDFs fails: "Print as image" in Advanced print settings for problem files.

## Third-party activation
- Collect: product, version, licence type (named user, device, concurrent/network
  server, subscription), the exact error.
- Named user: check assignment in the vendor admin console; sign out/in. Device-locked:
  deactivate old device first (vendor portal). Network licences: licence server
  reachable (port), seats free.
- Keep licence keys and admin console access in the vault, not in tickets.

## Verify
The app starts and the user completes the failing task; runtime versions and
associations are captured in the build standard so it doesn't recur.
