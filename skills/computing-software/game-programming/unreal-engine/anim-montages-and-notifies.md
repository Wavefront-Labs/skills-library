---
id: computing-software.game-programming.unreal-engine.anim-montages-and-notifies
name: anim-montages-and-notifies
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-animation, anim-montage, anim-notify, anim-notify-state, montage-sections, slots, playmontage, montage-replication, game-programming]
level: practitioner
status: docs-checked
description: "Use Unreal Anim Montages and Animation Notifies: slots and slot groups, sections, child montages, notify types, montage notifies, trigger settings and root-motion replication."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-montage-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-notifies-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anim Montages and notifies

**Goal:** one-shot gameplay animations (attacks, reloads, interactions) as Montages, with timing events from Notifies.

## Montage basics (Animation Montage page)
- A Montage combines several Animation Sequences in one asset and is played back under Blueprint control; it can also
  replicate Root Motion animation in network games.
- Sequences are organised into Slot Groups and Slots. By default, Sequences in the same Slot and Slot Group override
  any other sequence when triggered. Do not overlap sequences in one Slot: they interfere if played at once.
- Slot Groups can be set up to play on separate parts of the character through the Anim Graph (the page's example:
  an upper-body slot and a lower-body slot played at the same time). With several Slots, keep the end-to-end timing of
  the animations the same length.
- Montage Sections can be played in any order at runtime. Set the default order in the Montage Sections Panel (select
  Clear, then click the white box beside a section to choose its next section); dynamic transitions use Blueprints.
- Create: right-click in the Content Browser > Animation > Animation Montage, or right-click an Animation Sequence >
  Create > Create AnimMontage.
- Child Montages (right-click a Montage > Create Child Montage, name gets `_Child` appended) inherit the parent, open
  read-only, can override a segment with another animation (play rate and start/end adjusted automatically), and
  cannot be parents of other child montages.

## Notify types (Animation Notifies page)
- **Notify**: single event at a time (Particle Effect, Sound, Clothing Simulation, Reset Dynamics entries).
- **Skeleton Notify**: custom Notify stored on the Skeleton asset (so the Skeleton must be saved), used as an event
  in an Animation Blueprint Event Graph or Transition Graph through Add Anim Notify Event.
- **Notify State**: works over a duration with a start, an update and an end event.
- **Sync Marker**: also saved on the Skeleton; used for marker-based syncing (see the Sync Groups page).
- **Custom classes**: Content Browser > Add > Blueprint Class > `AnimNotify` or `AnimNotifyState`. Overridable
  functions on the page: Get Default Trigger Weight Threshold, Get Notify Name, Received Notify (plain notifies),
  Received Notify Begin / End / Tick (states).

## Montage notifies
Added in montages only: Montage Notify (fires On Notify Begin), Montage Notify Window (On Notify Begin and On Notify
End) and Disable Root Motion (a state that suppresses root motion so user input can control the character, since
montages lock out input by default). The first two require playing the montage with the Play Montage node, not Play
Anim Montage.

## Notify properties worth knowing
- Montage Tick Type: `Queued` is less precise, asynchronous and more performant; `Branching Point` is more precise,
  synchronous and higher cost, and the page recommends it for gameplay-altering decisions.
- Trigger Weight Threshold (and Min Trigger Weight): how much blend weight the animation needs to fire the notify;
  the page gives a default of 0.00001. Only relevant when blended.
- Trigger on Dedicated Server enables execution on dedicated servers; Trigger on Follower enables firing when the
  animation is a sync-group follower (by default only leaders fire notifies); Notify Trigger Chance 0 to 1; Notify
  Filter Type can filter by LOD.
- Link Method (montage notifies): Absolute, Relative or Proportional.

## Networking
The Montage page says replication of root motion happens by default but you first replicate the Play Montage node
manually with an RPC, and only root motion replication and correction is carried over by that.

## Checked
Date: 2026-11-07. Read in full: Animation Montage page (all sections including Child Montages and Network Games) and
Animation Notifies page (all sections, including Montage Notifies, Common Notify Properties and Custom Notify
Classes), unversioned en-us pages that state no engine version.
Removed because no readable page confirms them: the whole `Montage_Play` / `Montage_SetEndDelegate` C++ block and its
delegate signatures (the `UAnimInstance::Montage_Play` API URL returns an empty page and was dropped from `sources`),
`ACharacter::PlayAnimMontage`, GAS `PlayMontageAndWait` and `RepAnimMontageInfo`, the `VisibilityBasedAnimTickOption`
advice, the `DefaultGroup.UpperBody` slot name, the claim that Queued is the default, and the invented Verify checklist.
Method: documentation only; no commands were run.
