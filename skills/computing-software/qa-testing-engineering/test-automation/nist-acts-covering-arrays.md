---
id: computing-software.qa-testing-engineering.test-automation.nist-acts-covering-arrays
name: nist-acts-covering-arrays
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [acts-tool, covering-arrays, combinatorial-testing, pairwise-testing, t-way-testing]
level: practitioner
status: docs-checked
description: "Generate t-way covering arrays with NIST ACTS: input file sections, constraints, mixed strength, command-line degree of interaction, and output formats."
sources:
  - https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software
  - https://csrc.nist.gov/pubs/sp/800/142/final
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-142.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NIST ACTS covering array generation

**Goal:** produce compact t-way test sets with constraints, using NIST's ACTS tool. The NIST project page says it is free, public domain, and obtained by emailing a request to NIST (first name, last name, organisation, country); a download link is sent. The page names ACTS 3.3 as the latest version.

## What ACTS does (SP 800-142, Appendix C)
- Compact covering arrays for 2-way through 6-way combinations.
- Constraints that make some values depend on others.
- Mixed-level arrays: different strength for subsets of parameters (for example 2-way for one subset and 4-way for another).
- Output exported as human-readable, numeric or spreadsheet formats (the text also mentions comma-separated values).
- Either "don't care" or randomised values for tests whose combinations are already covered.
- A command-line version and a GUI; a comprehensive user manual ships with the download.
- NIST also lists a coverage measurement tool (coverage of an existing test set) and a sequence covering array generator.

## Input file
SP 800-142 shows a text file with the tags `[System]`, `[Parameter]`, `[Relation]`, `[Constraint]` and `[Misc]`. Most tags are optional; `[Parameter]` is essential, one per line as `<parameter name> (<type>): <values>` with values comma-separated.
```text
[System]

[Parameter]
OS (enum): XP,OS_X,RHL
Browser (enum): IE, Firefox
Protocol (enum): IPv4,IPv6
CPU (enum): Intel,AMD
DBMS (enum): MySQL,Sybase,Oracle

[Relation]

[Constraint]

[Misc]
```
Constraint example from the publication: `(OS != "XP" => Browser = "Firefox")` ensures an invalid combination is not generated. Do not delete rows by hand: that loses other combinations that still need coverage. A constraint can reduce the number of tests, but not always.

## Run from the command line
The publication (2010) gives:
```bash
java -Ddoi=2 -jar acts_cmd.jar ActsConsoleManager in.txt out.txt
```
`-Ddoi` sets the degree of interaction (2-way, 3-way, and so on). The publication says a variety of other options exist but only documents `doi`; the jar and class names may differ in current releases, so use the user manual from your download for other options.

## Workflow
1. Partition each parameter into a few representative values; continuous values must be discretised.
2. Encode real constraints (combinations that cannot exist).
3. Generate at t=2, review the size, then raise strength.
4. Import the output into a parametrised test and keep the input file under version control.

## Why t greater than 2
NIST states the interaction rule: most failures are induced by single-factor faults or by the interaction of two factors, with progressively fewer failures from interactions among three or more. The publication's data (error detection rates for interaction strengths 1 to 6) suggest pairwise is not sufficient and that 4-way to 6-way testing may give reasonably high assurance. The project page reports failures triggered by interactions of only 1 to 6 variables.

## Gotchas
- Over-constraining hides valid combinations; review each constraint with the domain owner.
- ACTS treats parameter values as listed; choose values yourself (partitioning is not done by the tool).

## Verify
Every generated row satisfies the constraints, and the coverage measurement tool confirms t-way coverage of the suite for the chosen strength.

## Checked
2026-11-09: checked against the NIST ACTS project page (read in full), the SP 800-142 record, and the SP 800-142 PDF (input file format, the doi example, constraints section 3.3.1, Appendix C, the interaction rule). Removed because neither the pages nor the publication state them: `-Dalgo`, `-Dchandler`, `-Doutput` values, `mode=extend`/`scratch`, `[Test Set]`, `check` mode, the GUI coverage graphs, the `[Relation]` line syntax, `int` and `boolean` parameter types, the deterministic-algorithm claim, and "Java" as the implementation language (the `java` command line implies it, but the pages do not say so).

Method: documentation only; no commands were run.
