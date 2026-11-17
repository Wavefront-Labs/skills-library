---
id: computing-software.game-programming.unreal-engine.gameplay-tag-matching-semantics
name: gameplay-tag-matching-semantics
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gameplay-tags, matchestag, hasany, hasallexact, game-programming]
level: practitioner
status: docs-checked
description: "Get Unreal gameplay tag container checks right: HasTag vs HasTagExact, HasAny/HasAll and the Exact variants, parent matching direction, and empty-container results."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/GameplayTags/FGameplayTagContainer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gameplay tag matching semantics

**Goal:** tag checks that mean what you think, especially with hierarchical tags.

## Hierarchy
Tags are hierarchical, separated by `.`: `Event.Movement.Dash` has three levels, `Event` the broadest and `Dash`
the most specific. A container holds tags "explicitly by adding them, and implicitly from adding child tags".

## Container checks (FGameplayTagContainer API page)
| Call | Behaviour |
|---|---|
| `HasTag(T)` | also checks parents: `{"A.1"}.HasTag("A")` true, `{"A"}.HasTag("A.1")` false; invalid T is always false |
| `HasTagExact(T)` | exact only: `{"A.1"}.HasTagExact("A")` false |
| `HasAny(C)` | `{"A.1"}.HasAny({"A","B"})` true, `{"A"}.HasAny({"A.1","B"})` false; empty or invalid C always false |
| `HasAnyExact(C)` | exact matches only; `{"A.1"}.HasAny({"A","B"})` false in the exact form; empty or invalid C false |
| `HasAll(C)` | `{"A.1","B.1"}.HasAll({"A","B"})` true, `{"A","B"}.HasAll({"A.1","B.1"})` false; empty or invalid C always true |
| `HasAllExact(C)` | exact matches only; empty or invalid C still true |

The Gameplay Tags page repeats the empty-input rule: an empty container input returns false except for the All
functions such as `HasAll`. If "no requirement" should pass for both Any and All checks, test emptiness
(`IsEmpty()`) yourself.

## Direction matters
The container is the "source" and the argument is what you ask about, so the child-in-container satisfies a
parent in the argument, not the other way round. Write requirement checks as `Owned.HasAll(Required)` and
negate `Owned.HasAny(Blocked)`.

## Other container helpers (same API page)
`GetGameplayTagParents()` returns a container with the tags and all their parents. `Filter(Other)` returns tags
matching any in Other, expanding parents; `FilterExact` requires exact matches. `AddTagFast` adds without a
uniqueness check. `MatchesQuery(Query)` runs an `FGameplayTagQuery`; query expressions are described in the
Gameplay Tags page (Any / All / No Tags Match and the root expressions).

## Verify
- [ ] A test table covers child, parent and sibling tags and empty inputs for each check you use.

## Checked
Date: 2026-11-07.
Read in full: Gameplay Tags (Evaluating Tags with Conditional Functions and Gameplay Tag Queries, plus the rest
of the page) and the FGameplayTagContainer API page including every function-table description. From dev.epicgames.com.
Removed as unconfirmed by these pages: all `FGameplayTag` member calls (`MatchesTag`, `MatchesTagExact`,
`MatchesAny`, `RequestDirectParent`; that API page is not cited), the C++ query-building snippet, GAS
`GetTagCount` / `HasMatchingGameplayTag` advice, the `RequestGameplayTag` assert claim, and the claim that
`AddTagFast` skips parent caching (the page says it skips the uniqueness check).
Method: documentation only; no commands were run.
