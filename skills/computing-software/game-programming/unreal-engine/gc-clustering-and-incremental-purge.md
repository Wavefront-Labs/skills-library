---
id: computing-software.game-programming.unreal-engine.gc-clustering-and-incremental-purge
name: gc-clustering-and-incremental-purge
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gc-clustering, garbage-collection, hitches, memory, game-programming]
level: practitioner
status: docs-checked
description: "Reduce Unreal garbage collection hitches: GC clustering settings for actors, assets and Blueprints, purge timing, and the experimental incremental reachability console variables."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-object-handling-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/garbage-collection-settings-in-the-unreal-engine-project-settings", "https://dev.epicgames.com/documentation/en-us/unreal-engine/incremental-garbage-collection-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GC clustering and incremental purge

**Goal:** garbage collection that does not show up as a frame spike.

## How GC finds garbage
The engine builds a reference graph from a "root set"; UObjects not found by that search are removed. Keep a
`UPROPERTY` reference (or a UE container of object pointers) to anything you want to keep alive. Weak pointers do not
keep an object alive. Reachability analysis is multithreaded.

## Project Settings > Engine > Garbage Collection (settings reference page)
General: Time Between Purging Pending Kill Objects (seconds of game time), Flush Streaming On GC, Number Of Retries
Before Forcing GC (0 means GC is never forced). Optimization: Allow Parallel GC, Incremental BeginDestroy Enabled
(destroys a few objects each frame under a time limit), Multithreaded Destruction Enabled, Create Garbage Collector
UObject Clusters, Asset Clustering Enabled, Actor Clustering Enabled, Blueprint Clustering Enabled, Minimum GC
Cluster Size, Maximum Object Count Not Considered By GC and Size of Permanent Object Pool (cooked builds only).
Debug: Verify FGCObject names, Verify UObjects Are Not FGCObjects.

## Clustering (Unreal Object Handling page)
- Create Garbage Collector UObject Clusters is on by default. Related objects form a cluster checked as one object, so
  reachability is faster, but all items in a large cluster are unhashed and prepared for deletion in the same frame,
  which can hitch. Generally cluster creation improves GC performance.
- Merge GC Clusters joins clusters when an object in one references another; clearing the reference later does not
  split them. It needs cluster creation on, makes destruction less frequent but larger, and one reference to any
  member keeps the whole merged cluster alive.
- Actor Clustering Enabled: also set `bCanBeInCluster` true or override `CanBeInCluster` to return true. Actors and
  components are off by default, except Static Mesh Actors and Reflection Capture Components. Suited to actors destroyed
  together, such as static meshes freed only by unloading their sublevel.
- Blueprint Clustering Enabled clusters the Blueprint Generated Class and related data, not Blueprint instances.
- Shortening Time Between Purging Pending Kill Objects reduces the amount of garbage found per pass, which can avoid
  hitches from cleaning up many Actors at once.

## Incremental reachability (experimental)
The Incremental Garbage Collection page says to use caution when shipping with it. It splits reachability
analysis across frames with a soft per-frame time limit, tracking references through `TObjectPtr` properties (a write
barrier), so all `UPROPERTY` pointers must be `TObjectPtr` or GC may reclaim objects too early. Enable in
`DefaultEngine.ini`:
```ini
[ConsoleVariables]
gc.AllowIncrementalReachability=1
gc.AllowIncrementalGather=1
gc.IncrementalReachabilityTimeLimit=0.002
```
(the last is a 2 ms soft limit, which can still be exceeded). Debug CVars: `gc.DelayReachabilityIteration`
(default 10 frames), `gc.VerifyNoUnreachableObjects`, `gc.ContinuousIncrementalGC`. Known limitation: not fully
thread safe, so the page recommends single-threaded builds only, for example dedicated servers.

## Verify
- [ ] An Unreal Insights capture before and after a change shows the GC spike moved or removed (the incremental page
      uses Insights for its comparison).

## Checked
Date: 2026-11-07.
Read in full: Unreal Object Handling (Garbage Collection section and the rest), the Garbage Collection project
settings reference, and Incremental Garbage Collection. dev.epicgames.com; the settings page lists
"Pending Kill Enabled" and no defaults, and the pages carry no version number.
Removed as unconfirmed: the "default 61 s" figure and `gc.TimeBetweenPurgingPendingKillObjects` name, other `gc.*`
names besides those on the incremental page, the "UE5.4+" gate, `stat gc` / `log LogGarbage` / `ForceGarbageCollection`
advice, pooling advice, and the claim that clusters dissolve when referencing non-clustered objects (the page says merged
clusters do not dissolve).
Method: documentation only; no commands were run.
