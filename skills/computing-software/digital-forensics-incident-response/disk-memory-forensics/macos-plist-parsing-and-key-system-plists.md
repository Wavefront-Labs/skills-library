---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.macos-plist-parsing-and-key-system-plists
name: macos-plist-parsing-and-key-system-plists
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [plist-forensics, plist, binary-plist, nskeyedarchiver, plutil, macos, ios, dfir]
level: practitioner
status: draft
description: "Parse XML, binary and NSKeyedArchiver plists with plutil and Python, and know which macOS system plists answer common investigative questions."
sources: ["https://developer.apple.com/documentation/foundation/propertylistserialization", "https://docs.python.org/3/library/plistlib.html", "https://github.com/ydkhatri/mac_apt"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plist parsing and key system plists

**Goal:** read any property list correctly (format, embedded data, archived objects) and know
where the useful ones live.

## Formats and tools
- XML (`<?xml ... <plist>`), binary (`bplist00` magic), and NSKeyedArchiver (binary plist with
  `$archiver`, `$objects`, `$top`: an object graph, not a plain dictionary).
```bash
plutil -p file.plist                     # pretty-print any format (macOS)
plutil -convert xml1 -o out.xml file.plist   # convert a copy, never the evidence
python3 -c "import plistlib,sys,pprint;pprint.pprint(plistlib.load(open(sys.argv[1],'rb')))" file.plist
```
- NSKeyedArchiver: resolve `CF$UID` references; use `ccl_bplist` or mac_apt's deserializer, or
  `plistutil`. Many SFL/SFL2/SFL3 recent-items files and app state files are archived objects.
- Embedded binary values (bookmarks, aliases) contain file paths, volume names and timestamps:
  parse bookmark data with mac_apt or `mac_alias`.
- Dates in plists are `<date>` (UTC) or Mac absolute time numbers (add 978307200 to get Unix).

## Key plists
| Question | Plist |
|---|---|
| OS version/build | `/System/Library/CoreServices/SystemVersion.plist` |
| Install date | `/private/var/db/.AppleSetupDone` (birth time), `/Library/Receipts/InstallHistory.plist` |
| Installed software history | `/Library/Receipts/InstallHistory.plist` |
| Time zone | `/Library/Preferences/.GlobalPreferences.plist` and `/etc/localtime` link |
| Users | `/private/var/db/dslocal/nodes/Default/users/<user>.plist` (UID, home, creation time, password policy) |
| Last logged in user, auto-login | `/Library/Preferences/com.apple.loginwindow.plist` |
| Network interfaces / Wi-Fi known networks | `/Library/Preferences/SystemConfiguration/preferences.plist`, `com.apple.wifi.known-networks.plist` |
| Bluetooth devices | `/Library/Preferences/com.apple.Bluetooth.plist` |
| Recent items / documents | `~/Library/Application Support/com.apple.sharedfilelist/*.sfl2` / `*.sfl3` |
| Finder recent folders, mounted volumes | `~/Library/Preferences/com.apple.finder.plist` |
| Dock (pinned/recent apps) | `~/Library/Preferences/com.apple.dock.plist` |
| Gatekeeper/quarantine (SQLite, not plist) | `~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2` |

## Gotchas
- `cfprefsd` caches preferences in memory; a live system's on-disk plist may lag recent
  changes. Collect after a graceful process or acquire memory.
- Modifying a plist with `defaults write` on evidence changes it; always work on copies.

## Self-check
You identified the plist format, decoded archived objects and embedded bookmarks, and converted
every date to UTC.
