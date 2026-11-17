---
id: computing-software.game-programming.unreal-engine.gameplaymessagesubsystem-tag-routed-events
name: gameplaymessagesubsystem-tag-routed-events
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gameplay-tags, gameplay-message-subsystem, gameplay-message-router, event-bus-unreal, game-programming]
level: practitioner
status: draft
description: "Decouple Unreal systems with the GameplayMessageRouter's UGameplayMessageSubsystem: tag channels, struct payloads, partial matching and listener handle lifetime."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-sample-game-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag-routed events with GameplayMessageSubsystem

**Goal:** UI, audio, achievements and gameplay communicate through typed messages on gameplay-tag
channels, without references to each other (Lyra's pattern).

## Setup
The GameplayMessageRouter plugin ships with the Lyra sample (copy `Plugins/GameplayMessageRouter`
into your project, add `"GameplayMessageRuntime"` to Build.cs). It provides
`UGameplayMessageSubsystem` (a GameInstance subsystem).

## Broadcast
```cpp
USTRUCT(BlueprintType)
struct FEliminationMessage { GENERATED_BODY()
    UPROPERTY(BlueprintReadWrite) TObjectPtr<APlayerState> Instigator;
    UPROPERTY(BlueprintReadWrite) TObjectPtr<APlayerState> Target; };
UE_DEFINE_GAMEPLAY_TAG_STATIC(TAG_Msg_Elimination, "Message.Elimination");
FEliminationMessage Msg{Killer, Victim};
UGameplayMessageSubsystem::Get(this).BroadcastMessage(TAG_Msg_Elimination, Msg);
```
## Listen
```cpp
FGameplayMessageListenerHandle Handle;
void UKillFeed::NativeConstruct() {
    Super::NativeConstruct();
    Handle = UGameplayMessageSubsystem::Get(this).RegisterListener(TAG_Msg_Elimination, this,
        &UKillFeed::OnElimination);   // void OnElimination(FGameplayTag Channel, const FEliminationMessage& M)
}
void UKillFeed::NativeDestruct() { Handle.Unregister(); Super::NativeDestruct(); }
```
Blueprint: "Listen for Gameplay Messages" async node (auto-cleans with the owning object).

## Matching
`EGameplayMessageMatch::ExactMatch` (default) or `PartialMatch`: a listener on `Message.Combat`
with partial match receives `Message.Combat.Hit` and `Message.Combat.Elimination`. Payload type must
match the broadcast struct, or the listener logs an error and is skipped.

## Rules
- Messages are **local and synchronous**: not replicated. Broadcast on each machine (e.g. from
  a multicast RPC or OnRep) if clients need them.
- Listeners called in registration order, immediately inside BroadcastMessage — don't destroy the
  broadcaster from a handler without care.
- Use for "something happened" notifications, not request/response.

## Gotchas
- Forgetting `Unregister` on objects that outlive the listener target leaks handlers; weak binding
  skips dead objects but the entry remains until unregistered.
- Struct mismatch between broadcaster and listener only shows as a runtime log error.

## Verify
- [ ] Kill feed updates without any reference from GameMode to UI.
- [ ] Destroying the widget then broadcasting: no crash, no handler call.
