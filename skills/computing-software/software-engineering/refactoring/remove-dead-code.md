---
id: computing-software.software-engineering.refactoring.remove-dead-code
name: remove-dead-code
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, moving-features, remove-dead-code, dead-code-removal, unused-code, static-analysis, fowler-catalog]
level: practitioner
status: docs-checked
description: "Find and remove dead code with an IDE or analysers (vulture for Python, knip for JS/TS), allowing for dynamic use, and delete rather than comment out."
sources:
  - https://refactoring.guru/smells/dead-code
  - https://github.com/jendrikseipp/vulture
  - https://knip.dev/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remove Dead Code

**Rule:** delete unused code; do not comment it out. Version control remembers it.

## What counts
A variable, parameter, field, method or class that is no longer used, usually because it is
obsolete; also an unreachable branch of a complex conditional.

## Finding candidates
- The quickest way is a good IDE.
- Python: Vulture finds unused code. Run it on both the library and its test suite to also find untested code.
- JavaScript/TypeScript: Knip finds unused dependencies, exports and files.
- Other languages: use the compiler or analyser of your stack and treat its output as candidates.

## Static tools miss dynamic use
Vulture's own docs warn that, because of Python's dynamic nature, static analysers are likely
to miss some dead code and that code only called implicitly may be reported as unused. The same
applies to any language: before deleting, search all repos for the name, and consider reflection,
dependency injection by name, string dispatch, plugins and templates.

## Mechanics
1. Confirm the code is unused (tool output plus a search; watch for dynamic or public use).
2. Delete the unused code and unneeded files.
3. If a whole class is unneeded, Inline Class or Collapse Hierarchy applies when a subclass or superclass is used; for unneeded parameters use Remove Parameter.
4. Rerun the analysis: deletions can expose more unused code. Run the full build and tests.
5. Commit the removal separately with a message saying what was removed and why it was dead.

## Verify
- [ ] Analyser reports no new unused items after the deletion cascade.
- [ ] Unused dependencies removed from the manifest too.

## Checked
2026-11-01. Confirmed against the Refactoring Guru "Dead Code" smell page (definition, IDE, delete, Inline Class, Collapse Hierarchy, Remove Parameter), the Vulture README (purpose, test-suite tip, dynamic-language caveat) and the Knip home page (unused dependencies, exports and files).
Removed: the per-language tool table with command lines and flags, ruff and ProGuard references, staticcheck check number, runtime tombstone advice, and the git-history search command, because no page read states them.
Method: documentation only; no commands were run.
