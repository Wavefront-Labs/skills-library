---
id: computing-software.game-programming.unreal-engine.blueprint-communication
name: blueprint-communication
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, blueprints, blueprint-communication, event-dispatcher, casting, direct-references, game-programming]
level: practitioner
status: docs-checked
description: "Choose between direct references, event dispatchers, Blueprint interfaces and casting for Blueprint communication, using Epic's usage page and Event Dispatcher mechanics."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprint-communication-usage-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/event-dispatchers-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blueprint communication

**Goal:** pick the right way for Blueprints to pass information to each other.

## The four methods (Blueprint Communication Usage page)
| Method | Relationship per the page | Page's example |
|---|---|---|
| Direct Blueprint communication | one-to-one; needs a reference to the target Actor | a switch opens a specific door or light |
| Event Dispatcher | tell other "listening" Blueprints an event happened; listeners react independently | boss calls "OnDied"; Character celebrates, door opens, HUD flashes |
| Blueprint Interface | a common way to talk to multiple types of objects sharing some functionality; "like a contract" | car and tree both implement `OnTakeWeaponFire`; walls simply do not implement it and ignore the call |
| Cast | ask an object "are you a special version of that object"; fails if it is not | Cast To a Flying Character Blueprint to reach its flying function |

Page notes: interface callers can treat different types the same, and Blueprints that do not implement the interface
ignore the call. Cast examples include casting to the special GameMode Blueprint to run a respawn script and casting to
Cat, Dog or Bird children of an Animal Blueprint.

## Event Dispatcher mechanics (Event Dispatchers page)
- Create in the Blueprint Editor My Blueprint panel using the Event Dispatcher category; set tooltip, category and inputs
  in Details (Inputs > New, or Copy Signature from another event). Inputs send data to every bound event.
- The dispatcher's own graph is locked. Bind, unbind and assign add events to the event list; Call activates every
  stored event.
- Target pin: in a Blueprint Class it is automatically Self, so the event list changes for the whole class (every
  instance). In the Level Blueprint it must be connected to a reference to an instance, so only that instance changes.
- Event Dispatchers also let a Blueprint Class report to the Level Blueprint.

## Checked
Date: 2026-11-07. Read in full: Blueprint Communication Usage page and Event Dispatchers page (all sections), unversioned
en-us pages that state no engine version.
Removed as not on those pages: the coupling/"hard reference" load-size discussion, Size Map / Reference Viewer checks,
the soft-reference and C++ base class advice, the Get All Actors Of Class performance advice, the GameMode (server only)
and subsystem notes, the Level Blueprint "avoid" advice, and the Verify checklist.
Method: documentation only; no commands were run.
