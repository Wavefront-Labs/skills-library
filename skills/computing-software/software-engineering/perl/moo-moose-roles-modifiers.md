---
id: computing-software.software-engineering.perl.moo-moose-roles-modifiers
name: moo-moose-roles-modifiers
category: computing-software
field: software-engineering
product: perl
tags: [perl, moo-role, moose-role, method-modifiers, before-after-around, requires, moo-moose-roles-modifiers]
level: advanced
status: docs-checked
description: "Compose behaviour with Moo::Role or Moose::Role (built on Role::Tiny), requires, and before/after/around modifiers from Class::Method::Modifiers."
sources: ["https://metacpan.org/pod/Moo::Role", "https://metacpan.org/pod/Moose::Role", "https://metacpan.org/pod/Class::Method::Modifiers", "https://metacpan.org/pod/Role::Tiny"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Roles and method modifiers

**Goal:** reusable behaviour without inheritance.

```perl
package Role::Logs;
use Moo::Role;                          # or Moose::Role
requires 'name';                        # consumer must implement
has log_level => (is => 'rw', default => 'info');
sub log { my ($s, $m) = @_; warn '[' . $s->name . '] ' . $m . "\n" }

package Service;
use Moo;
with 'Role::Logs';                      # several roles: with 'A', 'B'
sub name { 'svc' }
sub run { ... }
before run => sub { $_[0]->log('starting') };
after  run => sub { $_[0]->log('done') };
around run => sub { my ($orig, $self, @args) = @_; $self->$orig(@args) };
```

## Role composition (Role::Tiny, which Moo::Role builds on)
- If the class already defines a method, the role's version is not composed in: the class wins. A method merely inherited by the class is overridden by the role's method.
- A `requires`d method that is missing makes role application fail loudly.
- Several roles in one `with` statement whose methods clash raise an exception, unless the class provides that method. To resolve conflicts in favour of one role, use separate `with` statements (`with 'R1'; with 'R2';`). The docs say that for different conflicts resolved for different roles you should refactor.
- All subs created after importing the role module count as role methods. Moo::Role removes its own imports and anything imported before `use Moo::Role`; imports made after it are composed into consumers (the Moo::Role page shows `sha1_hex` leaking this way).
- `Moo::Role` adds `has` to Role::Tiny, so roles can declare attributes. Role::Tiny is the attribute-less subset of Moo::Role, itself a subset of Moose::Role.
- Introspection: `$class->does('Role')` (installed unless the class has `does`), `Role::Tiny::does_role($thing, 'Role')`, `Role::Tiny->is_role($pkg)`. Role::Tiny also overrides `DOES` unless an ancestor already provides it.
- Role::Tiny can apply roles to an object (it is reblessed) with `apply_roles_to_object`, and `create_class_with_roles` builds a class from a base plus roles.

## Moose::Role specifics
- `requires` and `excludes` (a role says it can never be combined with the named roles; not to be used lightly). Attribute accessors satisfy `requires`.
- Roles cannot use `extends`, `augment` or `inner`.
- Composition tries to be order-insensitive for conflicts and requirements, but method modifiers are order-sensitive: all before/around/after modifiers are included and applied in the order roles are used. Never assume ordering. There is no conflict between modifiers.
- Roles can be applied to an instance with `->meta->apply($instance)` (or `apply_all_roles`); this makes an anonymous subclass and reblesses, so `ref` may not return the original class name.
- `no Moose::Role` removes the exported keywords.

## Method modifiers (Class::Method::Modifiers; same semantics in Moo and Moose)
- `before` and `after` return values are ignored. They receive the same `@_` as the method; changing `$_[0]` or data inside a reference is visible to the original method ("a feature"). `after` sees changes the original made to `@_`; to avoid that, copy `@_` in `before`.
- `around` replaces the method and receives the original as first argument (`$orig`). It can pass different arguments, change the return value, or skip the original. Watch contextual return values of `$orig`.
- Several method names can be given as a list or arrayref. Multiple modifiers can live in one namespace without knowing about each other.
- Modifying a method that does not exist in the class hierarchy throws when the modifier is defined, so define or inherit the method first. `fresh` (CMM 2.00+, import it explicitly) installs a method but throws if the hierarchy already has one.
- Caveats: modifiers do not play well with `caller`; array lvalue methods are not fully supported.
- Role::Tiny roles that use modifiers need both Role::Tiny and Class::Method::Modifiers as dependencies (CMM is lazily loaded).

## Checked
Method: 2026-11-08 read the full plain-text POD of Moo::Role, Moose::Role, Class::Method::Modifiers (to the Acknowledgments) and Role::Tiny via the MetaCPAN API; added Role::Tiny as a source. Corrected v1: before/after can alter arguments in place; removed unsupported claims about stacking order, MooseX::Role::Parameterized and the "Failure modes" section. Did not read the Moose::Manual::Roles page.
