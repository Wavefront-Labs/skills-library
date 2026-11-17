---
id: computing-software.software-engineering.perl.typeglobs-symbol-table-manipulation
name: typeglobs-symbol-table-manipulation
category: computing-software
field: software-engineering
product: perl
tags: [perl, typeglob, glob-assignment, sub-installation, local-glob, package-stash, typeglobs-symbol-table-manipulation]
level: sme
status: docs-checked
description: "Use typeglob assignment to install or alias subs, localise globs, and generate accessors; know the documented limits."
sources: ["https://perldoc.perl.org/perlmod", "https://perldoc.perl.org/perldata", "https://perldoc.perl.org/perlref", "https://perldoc.perl.org/perlsub", "https://perldoc.perl.org/Sub::Util"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typeglobs and installing subs at run time

**Goal:** safe metaprogramming with symbol tables.

```perl
no strict 'refs';
*{"${class}::$name"} = sub { ... };            # install a method (symbolic reference)
*{"main::alias"} = \&My::Util::f;               # alias only the sub
*PI = \3.14159;                                 # alias a scalar to a constant: $PI cannot be altered
*dick = *richard;                               # alias the whole glob: $, @, %, &, handles
{ local *FH; ... }                              # localise $FH, @FH, %FH, &FH and the handle
my $code = *{"main::foo"}{CODE};                # glob slot: SCALAR, ARRAY, HASH, CODE, IO, GLOB, FORMAT
for my $field (qw(name age)) { *{"Person::$field"} = sub { $_[0]{$field} } }   # accessor generator
```

## Rules (all from perlmod, perlref, perlsub, Sub::Util)
- Assigning a typeglob aliases everything under that name. To alias only one thing assign a reference: `*dick = \$richard` makes `$dick` and `$richard` the same scalar but leaves `@dick` and `@richard` separate.
- `*foo = *bar` makes the globs synonymous so the alias can be localised; `*foo = \$bar` does not, and a `local $bar` later is not seen through `$foo`.
- `*x = \$y` works only for package (dynamic) variables, not `my` variables. Only package variables are visible to symbolic references, and `no strict 'refs'` is needed to use them; keep that scope small.
- `sub Some_package::foo { ... }` is shorthand for `BEGIN { *Some_package::foo = sub { ... } }`; the body is compiled in the current package, not `Some_package`.
- Exporter uses glob aliasing; an exported `$FOO` (via `@EXPORT = qw($FOO)`) cannot be localised, but `*FOO` can.
- Install subs in `BEGIN` when callers use them as barewords without parentheses: `foo;` acts like `foo()` only if the sub is predeclared or imported.
- Redefining a sub produces a `Subroutine ... redefined` warning; keep the original with `my $orig = \&Foo::bar;` before replacing it.
- `local *name = \&other;` overrides only until the enclosing block exits; this is useful in tests.
- `*foo{NAME}` and `*foo{PACKAGE}` give the name and package of the glob itself as strings; `*foo{THING}` returns `undef` for a slot not yet used (except SCALAR).
- Creating symbol-table entries directly, or modifying entries that are not already typeglobs, has undefined results that can change between Perl releases. Do not rely on the `%Pkg::` stash layout.
- `Sub::Util::set_subname($name, $code)` (core) names an anonymous sub so stack traces show it instead of `__ANON__`; it does not install the sub. `Sub::Util::subname($code)` returns the current name.

## Self-check
- [ ] After generating accessors with `set_subname`, `Sub::Util::subname($code)` returns the fully qualified name you gave it.

## Checked

Confirmed on perlmod, perlref, perlsub and Sub::Util: glob versus reference aliasing, `local *name`, constant scalar via `*PI`, `sub Pkg::foo` shorthand, Exporter localisation, symbolic refs only reach package variables, `*foo{THING}` slots, predeclared barewords, redefinition warning, stash-layout caveat, set_subname and subname. Removed (not on readable official pages): the CPAN helper list (Package::Stash, Sub::Install, namespace::clean and similar), `Symbol::gensym`, `B::svref_2object`, `no warnings 'redefine'`, and the in-memory STDOUT redirect example.

Method: docs-only read of cited pages, 2026-11-08
