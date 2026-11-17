---
id: computing-software.software-engineering.prolog.iso-core-builtins
name: iso-core-builtins
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, iso-core-builtins, portable-prolog]
level: advanced
status: draft
description: "Write portable ISO Prolog: ISO builtins (atom_chars, sub_atom, findall, catch), avoiding SWI extensions, and conformance testing."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ISO core and portability
ISO/IEC 13211-1 specifies syntax, builtins (`functor/3`, `arg/3`, `=../2`, `copy_term/2`, `atom_*`, `findall/3`, `bagof/3`, `setof/3`, `catch/3`, `throw/1`, streams), arithmetic and error terms.
Portable subset habits:
- Use code/char lists, not strings or dicts, in shared code.
- Avoid `format/2`, `forall/2` (check target systems), modules, tabling.
- Use `:- set_prolog_flag(double_quotes, codes).` in portable sources.
- Check: Ulrich Neumerkel's ISO conformity table (www.complang.tuwien.ac.at/ulrich/iso-prolog/conformity_testing) for a system's deviations.
Module standard: ISO/IEC 13211-2.
## Gotchas
- ISO leaves `forall/2`, `format/2`, `between/3`, `succ/2` out (de facto but non-ISO).
- Standard purchase required; use the conformity page and system manuals for details.
## Self-check
List which of your predicates use non-ISO builtins using `predicate_property(P, iso)`.
