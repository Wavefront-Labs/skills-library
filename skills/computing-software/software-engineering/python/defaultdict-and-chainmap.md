---
id: computing-software.software-engineering.python.defaultdict-and-chainmap
name: defaultdict-and-chainmap
category: computing-software
field: software-engineering
product: python
tags: [python, py-collections, defaultdict-chainmap, defaultdict, chainmap, ordereddict, layered-config, grouping]
level: practitioner
status: docs-checked
description: "Group and accumulate with defaultdict, layer settings with ChainMap (CLI over env over defaults) and know when OrderedDict or dict.setdefault is enough."
sources: ["https://docs.python.org/3/library/collections.html#collections.defaultdict", "https://docs.python.org/3/library/collections.html#collections.ChainMap"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defaultdict and ChainMap

## defaultdict
```python
from collections import defaultdict, ChainMap
groups = defaultdict(list)
for word in words:
    groups[word[0]].append(word)        # no KeyError, no setdefault boilerplate

graph = defaultdict(set); graph["a"].add("b")
counts = defaultdict(int); counts["x"] += 1
tree = lambda: defaultdict(tree)         # autovivifying nested dict
```
`default_factory` is called by `__missing__` for **`d[key]` only**. `d.get(key)` and `key in d` do not create entries, but a plain read `d["typo"]` does insert a new key. Freeze when done: `dict(groups)` or set `groups.default_factory = None`.

## ChainMap
```python
defaults = {"color": "red", "user": "guest"}
env = {"user": "ada"}
cli = {}
cfg = ChainMap(cli, env, defaults)       # lookup order: first mapping wins
cfg["user"]                               # 'ada'
cfg["color"] = "blue"                     # writes only go to the FIRST mapping (cli)
child = cfg.new_child({"user": "tmp"})    # scoped override, like a stack frame
cfg.parents                               # without the first layer
```
Views are live: later changes to `env` show through. Good for config layering and interpreter-style scopes.

## Gotchas
- `ChainMap` writes, updates and deletions only operate on the first mapping.
- A plain `dict` keeps insertion order; reach for `OrderedDict` only for `move_to_end` or order-sensitive equality.
- `defaultdict(list)` is documented as simpler and faster than the equivalent `dict.setdefault(k, []).append(v)`.

## Verify
- [ ] Test that reading a missing key from a defaultdict inserts it (or that you froze it).
- [ ] ChainMap precedence test: cli > env > defaults for each key.

## Checked

- 2026-11-03: checked against the CPython docs `library/collections.rst`: `__missing__` is called only by `__getitem__` and inserts the value, `get` returns None, `default_factory` attribute, ChainMap lookup order, writes to the first map, live views by reference, `new_child`, `parents`, OrderedDict `move_to_end` and order-sensitive equality, defaultdict versus `setdefault`.
- Removed: defaultdict pickling remark, ChainMap iteration/len/KeyError details (not in the docs read).

Method: documentation only; no commands were run.
