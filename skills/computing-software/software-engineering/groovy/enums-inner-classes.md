---
id: computing-software.software-engineering.groovy.enums-inner-classes
name: enums-inner-classes
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, enums-inner-classes]
level: practitioner
status: docs-checked
description: "Enum definitions with fields and methods, anonymous inner classes, and static nested classes."
sources:
  - https://groovy-lang.org/objectorientation.html
  - https://groovy-lang.org/semantics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums and inner/anonymous classes
```groovy
enum State { up, down }
State st = 'up'                      // String to enum coercion, no `as` needed
assert st == State.up
def val = "up"; State s2 = "${val}"  // a GString works too
// State bad = 'not an enum value'   // IllegalArgumentException at runtime

class Outer {
    private String privateStr = 'some string'
    class Inner { def methodA() { println "${privateStr}." } }   // inner class reads private members of Outer
    def start() {
        new Thread(new Runnable() { void run() { println "${privateStr}." } }).start()  // anonymous inner class
    }
}
class Computer { class Cpu { int coreNumber; Cpu(int n) { coreNumber = n } } }
assert 4 == new Computer().new Cpu(4).coreNumber    // Groovy 3+ Java-style inner instantiation
```
- Inner classes are defined inside another class; the enclosing class uses them as usual, and an inner class can access members of the enclosing class even when private. Other classes cannot access them.
- Anonymous inner classes avoid defining a class used only once (`new Runnable() { ... }`).
- Enum coercion in `switch`: `case 'up':` string labels match enum values; return types coerce implicitly, but passing a String to a method that takes the enum still needs an explicit `as State`.

## Self-check
Run the snippet.

## Checked

Checked 2026-11-09 against groovy-lang.org/objectorientation.html (section 2.2 Inner class and 2.2.1 Anonymous inner class) and groovy-lang.org/semantics.html (3.5 String to enum coercion), both read in the relevant sections.
Confirmed: inner class access to private enclosing members, anonymous inner class form, Groovy 3+ `outer.new Inner(...)` syntax, String and GString to enum coercion, the IllegalArgumentException on a bad value, `switch` and `as` coercion rules.
Removed as unconfirmed: enum constructors with fields and `valueOf`/`values()` usage, the static nested class note, anonymous-class `this` capture in scripts, and the `@CompileStatic` closure note.

Method: documentation only; no commands were run.
