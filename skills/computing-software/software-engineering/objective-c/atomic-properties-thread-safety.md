---
id: computing-software.software-engineering.objective-c.atomic-properties-thread-safety
name: atomic-properties-thread-safety
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-thread-safety, atomic-properties-thread-safety]
level: practitioner
status: docs-checked
description: "Explain what atomic guarantees (whole-value get/set) and what it does not guarantee about thread safety."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/EncapsulatingData/EncapsulatingData.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocProperties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomic properties and thread safety
**Goal:** avoid false confidence in `atomic`.

```objc
@property NSObject *implicitAtomicObject;            // atomic by default
@property (atomic) NSObject *explicitAtomicObject;
@property (nonatomic) NSObject *nonatomicObject;
```
- Properties are atomic by default. Synthesized atomic accessors ensure a value is always fully retrieved by the getter or fully set by the setter, even when called simultaneously from different threads.
- `nonatomic` makes synthesized accessors set or return the value directly, with no guarantees under simultaneous access; it is faster.
- Atomicity is not the same as thread safety. If one thread changes a first name and last name through atomic setters while another reads both, each getter returns a complete string but the pair can be mismatched.
- In a reference-counted environment, a synthesized getter for a `strong`, `copy` or `retain` atomic property uses a lock and returns `[[value retain] autorelease]`.

## Gotchas
- The synchronization of atomic accessors is private, so a synthesized accessor cannot be combined with one you write for the same atomic readwrite property; the compiler warns. With `nonatomic` you can mix a synthesized setter with your own getter.
- Protecting a group of related properties (an invariant across several values) needs your own synchronization; this skill does not cover a specific mechanism.

## Self-check
Name one invariant in your class spanning two properties and confirm that atomic accessors alone do not protect it.

## Checked
2026-11-08. Confirmed against the archived "Programming with Objective-C" chapter on encapsulating data (Properties Are Atomic by Default) and the "Objective-C Programming Language" chapter on declared properties: atomic default, whole-value guarantee, nonatomic, first/last name example, lock with retain and autorelease, no mixing accessors. Removed: queue and lock strategy code, C11 atomics, immutable-snapshot pattern, Thread Sanitizer self-check (not on the pages). The pages are retired documents.
Method: documentation only; no commands were run.
