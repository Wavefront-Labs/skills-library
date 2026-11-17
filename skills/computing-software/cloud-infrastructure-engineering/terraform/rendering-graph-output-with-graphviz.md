---
id: computing-software.cloud-infrastructure-engineering.terraform.rendering-graph-output-with-graphviz
name: rendering-graph-output-with-graphviz
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, graphviz-render, dot-rendering, terraform-graph, dot, svg, png, dependency-graph, visualisation, rover, blast-radius]
level: intro
status: gated
description: "Turn terraform graph DOT output into a readable SVG/PNG: dot vs sfdp for large graphs, pruning nodes, rankdir, and alternatives (Rover, blast-radius, inframap) when Graphviz is unreadable."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/graph", "https://graphviz.org/doc/info/command.html", "https://github.com/im2nguyen/rover"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rendering graph output with Graphviz

**Goal:** a picture you can actually read, from a DOT file that is usually far
too big.

## 1. Basic render
```bash
brew install graphviz   # apt-get install graphviz (gated: unconfirmed, source is paywalled or blocked) (installers not run; Graphviz 16.1.0 portable zip used on Windows)
terraform graph -type=plan > graph.dot
dot -Tsvg graph.dot -o graph.svg      # hierarchical layout; SVG is zoomable and searchable
dot -Tpng -Gdpi=150 graph.dot -o graph.png
```
Open the SVG in a browser; Ctrl-F finds resource names.

## 2. Make big graphs readable
- Layout engine: `dot` for < ~300 nodes; `sfdp -Goverlap=prism` or `neato` for
  bigger; `twopi` for radial views of a hub resource.
- Left-to-right: `dot -Grankdir=LR`.
- Prune noise before rendering — providers, variables, outputs. In `-type=plan` output every node is written `"[root] <address> (expand)"` and nested in a `subgraph "root" {` block, so the older pipeline `grep -v '"(var|output|provider|local)\b'` followed by `grep -v 'root'` matched nothing useful and then deleted every node line, leaving invalid DOT (ran: `syntax error in line 1 near '}'`). The filter below keeps the braces:
```bash
terraform graph -type=plan \
  | grep -v -E 'provider\[|\[root\] root|\.(var|output)\.|\(close\)' \
  | dot -Tsvg -o graph.svg
```
- Focus on one resource's neighbourhood:
```bash
terraform graph -type=plan | grep -E 'aws_lb\.app |digraph|^\s*\}|compound|newrank|subgraph' > focus.dot
```
(keep the `digraph {` header, the attribute lines and every closing brace; ran with `terraform_data.b` in place of `aws_lb.app`: the filtered DOT rendered with `dot -Tsvg`, whereas `grep -E '"terraform_data\.b"|digraph|^}'` produced no usable graph.)
- Strip the long `registry.terraform.io/hashicorp/` prefix from provider nodes:
  `sed 's#registry.terraform.io/hashicorp/##g'` (the builtin `terraform_data` provider node has no such prefix, so only third-party providers need it).

## 3. Alternatives when DOT is hopeless
- Tools below were not run (gated: unconfirmed, source is paywalled or blocked). **Rover** (`im2nguyen/rover`): `docker run --rm -it -p 9000:9000 -v $(pwd):/src im2nguyen/rover`
  renders an interactive browser graph from the plan, with resource details.
- **blast-radius**: interactive d3 graph; `blast-radius --serve .` (needs Graphviz).
- **inframap**: `inframap generate terraform.tfstate | dot -Tpng` draws only
  "real" infrastructure (provider-aware pruning).
- **terraform-visual**: renders a plan JSON as HTML.
Use these for architecture reviews; use raw DOT + grep for debugging a specific
ordering/cycle problem.

## Gotchas
- `dot` on a 5,000-node graph can run for minutes or exhaust memory; try `sfdp`
  first or prune.
- `-type=plan` graphs include module `(expand)`/`(close)` nodes that clutter the
  picture; filter them.
- Rendering is from your working directory state; sensitive values never appear
  in the graph (node names only), so SVGs are safe to attach to a PR.
- Windows: Graphviz installer must add `dot` to PATH; otherwise call it by full
  path.

## Verify
- [ ] `dot -Tsvg graph.dot -o graph.svg` succeeds and the SVG opens with resource names visible.
- [ ] After pruning, the graph for one resource shows its direct upstream and downstream edges only.

## Checked
- Terraform 1.17.0 and Graphviz 16.1.0 (portable zip) on Windows: `dot -Tsvg`, `-Tpng -Gdpi=150`, `-Grankdir=LR`, `sfdp`, `neato` and `twopi` all rendered a plan graph; the default `terraform graph` is the simplified resource graph, `-type=plan` has `[root]`, `(expand)` and `(close)` nodes; the skill's original prune and focus commands failed or produced empty graphs, the corrected ones rendered.
- Gated: package-manager installs, Rover, blast-radius, inframap, terraform-visual, large-graph timing.
