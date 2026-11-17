---
id: computing-software.software-engineering.perl.string-eval-safe-compartments
name: string-eval-safe-compartments
category: computing-software
field: software-engineering
product: perl
tags: [perl, string-eval, safe-module, eval-injection, do-file, code-injection, string-eval-safe-compartments]
level: advanced
status: docs-checked
description: "Know the risks of eval STRING and do FILE, how Safe compartments work, and why Safe is not an effective sandbox."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perlsec", "https://perldoc.perl.org/Safe"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String eval, do FILE and the Safe module

**Goal:** avoid running attacker-controlled Perl, and use dynamic code carefully.

```perl
my $v = eval "$user_input";        # arbitrary code execution: never with untrusted input
my $cfg = do $file;                # compiles and runs the file; see failure handling below
my $obj = eval { $class->new };    # eval BLOCK, no string compilation
```

## do FILE (perlfunc)
- If `do` can read the file but cannot compile it, it returns undef and sets `$@`. If it cannot read the file, it
  returns undef and sets `$!`. Always check `$@` first, as compilation could fail in a way that also sets `$!`.
- If the file compiles, `do` returns the value of the last expression evaluated.
- `do 'file'` searches `@INC`. Since perl 5.26.0 `.` is not in `@INC` by default, so a bare relative name no longer
  finds a file in the current directory; give an explicit path such as `./file`.
- A failed `eval '$answer ='` sets `$@` (perlfunc example), so check `$@` after string evals.

## Safe (Safe module docs)
```perl
use Safe;
my $cpt = Safe->new;
$cpt->permit_only(qw(:default));
my $r = $cpt->reval($code);
die $@ if $@;
```
- A compartment gets a new namespace: its root becomes a different package (default `Safe::Root0`, incremented per
  compartment) that appears as `main::` inside, and code cannot reach variables outside it, even by run-time glob
  lookups. Only `$_` and `@_` (and similar underscore items) are shared by default.
- Each compartment has an operator mask, default the `:default` optag. Code containing a masked operator fails to
  compile and is not run; the error reads "'%s' trapped by operation mask...".
- Methods: `permit`, `permit_only`, `deny`, `deny_only`, `share`, `share_from`, `reval`. `trap` and `untrap` are
  synonyms for `deny` and `permit`.
- Controlled access to risky operations: write a wrapper sub outside the compartment, vet its arguments, and
  `$cpt->share('&wrapper')`, because the mask only applies at compile time.
- WARNING from the module itself: Safe "does not implement an effective sandbox for evaluating untrusted code with the
  perl interpreter". Interpreter bugs that bypass Safe are not treated as vulnerabilities, there is no warranty, and
  "If in any doubt do not use it."

## Rules
- Prefer data formats and dispatch tables over evaluating strings; do not `eval` or `do` content from untrusted
  sources.
- Do not treat Safe as a security boundary for hostile code.
- Check `$@` after every string eval and `do FILE`.

## Self-check
- [ ] Every remaining `eval STRING` or `do FILE` handles only trusted input and has its `$@` checked.

## Checked
Confirmed 2026-11-08 against the Safe page (namespace, operator mask, methods, sharing, WARNING section) and perlfunc
`do EXPR` (return values, `$@` before `$!`, `.` absent from `@INC` since 5.26.0) and the `eval '$answer ='` example.
Removed: the module-recommendation lists (JSON::PP, YAML::PP, Math::Expression and so on), the Template Toolkit
`EVAL_PERL` note, Perl::Critic advice, the claim that Safe has no CPU or memory limits, the loop-compile performance
claim and the grep self-check, none of which the cited pages state.
Method: docs-only read of cited pages, 2026-11-08
