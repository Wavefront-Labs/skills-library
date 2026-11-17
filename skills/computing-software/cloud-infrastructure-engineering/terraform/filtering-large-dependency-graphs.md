---
id: computing-software.cloud-infrastructure-engineering.terraform.filtering-large-dependency-graphs
name: filtering-large-dependency-graphs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, graph-filtering, large-graph, terraform-graph, graphviz, dependency-graph]
level: practitioner
status: verified
description: "Make terraform graph output usable on big configurations: extract one resource's ancestors and descendants with gvpr or Python, and trim provider and variable noise."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/graph", "https://graphviz.org/pdf/gvpr.1.pdf", "https://graphviz.org/docs/cli/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtering large `terraform graph` output

A root module with a few hundred resources renders an unreadable hairball. Filter
the DOT before rendering.

## Get the DOT
```bash
terraform graph > full.dot               # 1.7+: simplified resource-only graph by default
terraform graph -type=plan > plan.dot    # full operation graph incl. providers, vars
```
Prefer the default (resources only) for dependency questions.

## Ancestors / descendants of one node
Node names look like `"aws_lb.main"` or `"module.app.aws_ecs_service.svc"`. A small
Python script keeps everything reachable from the target in either direction:
```python
import re, sys, collections
edges = re.findall(r'"([^"]+)"\s*->\s*"([^"]+)"', open("full.dot").read())
fwd, rev = collections.defaultdict(set), collections.defaultdict(set)
for a, b in edges: fwd[a].add(b); rev[b].add(a)
def walk(g, n, seen=set()):
    for m in g[n]:
        if m not in seen: seen.add(m); walk(g, m, seen)
    return seen
target = sys.argv[1]
keep = walk(fwd, target, set()) | walk(rev, target, set()) | {target}
print("digraph {"); [print(f'"{a}" -> "{b}"') for a, b in edges if a in keep and b in keep]; print("}")
```
```bash
python sub.py 'module.app.aws_ecs_service.svc' | dot -Tsvg > svc.svg
```
In Terraform's DOT an edge `A -> B` means A depends on B.

## Module-level view
Collapse resources to their module prefix to see module coupling:
```bash
sed -E 's/"(module\.[^.]+)\.[^"]*"/"\1"/g' full.dot | awk '!seen[$0]++' | dot -Tsvg > modules.svg
```

## Trim noise in -type=plan graphs
Every node in a `-type=plan` graph starts with `[root] `, so a plain `root` pattern deletes the whole
file. Strip the prefix first and match only the `"root"` node:
```bash
sed 's/\[root\] //g' plan.dot | grep -vE 'provider\[|var\.|local\.|output\.|\(close\)|"root"' > lean.dot
```
(`lean.dot` drops edges to variables and providers, which may disconnect module-boundary edges.)

## Gotchas
- `-type=plan` graphs include `(expand)` nodes and `[root] ` prefixes with escaped quotes inside provider names
  (`provider[\"...\"]`); strip them before matching, and note the extraction regex above is written for the
  default graph, whose edge lines look like `"b" -> "a";`.
- `dot` layout slows down on very large graphs; filter first (above), or try Graphviz's `sfdp` layout engine.

## Verify
- [ ] Subgraph contains the resources you expect to depend on the target and nothing unrelated.

## Checked
- Terraform 1.17.0, config with `a`, `b` (refs a), module `m` (refs b), `c` (refs module output): `terraform graph` printed edges `"b" -> "a";`, `"c" -> "module.m.terraform_data.inner";`, and the module resource inside `subgraph "cluster_module.m"`. The Python script (run unchanged) printed the connected subgraph for `terraform_data.b` and `terraform_data.a`, and the output rendered with Graphviz 12.2.1 `dot -Tsvg` (exit 0); the module-collapsing `sed | awk` also rendered (the module node's label stays the inner resource name).
- `grep -vE '...|root' plan.dot` as originally written removed every node and edge line (all start with `[root]`); the corrected two-step command kept the resource nodes and edges.
- The `-type=plan` nodes carry ` (expand)`. `sfdp` is shipped in the Graphviz 12.2.1 bin folder; no timing claim remains.
