---
id: computing-software.software-engineering.perl.moo-attributes-has
name: moo-attributes-has
category: computing-software
field: software-engineering
product: perl
tags: [perl, moo, has-attribute, lazy-builder, required, metacpan-moo, moo-attributes-has, perl-moo-moose]
level: practitioner
status: docs-checked
description: "Declare Moo attributes with has: is, required, default, lazy and builder, predicate, clearer, handles, trigger, coerce, plus BUILDARGS/BUILD and import cleanup."
sources: ["https://metacpan.org/pod/Moo", "https://metacpan.org/pod/Moo::Role"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Moo classes and has attributes

**Goal:** concise classes with Moo, an XS-free, fast-starting subset of Moose.

```perl
package Person;
use Digest::MD5 qw(md5_hex);        # imports go BEFORE "use Moo"
use Moo;
use namespace::clean;               # scrubs earlier imports (and Moo's keywords) from the class
use Types::Standard qw(Int);        # Type::Tiny types; Moo has no type system of its own

has name   => (is => 'ro', required => 1);
has age    => (is => 'rw', isa => Int, default => sub { 0 });
has tags   => (is => 'ro', default => sub { [] });          # ref defaults must be wrapped in a sub
has id     => (is => 'lazy');                               # builder is _build_id
has emails => (is => 'rwp', predicate => 1, clearer => 1);  # has_emails, clear_emails, _set_emails
has parent => (is => 'ro', weak_ref => 1);                  # weaken circular references
has _http  => (is => 'ro', init_arg => undef, handles => [qw(get post)]);  # delegate methods
has [qw(a b)] => (is => 'ro');                              # same options for several attributes
sub _build_id { md5_hex($_[0]->name) }
1;
```

## has options (Moo POD)
- `is` (required): `ro` (reader only), `rw` (accessor), `rwp` (reader plus writer `_set_NAME`, for attributes written only inside the class), `lazy` (like `ro` but sets `lazy => 1` and `builder => "_build_NAME"`).
- `isa`: a coderef that dies on invalid values; its return value is discarded. Moo has no basic type system, so `isa => 'Num'` is not supported. For named types use Type::Tiny (`Types::Standard`).
- `coerce`: a coderef; Moo always runs it, and runs any `isa` check after the coercion. `isa` checks are meant for bug trapping, coercions are structural.
- `default`: coderef called with `$self`, or a plain scalar. Hash or array refs are an error (they would be shared by all objects), so return them from a coderef. Other attributes may not be populated yet when a default runs during `new()`.
- `builder`: method name called as `$self->$builder`; `builder => 1` means `_build_NAME`.
- `lazy`: build on first access; useful when the builder needs other attributes.
- `required`: the attribute must be passed to the constructor.
- `predicate` / `clearer`: method names, or `1` for `has_NAME` / `clear_NAME` (with a leading underscore on the attribute: `_has_NAME` / `_clear_NAME`). Clearing a lazy attribute regenerates it on next access; a non-lazy one becomes undef.
- `trigger`: called whenever the attribute is set, including from the constructor but not for defaults or built values; `trigger => 1` calls `_trigger_NAME`. Unlike Moose it does not receive the old value.
- `handles`: arrayref of method names, hashref (alias to method), or a role name.
- `reader`, `writer`: custom method names. `init_arg`: constructor key; `undef` means a passed value is ignored. `weak_ref`: weaken the stored reference.
- `has '+attr' => (...)` overrides an attribute from a parent class.

## Class behaviour
- `new` accepts a hash or hashref; override with `around BUILDARGS`. `BUILD` runs parent-to-child after construction (validation); `DEMOLISH` runs child-to-parent and Moo implements it with `DESTROY`, so do not define your own `DESTROY`.
- `extends` called twice replaces superclasses. `with` composes Moo::Role or Role::Tiny roles and errors on conflicting methods. `before`/`after`/`around` come from Class::Method::Modifiers.
- Moo::Role adds `has` to Role::Tiny. Declare imports before `use Moo::Role` and they are not composed into consumers.
- `use Moo` enables strict and warnings; the authors recommend `use strictures 2`.
- Moo does not clean up imports. Put imports first, then `use Moo`, then `use namespace::clean`; imports after `namespace::clean` become methods (for example `$r->has`). With namespace::autoclean use version 0.16 or newer.
- No built-in meta object: calling `->meta` methods other than `make_immutable` upgrades to real Moose. Loading Moose makes Moo classes and roles usable from Moose code. Moo makes its constructor inlined automatically on first `new`.
- Not supported versus Moose: `initializer`, `super`/`override`/`inner`/`augment`, `lazy_build`, `auto_deref`.
- If Class::XSAccessor is available, simple accessors use it and then reject calls with the wrong number of arguments.

## Self-check
- [ ] `Person->new` without `name` dies with a missing-required-argument error.
- [ ] No `has`, `around`, or imported helper shows up as a method on instances.

## Checked
Method: 2026-11-08 read the full Moo and Moo::Role POD (MetaCPAN API plain-text export). Removed claims the pages do not state: MooX::StrictConstructor for unknown constructor arguments, "installs Class::Method::Modifiers and Role::Tiny", and the "do not name attributes like methods" rule. The `isa => ArrayRef[Str]` example was dropped and the original self-check error text was not confirmed by the pages, so it is now stated generally.
