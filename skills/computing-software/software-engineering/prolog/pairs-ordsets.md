---
id: computing-software.software-engineering.prolog.pairs-ordsets
name: pairs-ordsets
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, pairs-ordsets, ord-union]
level: practitioner
status: docs-checked
description: "Use library(pairs), ordered sets and list_to_set/2 in SWI-Prolog: keys and values, grouping, union and subtraction."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/pairs.pl
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/ordsets.pl
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/lists.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pairs and ordered sets
```prolog
?- pairs_keys_values(P, [a,b], [1,2]).          % P = [a-1, b-2]
?- transpose_pairs([a-2, b-1], T).               % T = [1-b, 2-a]
?- map_list_to_pairs(atom_length, [aaa,b], P).   % P = [3-aaa, 1-b]
?- group_pairs_by_key([a-1,a-2,b-3], G).         % G = [a-[1,2], b-[3]]
?- list_to_ord_set([c,a,b,a], S).                % S = [a,b,c]
?- ord_union([a,c], [b], U), ord_subtract([a,b,c], [b], D).
?- ord_memberchk(b, [a,b,c]).
?- list_to_set([a,b,a,X,X], S).                  % keeps first copies, order kept
```
- `group_pairs_by_key/2` groups consecutive pairs whose keys are `==`; sort with `keysort/2` first.
- `transpose_pairs/2` swaps keys and values and keysorts the result.
- `list_to_set/2` removes duplicates under `==`, keeps the left-most copy and preserves order; its cost is N*log(N). The list may contain variables.
- `ord_*` predicates expect ordered sets as built by `list_to_ord_set/2` or `sort/2`.
## Gotchas
- `list_to_set/2` compares with `==`, so `f(X)` and `f(Y)` are distinct.
- Build the input of `ord_*` predicates with `sort/2`.
## Self-check
`group_pairs_by_key([b-1,a-2,b-3], G)` does not merge the two `b` keys; after `keysort/2` it does.

## Checked

2026-11-03. SWI-Prolog library(pairs) and library(lists) documentation and source (pairs.pl, lists.pl, ordsets.pl in swipl-devel): signatures and behaviour of the predicates above, list_to_set/2 semantics (==, left-most copy, N*log(N), variables allowed). Removed: the claim that list_to_set/2 does not work for lists with variables (wrong) and the claim that ordset predicates silently misbehave on unsorted input (not covered).

Method: documentation only; no commands were run.
