---
id: computing-software.software-engineering.prolog.listing-portray-clause
name: listing-portray-clause
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, listing-portray-clause, check-0]
level: practitioner
status: docs-checked
description: "Inspect code with listing/1,2 and portray_clause, run check/0 and use the protect_static_code flag in SWI-Prolog."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/listing.pl
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/check.pl
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/overview.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listing code
```prolog
?- listing(foo/2).            % Name/Arity; also a Head term or a clause reference
?- listing(foo).
?- listing(foo/2, [variable_names(source)]).
?- portray_clause((a(X,Y) :- b(X), c(Y, _))).   % variables print as A, B; singletons as _
?- check.                     % static checks
?- predicate_property(foo(_,_), number_of_clauses(N)).
```
- `listing/1` also prints declarations such as `dynamic` and `multifile`. `listing/2` options include `variable_names`, `source`, `thread` and `module`.
- `portray_clause/1,2,3` writes a clause so it can be read back; options include `indent`, `variable_names` and `module`.
- `check/0` runs `list_undefined`, `list_trivial_fails`, `list_format_errors`, `list_redefined`, `list_void_declarations`, `list_autoload` and `check_predicate_options`.
- `apropos/1` and `help/1` search the manual.
## Gotchas
- If the flag `protect_static_code` is `true`, `clause/2` and `listing` do not work on static code; the default is `false` and once set to `true` it cannot be reset.
## Self-check
Assert `foo(1)`, call `listing(foo/1)` and compare with the `dynamic` declaration printed above the clause.

## Checked

2026-11-03. SWI-Prolog manual and library(listing) / library(check) documentation and source (listing.pl, check.pl, overview.plx): listing/1,2 arguments and options, portray_clause/1,2,3, check/0 contents, predicate_property number_of_clauses, flag protect_static_code. Removed: the prolog_xref cross-reference mention and the "can be reloaded" claim.

Method: documentation only; no commands were run.
