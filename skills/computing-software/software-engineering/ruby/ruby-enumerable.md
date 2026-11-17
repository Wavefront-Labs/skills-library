---
id: computing-software.software-engineering.ruby.ruby-enumerable
name: ruby-enumerable
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-collections, enumerable]
level: intro
status: docs-checked
description: "Use Enumerable methods like map, select, reduce, group_by, partition, each_with_object, tally."
sources: ["https://docs.ruby-lang.org/en/master/Enumerable.html", "https://docs.ruby-lang.org/en/master/Array.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Enumerable methods map select reduce group_by
- Documented Enumerable methods: `map`, `select`/`filter`, `reject`, `find`, `inject`/`reduce`, `sum`, `group_by`, `partition`, `tally`, `each_with_object`, `zip`, `flat_map`, `min_by`, `sort_by`, `each_cons`, `chunk_while`, `filter_map` (select plus map).
- The `Array#sum` source cites Kahan-Babuska compensated summation for floats.
- Include `Enumerable` in your class and define `each`.
Verify: empty-collection cases for every method you use.

## Checked
2026-11-02. Confirmed against: Enumerable method names and filter_map meaning; Kahan-Babuska comment in Array#sum source. Removed or softened (not stated on those pages): version tags, Schwartzian-transform remark, Enumerable-for-all-classes sum claim.
Method: documentation only; no commands were run.
