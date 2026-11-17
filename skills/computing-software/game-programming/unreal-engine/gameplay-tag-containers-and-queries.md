---
id: computing-software.game-programming.unreal-engine.gameplay-tag-containers-and-queries
name: gameplay-tag-containers-and-queries
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, gameplay-tags, gameplay-tag-container, gameplay-tag-query, hierarchical-tags, tag-matching, game-programming]
level: practitioner
status: docs-checked
description: "Use FGameplayTagContainer and FGameplayTagQuery: HasTag vs HasTagExact, HasAny/HasAll, empty-input results, query expressions, queries in code, IGameplayTagAssetInterface."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/GameplayTags/FGameplayTagQuery"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gameplay tag containers and queries

**Goal:** express state and requirements as hierarchical tags rather than booleans and enums.

## Containers
Add an `FGameplayTagContainer` variable to an object to store multiple tags (use a bare `FGameplayTag` only when one
tag is enough). Edit with `AddTag`, `RemoveTag` and `AppendTags` (set union). Evaluate with:

| Call | Result (from the FGameplayTagContainer API page) |
|---|---|
| `HasTag(T)` | `{"A.1"}.HasTag("A")` true; `{"A"}.HasTag("A.1")` false; invalid tag always false |
| `HasTagExact(T)` | `{"A.1"}.HasTagExact("A")` false |
| `HasAny(C)` | `{"A.1"}.HasAny({"A","B"})` true; `{"A"}.HasAny({"A.1","B"})` false; empty or invalid C always false |
| `HasAnyExact(C)` | exact matches only |
| `HasAll(C)` | `{"A.1","B.1"}.HasAll({"A","B"})` true; `{"A","B"}.HasAll({"A.1","B.1"})` false; empty or invalid C always true |
| `HasAllExact(C)` | exact matches only; empty or invalid C still true |

Matching is one-way: a child tag in the container satisfies a parent query, not the reverse. The Gameplay Tags page
states the empty-input rule: an empty container as input returns false except for the All functions, because no
tags are missing from the source set. Other container calls listed on the API page: `AddLeafTag` (adds a tag and
removes direct parents, skips it if a child exists), `AddTagFast` (no uniqueness check), `GetGameplayTagParents`,
`Filter` / `FilterExact`, `MatchesQuery(Query)`.

## Queries
An `FGameplayTagQuery` is a logical query run against a container; a query that succeeds "matches". Expressions:
Any Tags Match, All Tags Match (true if the query is empty), No Tags Match (true if empty); root expressions Any,
All and No Expressions Match (All and No are true with no sub-expressions). Queries nest, so
`((A && B) || C) && !D` becomes `ALL( ANY( ALL(A,B), ALL(C) ), NONE(D) )`.
- Expose the struct to Blueprints and edit with the custom editor, or build natively. The API page's code example:
  `FGameplayTagQuery Q; Q.BuildQuery( FGameplayTagQueryExpression().AllTagsMatch().AddTag(FGameplayTag::RequestGameplayTag(FName("Animal.Mammal.Dog.Corgi"))).AddTag(...) );`
- Evaluate with `Q.Matches(Container)`. Static shortcuts: `MakeQuery_MatchAllTags`, `MakeQuery_MatchAnyTags`,
  `MakeQuery_MatchNoTags`, `MakeQuery_MatchTag`, `MakeQuery_ExactMatchAllTags`, `MakeQuery_ExactMatchAnyTags`.
- Internally a query is a memory-efficient byte stream; no need to expose internals to Blueprints.

## Reading tags from any object
Implement `IGameplayTagAssetInterface` and override `GetOwnedGameplayTags`: callers get an object's tags without
casting, and it creates a Blueprint-accessible method that fills a container. The Lyra sample's `ALyraTaggedActor`
is the page's example.

## Verify
- [ ] Each gating check has a case for a child tag, a parent tag and an empty input.

## Checked
Date: 2026-11-07.
Read in full: Gameplay Tags (Defining, Using Defined Gameplay Tags, Queries, Advanced Topics) and the
FGameplayTagQuery API page; also read the FGameplayTagContainer API page (function table) for the match examples.
All from dev.epicgames.com; they carry no version number in their text.
Removed as unconfirmed: Fast Replication and index-based replication claims, GAS replication modes, tag count
containers and `GetTagCount`, `AddLooseGameplayTag`, `MakeQuery_MatchAllTags(Required)` usage as a designer
workflow, `Level.5` advice, and leaf-tag advice.
Method: documentation only; no commands were run.
