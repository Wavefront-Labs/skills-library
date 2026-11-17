---
id: computing-software.game-programming.unreal-engine.shared-derived-data-cache
name: shared-derived-data-cache
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-packaging, derived-data-cache, ddc, zen-server, game-programming]
level: practitioner
status: draft
description: "Speed up Unreal editor startup and cooks with a shared Derived Data Cache: local/shared/cloud DDC, Zen server, DDC graph config, pak DDC and diagnosing misses."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/derived-data-cache", "https://dev.epicgames.com/documentation/en-us/unreal-engine/zen-storage-server-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shared Derived Data Cache

**Goal:** nobody recompiles shaders or re-derives textures that a teammate or CI already built.

## What DDC stores
Compiled shaders, compressed textures, mesh build data (Nanite), audio formats, PSOs, motion matching
indexes — results keyed by input hash + version. Misses trigger expensive local builds ("Compiling
Shaders 30,000").

## Layers (UE5 DDC graph)
- **Local**: `Zen` local server (UE 5.1+ default; data under Local AppData/UnrealEngine/Common/Zen) or
  file-system cache.
- **Shared**: network file share (fast LAN), or a shared Zen server.
- **Cloud**: Unreal Cloud DDC (Horde storage / S3-backed) for distributed teams.
- **Pak**: `-run=DerivedDataCache -fill` output shipped with installed builds.

## Configure
Project `Config/DefaultEngine.ini`:
```ini
[InstalledDerivedDataBackendGraph]  ; or [DerivedDataBackendGraph]
Shared=(Type=FileSystem, ReadOnly=false, Clean=false, Flush=false, DeleteUnused=true, UnusedFileAge=10, FoldersToClean=10, MaxFileChecksPerSec=1, Path=\\fileserver\DDC, EnvPathOverride=UE-SharedDataCachePath, EditorOverrideSetting=SharedDerivedDataCache)
```
Per-user override: env var `UE-SharedDataCachePath=\\fileserver\DDC` (or `None` to disable when
offline), or Editor Preferences > Global > Shared DDC.

## CI warms the cache
Run a nightly cook / `UnrealEditor-Cmd <proj> -run=DerivedDataCache -fill -TargetPlatform=Windows`
with write access to the shared DDC so morning editors hit warm data.

## Diagnosing
- Startup log prints the backend graph and which layers are reachable.
- `-ddc=NoShared` to test local only; `-ddc=Cold` to bypass.
- Cook/editor summary: "DDC Summary" with hit/miss percentages per layer (`-DDCSummary` style logs at
  exit); Editor: Tools > Derived Data > Cache Statistics.
- Slow shared DDC over VPN is worse than none — use cloud DDC or disable shared for remote staff.

## Gotchas
- Different engine builds (custom changes to shaders) produce different keys; share DDC per engine
  version/branch, not across incompatible ones.
- Read-only shared DDC for artists, write from CI only, avoids corruption from flaky clients.

## Verify
- [ ] Fresh machine with shared DDC opens the project without mass shader compiles.
- [ ] DDC statistics show high shared hit rate after CI fill.
