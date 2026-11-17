---
id: computing-software.general-digital-literacy.basic-troubleshooting.slow-computer-and-storage-cleanup
name: slow-computer-and-storage-cleanup
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, slow-computer, performance, startup-programs, background-apps, task-manager, activity-monitor, disk-cleanup, storage-sense, malware, antivirus, ram, cpu, fan-noise, overheating]
level: intro
status: draft
description: "Find the real cause of a slow computer — startup bloat, background apps, low disk space or malware — with Task Manager/Activity Monitor instead of guessing."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slow computer and storage cleanup — find the actual cause before buying anything

**Goal:** diagnose *why* a computer is slow using the built-in tools everyone already has,
fix the common causes, and know the difference between "needs cleanup" and "needs new
hardware" — before paying for a "speed-up" utility, most of which do little beyond what
is free.

## 1. Look at what's actually busy
Open **Task Manager** (Windows: `Ctrl+Shift+Esc` › Processes tab, sort by CPU/Memory/Disk)
or **Activity Monitor** (macOS: Spotlight › "Activity Monitor" › CPU/Memory/Disk tabs).
- One process pinned near 100% CPU for minutes = that app or a runaway background task,
  not the whole machine being "old". Note its name before deciding anything.
- High **Disk** activity with low CPU (Windows) is often a scheduled antivirus scan,
  Windows Update downloading, or OneDrive/Dropbox syncing a large folder — wait it out or
  pause the sync rather than fighting it.
- Memory consistently over ~90% with the machine otherwise idle means too many apps are
  resident; close unused ones or add RAM — software fixes won't create memory.

## 2. Trim startup programs
Every app that starts with the OS adds boot time and sits in memory even unused.
- Windows: Task Manager › **Startup apps** tab (Windows 11) — disable anything you don't
  need running immediately (chat apps, updaters, game launchers). Don't disable antivirus
  or the audio/graphics driver tray apps.
- macOS: System Settings › General › **Login Items & Extensions** — remove apps you don't
  want auto-launching.
- Browsers with many extensions also slow every page load; disable unused ones (see
  browser-essentials).

## 3. Free up disk space
Under roughly **10–15% free space** slows the whole system (virtual memory/swap has
nowhere to breathe) and can make Windows Update fail outright.
- Windows: Settings › System › **Storage** › Temporary files / Storage Sense (schedule
  automatic cleanup). Settings › Apps to uninstall anything unused — check install size,
  largest first.
- macOS: Apple menu › About This Mac › **Storage** › Manage, or System Settings ›
  General › Storage — shows what's eating space (Documents, Apps, System, "Other").
- The single biggest easy win is usually the **Downloads folder** and old installers —
  see organising-files-and-folders for keeping it tidy going forward.

## 4. Rule out malware
A sudden slowdown, strange pop-ups, a browser homepage that changed itself, or a fan
constantly at full speed with nothing open are the classic signs.
- Windows: run a scan with built-in **Windows Security** (Microsoft Defender) — it's
  always running; a full scan is Settings › Privacy & security › Windows Security › Scan
  options › Full scan.
- macOS gets far less malware but is not immune — unexpected profile/extension installs
  or browser hijacks are the usual pattern; check Safari/Chrome extensions first.
- Don't install a second "antivirus" on top of Defender permanently — two real-time
  scanners fighting over every file access is itself a major slowdown.

## 5. Heat and fan noise (laptops especially)
Constant high fan noise under light use = something is pegging the CPU (see step 1) or
vents are blocked/dusty. Use the machine on a hard surface, not a bed or lap, and check
Task Manager/Activity Monitor before assuming hardware failure — thermal throttling from
a genuinely overheating, dust-clogged machine shows as slowdowns specifically under load
that go away once it cools.

## 6. When it's actually hardware
If free space, startup, and malware are all clean and it's still slow: an older machine
with a traditional spinning hard drive (not an SSD) will feel slow at everything,
especially boot and app launch — that's close to the ceiling software fixes can reach.
A cheap, reliable upgrade for an otherwise-working older laptop is swapping a hard drive
for an SSD; more RAM helps if Task Manager shows memory maxed with normal everyday use.

## Verify
- [ ] You identified the specific busy process/cause in Task Manager or Activity Monitor
      before changing anything.
- [ ] Startup apps list has only what you actually want launching automatically.
- [ ] Free disk space is comfortably above ~15%.
- [ ] A full malware scan has run recently and came back clean.
- [ ] You can say whether the bottleneck was software (fixable free) or hardware (needs
      an upgrade).
