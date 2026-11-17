---
id: computing-software.software-engineering.perl.accessors-encapsulation-roles
name: accessors-encapsulation-roles
category: computing-software
field: software-engineering
product: perl
tags: [perl, accessors, encapsulation, role-tiny, class-accessor, class-tiny, perlootut, accessors-encapsulation-roles]
level: practitioner
status: docs-checked
description: "Use accessors, keep objects opaque, pick an OO helper (Moose, Moo, Class::Accessor, Class::Tiny) and compose behaviour with Role::Tiny roles."
sources: ["https://perldoc.perl.org/perlootut", "https://metacpan.org/pod/Role::Tiny"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessors, encapsulation and Role::Tiny

**Goal:** safe attribute access and composition without hand-rolling an OO system.

## Encapsulation and accessors (perlootut)
- Most Perl objects are blessed hashes, but treat the internal structure as opaque. Access attributes only through accessor methods (getters, setters/mutators).
- Attributes are typically read-only (set at construction) or read-write.
- Encapsulation separates public API from private implementation, so the implementation can change without breaking callers, and makes classes easier to subclass.
- The recommended OO systems generate accessors and a constructor, so you should never touch the hash directly.
- Writing classes from scratch is discouraged; even the smallest helper removes boilerplate.

## Choosing a helper (perlootut)
| Module | Notes |
|---|---|
| Moose | Maximal: `has`, built-in roles, type checks (`isa => 'Bool'`), introspection, MooseX ecosystem. Slower to load, has dependencies and needs a compiler. |
| Moo | Subset of Moose with the same end-user API for shared features; no XS dependencies; usually faster to load; Moose can extend Moo classes and consume Moo roles. |
| Class::Accessor | Pure Perl, no non-core dependencies. `use Class::Accessor 'antlers'` gives Moose-like `has path => (is => 'ro')`; only `is` is supported. |
| Class::Tiny | `use Class::Tiny qw(path content last_mod_time)`; all accessors read-write; generates constructor; Class::Tiny::Antlers for Moose-like syntax. |

If you would otherwise use multiple inheritance, use roles instead. Role::Tiny works with Class::Accessor and Class::Tiny; Moose has its own roles.

## Role::Tiny (POD)
```perl
package Some::Role;
use Role::Tiny;
requires 'name';                  # consumer must implement it
sub describe { my $s = shift; 'I am ' . $s->name }
around baz => sub { ... };        # modifiers via Class::Method::Modifiers

package Some::Class;
use Role::Tiny::With;
with 'Some::Role';
sub name { 'thing' }
```
- All subs created after `use Role::Tiny` are composed as role methods; subs imported before it are not (use namespace::clean for extra control).
- If the class already defines a method, the role's version is not composed in (the class wins); a merely inherited method is overridden by the role's.
- A `requires` method that is missing makes role application fail loudly.
- Two roles in a single `with` that provide the same method raise an exception unless the class provides the method. To resolve in favour of one role, use separate `with` statements; the docs say more complex conflict resolution calls for refactoring.
- `before`, `after`, `around` need Class::Method::Modifiers, which is lazily loaded and not a declared dependency: depend on both modules.
- `Role::Tiny::does_role($obj_or_class, $role)` tests composition; `->does` is installed on consuming classes (unless they have one) and Role::Tiny overrides `DOES` unless a class in the hierarchy provides it. Other helpers: `make_role`, `apply_roles_to_package`, `apply_roles_to_object` (reblesses), `create_class_with_roles`, `is_role`.
- Role::Tiny has no attributes; for roles with attributes see Moo::Role.

## Self-check
- [ ] Removing the required `name` method from the consuming class makes `with` die.
- [ ] No caller reaches into `$obj->{field}`.

## Checked
Method: 2026-11-08 read the full perlootut and Role::Tiny POD (MetaCPAN API plain-text export). Removed claims the pages do not state: Hash::Util::lock_keys, inside-out objects with FieldHash, returning copies of internal refs, the "define methods before `with`" failure mode (the Role::Tiny synopsis puts `with` before the class subs), and `Role::Tiny->does_role` (the docs use the function form). The hand-written closure accessor example was dropped.
