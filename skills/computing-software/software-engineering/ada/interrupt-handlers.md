---
id: computing-software.software-engineering.ada.interrupt-handlers
name: interrupt-handlers
category: computing-software
field: software-engineering
product: ada
tags: [ada, interrupt-handlers]
level: advanced
status: draft
description: "Attach Ada interrupt handlers using protected procedures with Interrupt_Handler / Attach_Handler and ceiling priorities."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/Ada_For_The_Embedded_C_Developer/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interrupt handling with protected procedures
```ada
protected Button with Interrupt_Priority => System.Interrupt_Priority'Last is
   procedure Handler with Attach_Handler => Ada.Interrupts.Names.Some_IRQ;
end Button;
```
- Handler procedure is a protected procedure without parameters; runs at interrupt priority.
- `Interrupt_Handler` (dynamic attach via `Ada.Interrupts.Attach_Handler`) vs `Attach_Handler` (static).
- Names come from `Ada.Interrupts.Names` in the runtime.
## Gotchas
- Don't call blocking ops in handlers.
## Self-check
Trigger the IRQ in simulation/QEMU and count handler entries.
