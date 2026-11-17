---
id: computing-software.software-engineering.perl.perlstyle-conventions
name: perlstyle-conventions
category: computing-software
field: software-engineering
product: perl
tags: [perl, perlstyle, coding-style, naming-conventions, modern-perl, perl-best-practices, perlstyle-conventions, perl-style-lint]
level: practitioner
status: docs-checked
description: "Apply perlstyle and widely used Perl conventions: layout, naming, idioms to prefer and avoid."
sources: ["https://perldoc.perl.org/perlstyle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# perlstyle conventions and idioms

**Goal:** consistent, readable Perl code.

## What perlstyle says
- Use `strict` and `warnings` in all your code or know the reason why not. Turn them off for limited portions with
  `no warnings` or `no strict`; do not use `-w` or `$^W` for that, since they affect code you did not write. A concise
  way is `use v5.36;` (version 5.36 or above enables strict and warnings plus other named features).
- Layout: the one thing stressed is that the closing curly of a multi-line BLOCK lines up with the keyword that
  started it. Weaker preferences: 4-column indent; opening curly on the same line as the keyword if possible;
  space before the opening curly of a multi-line BLOCK; one-line BLOCKs may sit on one line; no space before the
  semicolon; space around most operators and around a complex subscript; blank lines between chunks that do different
  things; uncuddled `else`; no space between a function name and its opening parenthesis; space after each comma;
  long lines broken after an operator (except `and` and `or`); line up corresponding items vertically.
- Pick the most readable of the ways Perl offers: `open(my $fh, '<', $foo) || die "Can't open $foo: $!";` beats the
  statement-modifier form that hides the main point, and `print "..." if $verbose;` beats `$verbose && print ...`.
- Do not rely on default arguments or omitted parentheses just because you can; when in doubt, parenthesize.
- Use `last` to exit a loop in the middle rather than contortions, and do not be afraid of loop labels.
- Avoid `grep()`, `map()` or backticks in a void context; use `foreach` or `system()`.
- For portability, test uncertain features in an `eval`, or check `$]`, or interrogate the `Config` module.
- Always check return codes of system calls; error messages go to STDERR, name the program, the failed call and
  arguments, and include `$!`, for example `opendir(my $dh, $dir) or die "can't opendir $dir: $!";`.
- Use here-documents instead of repeated `print`; use `/x` or `/xx` for hairy regexes and do not use slash as the
  delimiter when the pattern has slashes or backslashes.
- Use `and`/`or` to avoid parenthesizing list operators and to reduce `&&`/`||`; call subs like functions or list
  operators to avoid excess ampersands.

## Naming
- Choose mnemonic identifiers. Short names like `$gotit` are fine; separate words in longer ones with underscores
  (`$var_names_like_this`), which also fits `VAR_NAMES_LIKE_THIS`.
- Letter case can show scope: `$ALL_CAPS_HERE` for constants only, `$Some_Caps_Here` for package-wide globals,
  `$no_caps_here` for `my` or `local` variables.
- Function and method names work best all lowercase (`$obj->as_string()`). A leading underscore marks something not to
  be used outside its package.
- Lowercase module names are informally reserved for pragmas (`integer`, `strict`); other modules start with a capital
  and use mixed case, probably without underscores.

## Documentation (Pod)
`C<>` for function, variable and module names (function names read better with parentheses), `B<>` for command
names, `F<>` or `C<>` for file names (`C<>` can render paths better). Be consistent.

## Rules
- Follow the project's linter config over personal taste.
- Consider reusability: generalise code, and make it run cleanly under `strict` and `warnings`.

## Self-check
- [ ] New code uses `strict` and `warnings` (or `use v5.36;`), checks system-call return codes, and has consistent
      brace alignment.

## Checked
Confirmed 2026-11-08 against perlstyle on perldoc.perl.org (read in full). Removed everything perlstyle does not say:
the "unless-free" and "avoid unless/else" rules, hash key quoting, `=>` pairs, the constant and `is_`/`has_` naming
rules, the idioms code block, the "Avoid" list (indirect object syntax, bareword filehandles, two-arg `open`,
prototypes, and so on), the perltidy and perlcritic advice, and the book recommendations. perltrap and perlmodstyle
were dropped from sources because no claim relies on them.
Method: docs-only read of cited pages, 2026-11-08
