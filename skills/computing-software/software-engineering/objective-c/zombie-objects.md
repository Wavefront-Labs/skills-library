---
id: computing-software.software-engineering.objective-c.zombie-objects
name: zombie-objects
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-memory-tools, zombie-objects]
level: practitioner
status: draft
description: "Diagnose messages to deallocated objects with Zombie Objects (NSZombieEnabled) and read the unrecognized-selector-to-deallocated-instance log."
sources:
  - https://developer.apple.com/documentation/xcode
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/MemoryMgmt.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zombie objects
**Goal:** find over-released or dangling `unsafe_unretained`/`assign` references.

- Enable: Xcode scheme > Run > Diagnostics > Zombie Objects; or environment variable `NSZombieEnabled=YES` for command-line runs.
- Deallocated objects become zombies instead of being freed; messages to them log `*** -[Foo bar]: message sent to deallocated instance 0x...` and break into the debugger.
- Typical causes: `assign`/`unsafe_unretained` delegate properties, MRC over-release, unbalanced CF release, KVO observers.
- Combine with Instruments Allocations "Record reference counts" to trace the retain/release history of that address.
- Zombies disable memory reclaiming; do not leave on for long sessions or profiling.
- Does not work as expected with objects freed by C `free()` or memory the sanitizer manages; use Address Sanitizer for those.

## Gotchas
- Zombie mode slows nothing but grows memory; recheck behaviour with it off.
- ARC-managed `weak` references are zeroed; zombies surface mostly in MRC or unsafe code.

## Self-check
Write a deliberate `unsafe_unretained` delegate dangling case and verify the zombie log appears.
