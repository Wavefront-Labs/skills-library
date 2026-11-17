---
id: computing-software.software-engineering.refactoring.codemods-and-large-scale-automated-refactors
name: codemods-and-large-scale-automated-refactors
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, codemod, jscodeshift, ast-grep, openrewrite, ast-based-refactoring, large-scale-change, api-migration, grit, semgrep-autofix, automated-refactoring]
level: advanced
status: draft
description: "Run a safe org-wide codemod with an AST-based tool (jscodeshift, ast-grep, OpenRewrite): staged rollout, idempotency, and verifying the transform didn't just move bugs."
sources: ["jscodeshift README and docs", "ast-grep docs", "OpenRewrite docs (Java/multi-language recipes)", "personal experience running codebase-wide find/replace migrations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Codemods — rewriting hundreds of call sites without hand-editing any of them

**Goal:** migrate an API, rename a widely-used symbol, or enforce a new pattern
across a large codebase mechanically and reversibly, instead of a multi-day manual
find-and-replace that inevitably misses edge cases or breaks formatting.

## 1. Regex find/replace is not a codemod
`sed`/regex replace doesn't understand code structure — it matches text, so it
breaks on a renamed variable that happens to match the pattern in a comment or string
literal, or misses the target when it's spread across multiple lines or aliased via
an import rename. A real codemod operates on the **AST** (abstract syntax tree), so
it only matches actual code constructs (a specific function call, a specific import)
and can be made precise regardless of formatting.

## 2. Pick the tool for the language and transform's complexity
- **jscodeshift** (JS/TS, built on recast/babel) — write a transform function
  operating on the parsed AST; recast preserves original formatting/comments for
  untouched code, which matters for a reviewable diff.
- **ast-grep** — pattern-based (write the "before" and "after" as code snippets with
  meta-variables, not a full AST-manipulation script) across many languages; much
  faster to write for simple structural replacements (`foo($ARG)` → `bar($ARG)`)
  than hand-rolling an AST transform.
- **OpenRewrite** — Java/JVM-focused, ships many pre-built "recipes" for common
  framework migrations (Spring Boot version bumps, JUnit 4→5) — check if your
  migration is already a published recipe before writing one.
- **Comby, Semgrep (with --autofix)** — similar structural-pattern-match-and-replace
  approach, useful when the transform is simple enough to express as a pattern
  without full AST scripting.

## 3. Write the transform against real, varied examples first
Before running org-wide, collect 10-20 real call sites of the pattern you're
changing, including the ugly ones (destructured arguments, spread, an aliased
import, a call inside a ternary) — a transform tested only against the clean,
textbook case will produce malformed output on the 5% of call sites that don't match
your mental model, and that 5% across a large codebase is still dozens of broken files.

## 4. Stage the rollout; never run org-wide blind
1. **Dry run** (`--dry`/print mode most tools support) on the whole codebase first —
   review the diff stat (files touched, lines changed) for a sanity check before
   writing anything.
2. **Apply to one directory/package**, open a real PR, get it reviewed and merged —
   this surfaces transform bugs on a bounded blast radius.
3. **Apply to the rest in batches** sized for reviewable PRs (hundreds, not
   thousands, of changed lines per PR) — a 50,000-line single PR gets rubber-stamped,
   not actually reviewed, which defeats the purpose of having a human check the
   mechanical change.
4. Keep the codemod script itself in version control (even if deleted after the
   migration completes) so a mistake found later can be traced to exactly what ran.

## 5. Idempotency and partial-application safety
A codemod run twice (because the branch was rebased, or run accidentally again)
should either be a no-op on already-migrated code or explicitly guard against
double-transforming — a naive text-based find/replace run twice can corrupt output
(wrapping an already-wrapped call a second time). AST-based transforms should check
the current node shape before transforming, not blindly assume the "before" pattern
still matches.

## 6. Verification is not "it compiled"
Compiling confirms syntax validity, not semantic preservation. For a pure
refactor (same behavior, different code shape): run the full test suite, and where
feasible, diff the compiled/transpiled *output* bytecode or behavior for a sample of
changed files against the pre-transform version. For an actual API migration (not
behavior-preserving by definition — the new API might have different edge-case
semantics), rely on the test suite plus explicit manual review of behavior-sensitive
call sites (error handling, edge cases) that the codemod touched.

## Gotchas
- A codemod that touches generated files (protobuf stubs, build output
  accidentally checked in) corrupts them on the next generation — exclude generated
  paths explicitly, don't rely on `.gitignore` matching what the codemod tool scans.
- Comment-embedded code (JSDoc examples, markdown code blocks in docs) referencing
  the old API won't be caught by an AST tool scanning only real source — grep
  separately for documentation that also needs updating.
- Formatting-preserving tools (recast) can still shift unrelated whitespace/quote
  style on touched lines if the parser's printer doesn't perfectly round-trip —
  review the diff for unexpected unrelated-looking changes, don't assume "AST-based"
  means "zero formatting noise."

## Verify
- [ ] The transform was tested against a deliberately varied sample (10-20 real,
      messy call sites) before any org-wide run.
- [ ] A dry-run diff was reviewed for unexpected scope (files touched that shouldn't
      be) before the first real apply.
- [ ] Rollout happened in reviewable-sized batches with the first batch's PR actually
      reviewed, not just the last batch rubber-stamped.
- [ ] Full test suite passes after the transform; for an actual semantic API change,
      behavior-sensitive call sites were manually checked, not just compiled.

Related: computing-software.software-engineering.refactoring.extract-and-decompose-large-classes,
computing-software.software-engineering.refactoring.characterisation-tests-and-safe-refactoring
