---
id: computing-software.web-development.react.drag-and-drop-with-dnd-kit
name: drag-and-drop-with-dnd-kit
category: computing-software
field: web-development
product: react
tags: [dnd-kit, drag-and-drop, sortable-lists, keyboard-dragging, react]
level: practitioner
status: docs-checked
description: "Building accessible drag and drop in React with dnd-kit: DndContext, sensors including keyboard, sortable lists, drag overlays, announcements, and non-drag alternatives."
sources:
  - https://dndkit.com/legacy/presets/sortable/sortable-context
  - https://dndkit.com/legacy/guides/accessibility
  - https://dndkit.com/legacy/api-documentation/sensors/pointer
  - https://dndkit.com/legacy/api-documentation/sensors/keyboard
  - https://github.com/clauderic/dnd-kit
  - https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drag and drop with dnd-kit

dnd-kit is headless and supports pointer, mouse, touch and keyboard sensors plus screen-reader announcements and live regions. This skill covers the classic `@dnd-kit/core` and `@dnd-kit/sortable` packages (documented under `/legacy` on dndkit.com); the repository's current packages are `@dnd-kit/react` (and dom, vue, svelte, solid adapters) with a different API, so check which one you install.

## 1. Sortable list
```jsx
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from "@dnd-kit/core";
import { SortableContext, arrayMove, sortableKeyboardCoordinates, useSortable, verticalListSortingStrategy } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

function List({ items, setItems }) {
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 6 } }),   // don't hijack clicks
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }));
  return (
    <DndContext sensors={sensors} collisionDetection={closestCenter}
      onDragEnd={({ active, over }) => { if (over && active.id !== over.id)
        setItems(xs => arrayMove(xs, xs.findIndex(x => x.id === active.id), xs.findIndex(x => x.id === over.id))); }}>
      <SortableContext items={items.map(i => i.id)} strategy={verticalListSortingStrategy}>
        <ul>{items.map(i => <Row key={i.id} item={i} />)}</ul>
      </SortableContext>
    </DndContext>);
}
function Row({ item }) {
  const { attributes, listeners, setNodeRef, setActivatorNodeRef, transform, transition, isDragging } = useSortable({ id: item.id });
  return (
    <li ref={setNodeRef} style={{ transform: CSS.Transform.toString(transform), transition, opacity: isDragging ? .5 : 1 }}>
      <button ref={setActivatorNodeRef} {...attributes} {...listeners} aria-label={`Reorder ${item.name}`}>⠿</button>
      {item.name}
    </li>);
}
```
- Put listeners on a **handle** so inner buttons/inputs remain usable.
- Keyboard: focus the handle, Space or Enter to pick up and to drop, arrow keys to move, Escape to cancel (the Keyboard sensor defaults).
- `items` is the sorted array of unique ids, in the same order the items render; ids must be stable (not array indexes).

## 2. Polish
- `DragOverlay` renders a floating copy; the docs recommend it for items in scrollable containers, items that move between containers, virtualised lists and smooth drop animations. Keep it mounted and conditionally render its children.
- Customise the `announcements` and `screenReaderInstructions` props of `DndContext` to say "Picked up Task 3. Position 3 of 8" in your language.
- Touch: use a delay constraint (`delay` in ms, `tolerance` in px) so the page can still scroll, and set `touch-action: none` on the handle only when the item sits in a scrollable list.

## 3. Alternatives required
WCAG 2.5.7 requires a single-pointer, non-drag way to do the same thing: "Move up/down" buttons or a "Move to..." menu per item.

## 4. Persisting
Optimistically update local order, send the new order (or `{ id, beforeId }`) to the server, roll back on failure.

## Verify
- [ ] Reorder works by mouse, touch and keyboard; screen reader announces pick-up, moves and drop; move buttons provide a non-drag alternative; order persists after reload.

## Checked

Checked 2026-10-25 against the clauderic/dnd-kit repository (main, pushed 2026-10-22; legacy docs under apps/docs/docs/legacy, @dnd-kit/react 0.5.1) and the W3C WCAG repository. Confirmed: pointer sensor distance and delay constraints and the touch-action recommendation; Keyboard sensor start and end keys Space and Enter, cancel Escape; `setActivatorNodeRef` on useSortable; `SortableContext` takes a sorted array of unique ids; `announcements` and `screenReaderInstructions` props on DndContext; DragOverlay guidance; WCAG 2.2 Understanding page "Dragging Movements" (2.5.7). Added the note that the current packages are `@dnd-kit/react`. Removed the unconfirmed HTML5 drag-and-drop comparison, the specific touch delay values, the kanban handler advice and the fractional-indexing library name.

Method: documentation only; no commands were run.
