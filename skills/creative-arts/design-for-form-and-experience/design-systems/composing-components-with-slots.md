---
id: creative-arts.design-for-form-and-experience.design-systems.composing-components-with-slots
name: composing-components-with-slots
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [component-composition, slots, component-slots, composition-over-configuration, compound-components, slot-api]
level: advanced
status: draft
description: "Compose components with slots and children: when to replace props with slots, compound components, nested instances in Figma and keeping accessibility intact."
sources:
  - "MDN Web Docs, HTML slot element (developer.mozilla.org)"
  - "Nathan Curtis, EightShapes articles on component APIs (medium.com/eightshapes-llc)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Composition and slots

Composition means building a component from parts supplied by the consumer rather than from configuration props. A **slot** is a named place in a component where content can be inserted.

## When to use slots
- A card has a header, body and footer that vary a lot: a `header` slot is simpler than props for every possible element.
- You need to place different controls (button, link, menu) in the same position.
- You find yourself adding many boolean props to toggle small parts (`showIcon`, `showBadge`, `showAction`).

## Implementation patterns
- **Children and named slots:** React children plus props that accept nodes (`header={...}`), or compound components (`<Card><Card.Header/><Card.Body/></Card>`); web components and frameworks such as Vue and Svelte offer `<slot>` or slot syntax natively.
- **Constrain slots** with documented allowed content and tests, otherwise accessibility and spacing break; give the container the layout and spacing rules and let children supply content.
- **Keep semantics in the parent:** roles, ARIA relationships, focus management belong in the component, not in each consumer.

## In Figma
Use nested instances with instance-swap properties for slots (see `...figma.nested-instances-and-instance-overrides`); Figma has also added native slot support in recent releases, so check the current Help Center for availability on your plan.

## Verify
- [ ] The slot has a documented content contract.
- [ ] Spacing and layout hold with varied slot content.
- [ ] Accessibility semantics still work with swapped content.
