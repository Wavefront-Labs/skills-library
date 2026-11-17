---
id: computing-software.game-programming.unreal-engine.umg-listview-and-tileview
name: umg-listview-and-tileview
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, umg, listview, tileview, userobjectlistentry, game-programming]
level: practitioner
status: draft
description: "Build virtualised Unreal UMG lists with ListView/TileView: item objects, IUserObjectListEntry entry widgets, selection, refresh and gamepad navigation."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-lists-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/UMG/Components/UListView"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UMG ListView and TileView

**Goal:** long lists (inventory, server browser, chat) that create only visible entry widgets and
recycle them.

## Pieces
- **Item**: any `UObject` holding data (`UInventoryItemData`). ListView stores items, not widgets.
- **Entry widget**: a `UUserWidget` implementing `IUserObjectListEntry`; set as the ListView's Entry
  Widget Class.
- ListView generates entries for visible rows and reassigns items to them on scroll.

## Entry implementation
```cpp
UCLASS()
class UInvEntry : public UUserWidget, public IUserObjectListEntry {
    GENERATED_BODY()
protected:
    virtual void NativeOnListItemObjectSet(UObject* Item) override {
        const auto* D = CastChecked<UInventoryItemData>(Item);
        NameText->SetText(D->DisplayName); CountText->SetText(FText::AsNumber(D->Count));
    }
    virtual void NativeOnItemSelectionChanged(bool bSelected) override { /* highlight */ }
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UTextBlock> NameText;
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UTextBlock> CountText;
};
```
Blueprint: implement the "User Object List Entry" interface and the On List Item Object Set event.

## Populating
```cpp
List->SetListItems(Items);           // TArray<UObject*>
List->AddItem(NewItem); List->RemoveItem(Old);
List->RequestRefresh();              // re-run entry set for visible rows after data changes
List->OnItemClicked().AddUObject(this, &UInvScreen::HandleClicked);
List->ScrollIndexIntoView(i); List->SetSelectedIndex(i);
```

## Rules
- Entry widgets are recycled: **never store per-item state in the entry**; read everything from the
  item object in `NativeOnListItemObjectSet`, and reset visual state there.
- Items must stay referenced (UPROPERTY array somewhere) or GC removes them.
- TileView: set Entry Width/Height; TreeView for hierarchies (`OnGetItemChildren`).

## Gamepad
Entries are focusable when "Is Focusable" is set; ListView handles up/down navigation. CommonUI's
`UCommonListView` integrates with CommonUI input routing.

## Gotchas
- Variable-height entries are supported in ListView (not TileView) but large height variance can
  jitter scroll; prefer fixed height for big lists.
- Changing item data without `RequestRefresh` leaves visible entries stale.

## Verify
- [ ] 5,000 items: Widget Reflector shows only ~visible count of entry widgets.
- [ ] Scroll fast: entries never show another item's highlight state.
