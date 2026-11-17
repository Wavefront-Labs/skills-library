---
id: computing-software.game-programming.gameplay-programming.inventory-system-design
name: inventory-system-design
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-state, inventory-system, item-stacks, item-definitions, equipment-slots, grid-inventory, transactions, item-instances, game-programming]
level: practitioner
status: draft
description: "Design a game inventory: item definitions vs instances, stacking rules, slot and grid layouts, atomic move/split/merge operations, events for UI, and save/network concerns."
sources: ["https://gameprogrammingpatterns.com/type-object.html", "https://www.gameenginebook.com/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-sample-game-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inventory system design

**Goal:** an inventory that never duplicates or loses items, supports stacks, equipment and UI, and
saves/replicates cleanly.

## Data model
```
ItemDefinition (shared, authored data; Type Object)
  id: "potion_small", maxStack: 20, category: Consumable, icon, weight, gridSize: 1x1
ItemInstance (per item that exists)
  instanceId (GUID, only needed for unique items), defId, count, durability, rolledStats
Inventory
  slots: array<ItemInstance?> (fixed capacity) or list for unlimited bags
EquipmentSlots
  map<SlotType, ItemInstance?>
```
Stackable items (ammo, potions) are a count on one instance; unique items (a sword with rolled stats)
have count 1 and their own state. Never store item state in the UI.

## Core operations (all validated, all-or-nothing)
```
add(def, count) -> remainder
  1. fill existing stacks of def up to maxStack
  2. put the rest into empty slots
  3. return what did not fit (caller drops it on the ground or refuses pickup)
remove(def, count) -> bool        # check total available first, then remove; never partial
move(fromSlot, toSlot)            # same def & stackable -> merge (overflow stays); else swap
split(slot, n)                    # new stack of n in first empty slot
canEquip(item, slot)              # category/level/class checks
```
Implement each as a transaction: compute the result on a copy or verify all preconditions first,
then mutate. Partial failure is how duplication and loss bugs happen.

## Grid inventories (Diablo/Resident Evil style)
Store occupancy grid + list of (item, position, rotated). Placement check scans the item's footprint
for free cells; `findFirstFit` scans row-major. Rotation swaps width/height.

## Events
Emit `onSlotChanged(slotIndex)` / `onInventoryChanged` after each committed operation; UI listens and
redraws affected slots. Do not let UI call mutating operations other than through the same API that
gameplay uses.

## Save and network
- Save: list of (slot, defId, count, instance state). Load must tolerate removed definitions (drop
  with a log) and changed maxStack (split overflow).
- Multiplayer: server owns the inventory. Clients send requests (`RequestMove(from, to)`), server
  validates and replicates the changed slots. Never trust a client-reported item or count.
  Unreal: `FFastArraySerializer` for efficient slot replication (as in Lyra's inventory).

## Tests worth having
Property-based test: random sequences of add/remove/move/split; invariant `sum(count per def)` equals
what was added minus removed, and no slot exceeds maxStack.

## Verify
- [ ] Invariant test passes 100k random operations.
- [ ] Full inventory pickup returns the correct remainder; nothing disappears.
- [ ] Rapid double-clicks/drag spam in UI cannot duplicate items (server validation in multiplayer).
