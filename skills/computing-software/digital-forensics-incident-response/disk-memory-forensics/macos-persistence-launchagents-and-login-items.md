---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.macos-persistence-launchagents-and-login-items
name: macos-persistence-launchagents-and-login-items
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [launchagents, launchdaemons, macos-persistence, login-items, btm, cron, configuration-profiles, dfir]
level: practitioner
status: draft
description: "Hunt macOS persistence: LaunchAgents and LaunchDaemons, login and background items (BTM), cron, profiles, shell configs, and how to review them offline."
sources: ["https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html", "https://attack.mitre.org/techniques/T1543/004/", "https://objective-see.org/tools.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS persistence (LaunchAgents, LaunchDaemons, login items)

**Goal:** enumerate every common autostart location on a Mac and separate attacker
persistence from legitimate software.

## launchd jobs (by far the most common)
| Path | Runs as | When |
|---|---|---|
| `~/Library/LaunchAgents/*.plist` | user | user login |
| `/Library/LaunchAgents/*.plist` | each user | any login |
| `/Library/LaunchDaemons/*.plist` | root | boot |
| `/System/Library/Launch{Agents,Daemons}/` | Apple only (SIP-protected) | |
Key plist fields: `Label`, `ProgramArguments`/`Program`, `RunAtLoad`, `KeepAlive`,
`StartInterval`, `WatchPaths`. Red flags: binaries in `/tmp`, `/Users/<shared>` (the Shared folder), hidden
directories (`~/.local`, `~/Library/.x`), interpreters (`/bin/sh -c`, `python`, `osascript`)
with inline code, labels imitating Apple (`com.apple.*` outside `/System`), unsigned targets.
```bash
plutil -p ~/Library/LaunchAgents/com.example.update.plist
codesign -dv --verbose=4 /path/to/target ; spctl -a -vv /path/to/target
launchctl print gui/$(id -u) | less     # live: loaded jobs for the user
```

## Login and background items
- macOS 13+: Background Task Management database
  `/private/var/db/com.apple.backgroundtaskmanagementd/BackgroundItems-v*.btm`. Dump live with
  `sfltool dumpbtm`; it lists login items, launch agents/daemons registered by apps and their
  developer/team IDs. Unified log: `log show --predicate 'subsystem == "com.apple.backgroundtaskmanagement"'`.
- Older: `~/Library/Application Support/com.apple.backgroundtaskmanagementagent/backgrounditems.btm`.

## Other locations
- `cron`/`at`: `/usr/lib/cron/tabs/`, `/var/at/tabs/`; `periodic` scripts in `/etc/periodic/`.
- Shell startup files: `~/.zshrc`, `~/.zprofile`, `~/.zshenv`, `/etc/zshrc`, `~/.bash_profile`.
- Configuration profiles: `profiles show -all` (malicious profiles set proxies, DNS, root certs).
- Login/logout hooks (deprecated): `defaults read com.apple.loginwindow`.
- Authorization plugins `/Library/Security/SecurityAgentPlugins/`, kexts/system extensions,
  Spotlight importers, `emond` rules (`/etc/emond.d/`, removed in recent macOS), dylib hijacks
  via `DYLD_INSERT_LIBRARIES` in plist `EnvironmentVariables`.

## Workflow
1. Run KnockKnock (Objective-See) or `mac_apt` AUTOSTART on the image for a full listing.
2. For each item: target path, signature/team ID, file birth time, quarantine xattr
   (`xattr -l`), and creation in FSEvents/unified logs.
3. Compare with an inventory of approved software.

## Self-check
Each autostart item is signed by a known developer or explained; unknown ones have a target
hash, creation time and origin.
