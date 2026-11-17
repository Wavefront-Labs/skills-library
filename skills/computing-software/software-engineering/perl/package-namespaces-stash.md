---
id: computing-software.software-engineering.perl.package-namespaces-stash
name: package-namespaces-stash
category: computing-software
field: software-engineering
product: perl
tags: [perl, package, namespace, symbol-table, stash, perlmod, package-namespaces-stash, perl-modules]
level: practitioner
status: docs-checked
description: "Declare packages (including block syntax and versions), reach package variables, and inspect a symbol table."
sources: ["https://perldoc.perl.org/perlmod"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packages, namespaces and symbol tables

**Goal:** understand packages as namespaces.

```perl
package My::Util 1.02;          # sets $My::Util::VERSION
package My::Other { ... }       # block form: scope ends at the brace
our @EXPORT_OK = qw(f);         # package variable
$My::Util::count = 0;           # fully qualified
main::helper();  ::helper();    # main is the default package
__PACKAGE__->method;            # current package name as string
```

## Symbol table inspection
```perl
no strict 'refs';
for my $name (sort keys %{"My::Util::"}) { print "$name\n" }    # stash entries
print defined &{"My::Util::f"} ? "has f" : "no f";
*{"My::Util::alias"} = \&My::Util::f;                          # install an alias
```

## Rules
- A package does not imply a file; a file may contain several packages.
- `package` statements are lexically scoped: `package Foo;` lasts until the next `package` or end of the enclosing block/file.
- `::` separates package names; the old `'` separator is controlled by the `apostrophe_as_package_separator` feature (off in the 5.42 bundle onward), so use `::`.
- `our` creates a lexical alias to the package variable in the current package.
- `__PACKAGE__->can('f')` finds subs defined in the current package.
- Special packages: `main`, `CORE`, `CORE::GLOBAL` (overrides built-ins globally; use sparingly), `UNIVERSAL`.

## Failure modes
- Subs defined after `package Other;` land in `Other`, not the file's first package.
- Name clashes when importing functions with the same name from two modules.

## Self-check
- [ ] `perl -e 'package A; sub f{1} package main; print exists $A::{f} ? 1 : 0'` prints `1`.

## Checked
2026-11-03: confirmed against perlfunc package (NAMESPACE, VERSION and BLOCK forms, scope of a package declaration, __PACKAGE__, our), perlmod (symbol tables, packages, BEGIN/END, nested names) and the feature documentation (apostrophe_as_package_separator). Removed: version numbers for the VERSION and BLOCK syntax, Package::Stash, Sub::Util, Class::Inspector, the one-package-per-file convention, the underscore privacy claim, and the keys %A:: self-check output.
Method: documentation only; no commands were run.
