---
id: computing-software.game-programming.unity.eventsystem-and-pointer-handlers
name: eventsystem-and-pointer-handlers
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-ui, unity-event-system, ipointerclickhandler, ugui, raycasters, drag-and-drop, game-programming]
level: practitioner
status: docs-checked
description: "Route clicks, drags and hovers through Unity's EventSystem: input modules, the three raycasters and the IPointer/IDrag handler interfaces, for UI and world objects."
sources: ["https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/EventSystem.html", "https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/SupportedEvents.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventSystem and pointer handlers

**Goal:** UI and world objects receive pointer events through the Event System by implementing handler interfaces.

## Pieces
The Event System component is a manager and facilitator between modules. Its roles: manage which GameObject is selected,
which Input Module is in use, raycasting (if required), and updating all Input Modules as required.
- **Input Module:** holds the logic for handling input, managing event state and sending events to scene objects. Only
  one Input Module can be active in the Event System at a time, and Input Modules must be components on the same
  GameObject as the Event System component.
- **Raycasters** work out what the pointer is over; Input Modules commonly use the raycasters configured in the scene.
  Three are provided: Graphic Raycaster (UI elements), Physics 2D Raycaster (2D physics elements), Physics Raycaster
  (3D physics elements).

## Handlers
Events are provided as interfaces you implement on a MonoBehaviour; with a valid Event System they are called at the
right time (the page states this for the Standalone and Touch Input Modules). Method and meaning:
- `IPointerEnterHandler.OnPointerEnter`, `IPointerExitHandler.OnPointerExit`: pointer enters or exits the object.
- `IPointerDownHandler.OnPointerDown`: pointer pressed on the object. `IPointerUpHandler.OnPointerUp`: pointer
  released (called on the GameObject the pointer is clicking).
- `IPointerClickHandler.OnPointerClick`: pointer pressed and released on the same object.
- `IInitializePotentialDragHandler.OnInitializePotentialDrag`: a drag target is found; can initialise values.
- `IBeginDragHandler.OnBeginDrag`, `IDragHandler.OnDrag`, `IEndDragHandler.OnEndDrag`: called on the drag object when
  dragging is about to begin, is happening, and finishes.
- `IDropHandler.OnDrop`: called on the object where a drag finishes.
- `IScrollHandler.OnScroll`: mouse wheel scrolls.
- `IUpdateSelectedHandler.OnUpdateSelected` (each tick on the selected object), `ISelectHandler.OnSelect`,
  `IDeselectHandler.OnDeselect`, `IMoveHandler.OnMove` (left, right, up, down), `ISubmitHandler.OnSubmit`,
  `ICancelHandler.OnCancel`.

```csharp
public class Slot : MonoBehaviour, IPointerClickHandler {
    public void OnPointerClick(PointerEventData e) { /* react to the click */ }
}
```

## Non-UI objects
With a 2D or 3D raycaster configured in the scene, a non-UI object receives messages from the Input Module once a
script on it implements one of the event interfaces (see the IPointerEnterHandler and IPointerClickHandler script
reference pages).

## Custom input
To write a custom Input Module, send events that existing UI components support; to extend with your own events, see
the Messaging System documentation.

## Checked
Date: 2026-11-07.
Read in full: ugui 2.0 "Event System" and "Supported Events" manual pages (both short; no code tabs or includes).
Removed as unconfirmed by those pages: the one-EventSystem-per-scene warning, InputSystemUIInputModule replacement
advice, Raycast Target toggle, event bubbling to parents, `dragThreshold`, `IsPointerOverGameObject`/`RaycastAll`
guidance and its Input System caveat, drag-handler pairing claim, and the invented Verify checklist. The code sample
is now a minimal illustration only.
Method: documentation only; no commands were run.
