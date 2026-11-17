---
id: computing-software.software-engineering.perl.exporter-import-conventions
name: exporter-import-conventions
category: computing-software
field: software-engineering
product: perl
tags: [perl, exporter, export-ok, export-tags, import-conventions, perlmod, exporter-import-conventions]
level: practitioner
status: docs-checked
description: "Export functions from a module with Exporter using @EXPORT_OK and %EXPORT_TAGS, and know when not to export by default."
sources: ["https://perldoc.perl.org/perlmod", "https://perldoc.perl.org/Exporter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporter, @EXPORT_OK and import conventions

**Goal:** a module interface that does not pollute callers.

```perl
package My::Util;
use strict; use warnings;
use Exporter 'import';                       # import only, no inheritance from Exporter
our $VERSION   = '1.09';                     # at least two decimal places
our @EXPORT_OK = qw(trim slurp);
our %EXPORT_TAGS = (all => \@EXPORT_OK, io => [qw(slurp)]);
sub trim  { my $s = shift; $s =~ s/^\s+|\s+$//g; $s }
sub slurp { ... }
1;
```
Caller:
```perl
use My::Util qw(trim);          # explicit list
use My::Util qw(:all);          # tag
use My::Util qw(:all !slurp);   # a leading ! deletes matching names from the list so far
```

## Conventions (from the Exporter documentation)
- Prefer `@EXPORT_OK` (opt-in) over `@EXPORT`: "Exports pollute the namespace of the module user"; avoid short or common symbol names to reduce name clashes. "Do not export anything else by default without a good reason!"
- If the module is object oriented, export nothing; do not export method names. If it is a collection of functions, `@EXPORT_OK` anything, and use `@EXPORT` with caution.
- Do not export variable names, even though Exporter allows it.
- Names in `%EXPORT_TAGS` must also appear in `@EXPORT` or `@EXPORT_OK`. A `:all` tag is useful when several categories exist, and `Exporter::export_tags` / `export_ok_tags` add tagged sets to the arrays.
- A leading `!` in the first specification is treated as if preceded by `:DEFAULT` (all names in `@EXPORT`); to import extras on top of the defaults you must still include `:DEFAULT` explicitly.
- Version check: importing a number calls `$module_name->VERSION($value)`, so `use My::Util 1.09 qw(trim);` checks the module version. Because `UNIVERSAL::VERSION` treats the version as a number, 1.10 is lower than 1.9; use at least two decimal places (for example 1.09).
- Names that cannot be exported on some platform can be listed in `@EXPORT_FAIL`, with an `export_fail` method for better messages or lazy checks.
- Anything not exported is still reachable as `YourModule::item_name`; a leading underscore informally marks internal names.

## Self-check
- [ ] A caller importing a name not in `@EXPORT_OK` or `%EXPORT_TAGS` fails at `use` time; `perl -MMy::Util=trim -e 'print trim(" a ")'` works.

## Checked
Read the Exporter documentation (Good Practices, specifications and tags, version checking, @EXPORT_FAIL) and perlmod. Fixed the exclusion example (`!slurp :all` would re-add the deleted name). Removed, because the cited pages do not state them: `Exporter::Tiny`/`Sub::Exporter`/`import::into` advice, the exact "is not exported by" error text, the "Subroutine redefined" warning, the alias claim for exported variables, and the OO-class `sub import` claim.
Method: docs-only read of cited pages, 2026-11-08
