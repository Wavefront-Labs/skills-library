---
id: computing-software.firmware-embedded-development.bare-metal-programming.misra-checking-with-cppcheck
name: misra-checking-with-cppcheck
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [misra-static-analysis, cppcheck, misra-addon, misra-c, static-analysis, compile-commands, ci-gate, suppressions, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use the cppcheck misra.py addon for MISRA C:2012 checks: the rule-texts file, suppress-rules, verify-rule-texts, and why MISRA text is not shipped with the addon."
sources:
  - https://github.com/danmar/cppcheck/blob/main/addons/misra.py
  - https://www.misra.org.uk/misra-c/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MISRA static analysis with cppcheck

**Goal:** an automated MISRA C:2012 check that reports real findings on your code, with rule
texts you are licensed to use, and a gate that blocks regressions.

## What the addon is
`addons/misra.py` in the cppcheck repository implements MISRA C 2012 checks, including
amendments 1 and 2 (its header counts 143 rules). It is open source, and MISRA does not allow
the rule texts to be distributed openly, so the addon ships without them.

## Run it
The addon works on cppcheck dump files:
```sh
cppcheck --dump main.c
python misra.py --rule-texts=<path-to-rule-texts> main.c.dump
```
cppcheck also loads addons itself through its `--addon=` option; see the cppcheck manual for the
project, platform and suppression options of the main program, which this skill does not restate.

## Addon options (from `misra.py --help`)
- `--rule-texts=<file>`: your rule-text file. Without it, findings print as "misra violation
  (use --rule-texts=<file> to get proper output)" and the script reports an error asking for the file.
- `--verify-rule-texts`: check that all supported rules have text in the given file, then exit.
- `--suppress-rules 15.1,11.3,20.13`: comma-separated rules to suppress.
- `--show-suppressed-rules`: print the suppression list.
- `-P` / `--file-prefix`: prefix to strip when matching file-based rule suppressions.
- `--no-summary`: hide the summary of violations.
- `--severity`: a custom severity string, for example `error` or `warning`.

## Rule-texts file
Copy it from your licensed MISRA PDF. Either run `pdftotext MISRA_C_2012.pdf MISRA_C_2012.txt`
or paste the "Appendix A Summary of guidelines" chapter. The format is arbitrary text, then the
line `Appendix A Summary of guidelines`, then for each guideline a header such as
`Rule 1.1 Required` followed by its text lines. Buy the standard from misra.org.uk; do not commit
the text to a public repository.

## CI pattern
- Run `--verify-rule-texts` once so a missing guideline text is noticed early.
- Baseline legacy code: save the first findings and fail only on new ones.
- Pin the cppcheck version, because results change between versions.

## Coverage limits
Check which guidelines the addon covers against its source before claiming compliance. A
formal compliance claim needs a documented guideline enforcement plan that states which tool
covers which guideline; use the MISRA documents for that process.

## Verify
- [ ] Findings print the rule number and text (rule-texts file loaded).
- [ ] `--verify-rule-texts` reports no missing texts.

## Checked
Date: 2026-10-31.
Confirmed in `addons/misra.py` (cppcheck main branch): purpose and rule count, the rule-texts
limitation and file format, `--rule-texts`, `--verify-rule-texts`, `--suppress-rules`,
`--show-suppressed-rules`, `-P/--file-prefix`, `--no-summary`, `--severity`, the dump-file workflow.
Removed as unconfirmed (the cppcheck manual is a PDF that does not fetch): `--project`, `--platform`,
`--suppressions-list`, `--inline-suppr`, `--error-exitcode`, `-j` behaviour, `--check-config`,
`misra-c2012-N.N` suppression ids, `misra.json` layout, the commercial tool list and the Rule 1.3 and Dir 4.1 claims.
Method: documentation only; no commands were run.
