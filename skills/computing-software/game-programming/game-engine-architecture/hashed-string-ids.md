---
id: computing-software.game-programming.game-engine-architecture.hashed-string-ids
name: hashed-string-ids
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, engine-support-systems, string-id, string-hashing, fnv1a, compile-time-hash, name-table, interned-strings, fname, stringname, game-programming]
level: practitioner
status: draft
description: "Replace runtime string comparisons with hashed string ids: FNV-1a/xxHash compile-time hashing, debug name tables, collision detection, and engine equivalents (FName, StringName)."
sources: ["https://www.gameenginebook.com/", "http://www.isthe.com/chongo/tech/comp/fnv/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/fname-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hashed string ids

**Goal:** identify assets, animation events, bones, tags and messages by string-like names without
string compares or allocations at runtime (Gregory, GEA ch. 6.4 "Strings").

## The idea
Hash the string once (ideally at compile time) to a 32- or 64-bit integer and compare integers.
Keep the original string in a debug table for logging.
```cpp
constexpr uint64_t fnv1a64(const char* s, uint64_t h = 0xcbf29ce484222325ull) {
    return *s ? fnv1a64(s + 1, (h ^ (uint8_t)*s) * 0x100000001b3ull) : h;
}
struct StringId {
    uint64_t value;
    constexpr explicit StringId(uint64_t v) : value(v) {}
    friend constexpr bool operator==(StringId a, StringId b) { return a.value == b.value; }
};
consteval StringId operator""_sid(const char* s, size_t) { return StringId(fnv1a64(s)); }

switch (evt.id.value) {                    // integers work in switch
    case "footstep"_sid.value: playFootstep(); break;
    case "hit_frame"_sid.value: applyHit(); break;
}
```
Runtime-built strings (from data files) are hashed at load time with the same function.

## Debug name table
```cpp
StringId intern(std::string_view s) {
    StringId id(fnv1a64_runtime(s));
#if !SHIPPING
    auto [it, inserted] = g_names.try_emplace(id.value, s);
    assert(inserted || it->second == s && "string id collision");   // detect collisions
#endif
    return id;
}
const char* debugName(StringId id);  // "unknown" in shipping
```
Tools can also emit a hash->string dictionary file at build time for crash reports and logs.

## Choosing the hash
- 32-bit: compact, but birthday collisions become likely around tens of thousands of strings
  (~1% chance near 10k). Fine with collision checks in dev builds for small sets.
- 64-bit (FNV-1a 64, xxHash64): collisions practically negligible for game-sized name sets.
- Normalise before hashing where appropriate (lowercase asset paths, forward slashes).
- Hash values must be stable across platforms and versions if stored in data files; never use
  `std::hash` (implementation-defined).

## Engine equivalents
- **Unreal FName**: interned in a global name table, compared by index; case-insensitive; with
  instance number suffix. `FName` for identifiers, `FString` for mutable text, `FText` for UI.
- **Godot StringName**: interned, pointer comparison; literal syntax `&"name"` in GDScript.
- **Unity**: `Animator.StringToHash`, `Shader.PropertyToID` for the same purpose.

## Verify
- [ ] Dev-build collision assert never fires across all project strings (run over the asset database).
- [ ] Profiling shows no strcmp/string allocations in event dispatch hot paths.
- [ ] Logs show readable names for ids in development builds.
