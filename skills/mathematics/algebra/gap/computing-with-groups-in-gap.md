---
id: mathematics.algebra.gap.computing-with-groups-in-gap
name: computing-with-groups-in-gap
category: mathematics
field: algebra
product: gap
tags: [gap, gap-system, computational-group-theory, computer-algebra, permutation-groups, smallgroups-library, character-table, conjugacy-classes, sylow-subgroups, group-theory, representation-theory, cas, scripting]
level: practitioner
status: docs-checked
description: "Use GAP to build permutation and matrix groups, query classes, Sylow subgroups and centres, and avoid its left-to-right composition trap."
sources:
  - https://www.gap-system.org/doc/
  - https://docs.gap-system.org/doc/tut/chap1_mj.html
  - https://docs.gap-system.org/doc/tut/chap2_mj.html
  - https://docs.gap-system.org/doc/tut/chap5_mj.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Computing with groups in GAP

**Goal:** check or discover group-theoretic facts (orders, classes, subgroups) with the
GAP system instead of by hand.

## 1. Session basics
- A statement ends with `;`; a double semicolon `;;` prevents the result being printed.
- Assignment is `:=`; equality is `=`.
- `?help` opens help (for example `?SylowSubgroup`); `quit;` ends the session.
  `Read("file");` loads a file of GAP statements.
- The variable `last` holds the previous result.

## 2. Making groups
```gap
s4 := SymmetricGroup(4);;
h := Group((1,2,3,4), (1,2));;
m := GL(2, 3);;
```

## 3. Everyday queries
```gap
Size(s4); IsAbelian(s4);
ConjugacyClasses(s4);
SylowSubgroup(s4, 2);
Centre(s4); DerivedSubgroup(s4);
IsomorphismGroups(g1, g2);
```
These names all appear in the GAP tutorial's groups chapter. The Small Groups library
holds all groups of order at most 2000 except 1024 (GAP tutorial preface). Look up its
function names and the character-table functions in the reference manual of your version.

## 4. The composition trap
The tutorial states that `*` composes mappings left to right, and that group actions in
GAP are always from the right (`OnPoints(d, g)` is `d^g`). Many textbooks compose right to
left. Test one product before trusting a comparison with a hand calculation.

## Gotchas
- Printing huge objects floods the terminal; use `;;`.
- Function names and output formats can differ between GAP versions; confirm in the manual.

## Verify
- [ ] One hand-checkable fact (for example `Size(SymmetricGroup(4))` is 24) runs first.
- [ ] A sample product is checked against your composition convention.
- [ ] The script is saved in a file that `Read` can load, so results are reproducible.

## Checked
2026-11-01. Confirmed in the GAP tutorial (chapters 1, 2, 5): `;` and `;;`, `:=`, `=`,
`?help`, `quit;`, `Read`, `last`, SymmetricGroup, Group, GL, Size, IsAbelian,
ConjugacyClasses, SylowSubgroup, Centre, DerivedSubgroup, IsomorphismGroups, left-to-right
`*` and right actions, the Small Groups size range.
Removed (not found on the pages read): LogTo, list indexing, DihedralGroup argument
convention, FreeGroup and finitely presented examples, IsomorphismPermGroup,
NormalSubgroups, StructureDescription, IdGroup, SmallGroup and AllSmallGroups usage,
CharacterTable and Irr, specific outputs, and memory/speed advice.
Method: documentation only; no commands were run.
