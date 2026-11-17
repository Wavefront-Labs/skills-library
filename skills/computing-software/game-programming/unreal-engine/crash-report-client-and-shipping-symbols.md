---
id: computing-software.game-programming.unreal-engine.crash-report-client-and-shipping-symbols
name: crash-report-client-and-shipping-symbols
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, crash-report-client, crash-reporting, crash-context, shipping, game-programming]
level: practitioner
status: docs-checked
description: "Package and configure Unreal's Crash Report Client for your own server: Include Crash Reporter, [CrashReportClient] keys and defaults, custom game data, report locations."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/crash-reporting-in-unreal-engine"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Crash Report Client for packaged games

**Goal:** player crashes reach your own server with useful context.

## Package it (Crash Reporting page)
By default the Crash Report Client is not included in packaged games. Enable Project Settings > Project > Packaging >
Advanced > Include Crash Reporter, or in `Config/DefaultGame.ini`:
```ini
[/Script/UnrealEd.ProjectPackagingSettings]
IncludeCrashReporter=True
```
If not in unattended mode, the client shows a window with the crash data and lets the user send or opt out.

## Configure
Settings go under `[CrashReportClient]` (in an Engine.ini; the page's reference table says `Config/DefaultEngine.ini`).
| Key | Page default | Notes |
|---|---|---|
| `bAgreeToCrashUpload` | false on Windows and Mac, true on Linux | only used for Linux builds |
| `bSendUnattendedBugReports` | true | skips the dialog and sends automatically; all platforms |
| `DataRouterUrl` | empty | server that receives reports |
| `CompanyName` | empty | shown in the "Allow contact" text |
| `CrashReportClientVersion` | empty | |
| `UserCommentSizeLimit` | 4000 | |
| `bSendLogFile` | true | "Send log file" checkbox default |
| `bHideLogFilesOption` | false | |
| `bAllowToBeContacted` | true | |
| `bIsAllowedToCloseWithoutSending` | true | |
| `bShowEndpointInTooltip` | true | |
| `bIsAllowedToCopyFilesToClipboard` | false | Windows only |
| `bHideRestartOption` | true | |

## Where reports go
Per the page, as of UE 5.4 Epic receives no reports from packaged builds. Launcher editor builds send bug reports to Epic
(opt out: Editor Preferences > Privacy > Bug Reports > Don't Send); source-built editors send nothing to Epic. UE ships no
crash report server; the page lists Backtrace, Bugsplat and Sentry as commonly used services with their own UE setup docs.

## Contents and custom context
- A report holds a crash guid, error type (crash, assert, ensure) and callstacks of all threads, system and build info, the
  log output, key/value game data, and user comments. Local reports are in the project's `Saved/Crashes`.
- Add context with `FPlatformCrashContext::SetGameData(Key, Value)` (empty value removes the key); set it before the error,
  and the current values are captured when the report is collected. It appears under `<GameData>` in
  `CrashContext.runtime-xml`.
- An `ensure` does not crash: it logs to the Output Log and sends a report to the Crash Reporter in unattended mode.

## Checked
Date: 2026-11-07. Read in full: the Crash Reporting page (all sections), an en-us page whose only version statement is the
"as of UE 5.4" note. The second source (Packaging Your Project) was dropped: it does not mention Include Crash Reporter.
Removed as not on the page: the `.pdb` / symbol server (`symstore`), `-archive`, Linux/Android/console symbol advice,
launcher "Editor symbols for debugging", `UEMinidump.dmp`, `BuildVersion` tagging, `-NoDebugInfo` warning, GDPR consent,
the claim that ensures report only in development builds, `debug crash` Verify step, and the example key
`CrashReportClientVersion=1.0` and Sentry-style URL.
Method: documentation only; no commands were run.
