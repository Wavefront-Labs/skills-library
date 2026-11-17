---
id: computing-software.software-engineering.prolog.assoc-library
name: assoc-library
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-assoc-sets, assoc-library, rbtrees]
level: practitioner
status: docs-checked
description: "Store key-value maps in AVL trees with list_to_assoc/2, put_assoc/4, get_assoc/3, and rb_* for red-black trees."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Association lists as AVL trees
```prolog
:- use_module(library(assoc)).
?- list_to_assoc([a-1,b-2], A), put_assoc(c, A, 3, A2), get_assoc(c, A2, V), assoc_to_list(A2, L).
?- empty_assoc(E), assoc_to_keys(E, K).
?- max_assoc(A2, K, V).
:- use_module(library(rbtrees)).
?- rb_new(T0), rb_insert(T0, k, v, T1), rb_lookup(k, V, T1).
```
- AVL trees, purely functional (a new tree is returned).
- `get_assoc/3` fails if absent; `del_assoc/4` removes.
## Gotchas
- Keys are compared by standard order; `1` and `1.0` differ.
- `list_to_assoc` raises `domain_error(unique_key_pairs, List)` on duplicate keys; `ord_list_to_assoc` takes pairs already sorted by key.
## Self-check
Count word frequencies into an assoc with `foldl`.

## Checked

2026-11-02. library(assoc) source (empty_assoc, list_to_assoc, ord_list_to_assoc, put_assoc(Key, Assoc0, Value, Assoc), get_assoc semidet, del_assoc/4, max_assoc/3, assoc_to_list, assoc_to_keys; AVL trees; domain_error(unique_key_pairs, _) on duplicates), library(rbtrees) (rb_new/1, rb_insert(Tree, Key, Value, NewTree), rb_lookup(Key, Value, Tree)) and the standard order of terms (equal numbers: float before integer). Removed: the O(log n) figure (not stated in the source).

Method: documentation only; no commands were run.
