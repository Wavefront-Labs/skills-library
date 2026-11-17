---
id: computing-software.cloud-infrastructure-engineering.terraform.graph-type-and-draw-cycles-flags
name: graph-type-and-draw-cycles-flags
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, graph-type, draw-cycles, terraform-graph, dependency-graph, plan-graph, apply-graph, dot, graph-debugging]
level: practitioner
status: verified
description: "Choose the graph that answers your question: terraform graph -type=plan/plan-destroy/apply, -plan=FILE, and -draw-cycles to highlight the edges behind a Cycle error."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/graph", "https://developer.hashicorp.com/terraform/internals/graph"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `graph -type` and `-draw-cycles`

**Goal:** generate the specific dependency graph Terraform will walk — not the
generic config graph — so ordering and cycle problems are visible.

## 1. Graph types
```bash
terraform graph                               # default: config graph (1.7+: simplified resource-only view)
terraform graph -type=plan                    # the graph a plan walks (includes data sources, providers, module boundaries)
terraform graph -type=plan-destroy            # graph for a destroy plan (reversed edges)
terraform graph -type=plan-refresh-only       # graph for a refresh-only plan
terraform graph -type=apply                   # apply graph built from the configuration
terraform graph -plan=tfplan                  # apply graph of a SAVED plan (-plan implies -type=apply)
terraform graph -draw-cycles -type=plan       # colour cycle edges red (needs an operation -type)
terraform graph -format=mermaid               # Mermaid flowchart instead of DOT (dot is the default)
terraform graph -module-depth=1               # deprecated: collapse modules deeper than N (older versions)
```
Output is Graphviz DOT on stdout (or Mermaid with `-format=mermaid`). Since 1.7 the default
(no `-type`) output is a reduced graph of just resources, with plain node names such as
`"terraform_data.b" -> "terraform_data.a";` and module resources inside `subgraph "cluster_module.m"`;
use `-type=plan` for the full picture Terraform actually uses (nodes there carry a `[root] `
prefix and ` (expand)` suffix).

## 2. Which type for which problem
| Question | Type |
|---|---|
| Why does X apply before/after Y? | `-type=plan` (or `-plan=tfplan` for exactly this change) |
| Why is destroy failing on dependency order? | `-type=plan-destroy` |
| Where is the cycle? | `-draw-cycles -type=plan` and look for `color = "red"` edges |
| What does this provider block depend on? | `-type=plan` — provider nodes appear as `provider["registry.terraform.io/hashicorp/aws"]` |

## 3. Reading the DOT
- Nodes: `"aws_instance.web"`, `"module.vpc.aws_vpc.this"`, `"data.aws_ami.x"`,
  `"var.name"`, `"provider[...]"`, `"output.x"`.
- Edge `A -> B` means **A depends on B** (B is applied first).
- `(expand)` nodes are `count`/`for_each` expansion points; `(close)` nodes bound
  module scope.
- Red edges (`-draw-cycles`, written as `[color = "red", penwidth = "2.0"]`) are the cycle members; follow them to the resource
  pair and break the loop with `create_before_destroy` changes, splitting a
  resource, or removing a `depends_on`.

## 4. Filtering
Graphs of real states are thousands of nodes. Trim with grep before rendering:
```bash
terraform graph -type=plan | grep -E 'aws_security_group|aws_instance' | grep -- '->' > sub.dot
```
Or in dot, keep only edges touching a node:
```bash
terraform graph -type=plan | grep -E '"aws_lb\.app"' 
```
(see `computing-software.cloud-infrastructure-engineering.terraform.rendering-graph-output-with-graphviz` for rendering).

## Gotchas
- `-type=apply` without `-plan` does not error on 1.17.0: it prints an apply graph built from the
  configuration; add `-plan=tfplan` to graph a specific saved plan.
- The graph reflects the **current working directory config and state**; run `init` first
  (without it, a configuration with a registry provider fails with `Inconsistent dependency lock file`).
- A reference cycle makes plain `terraform graph` (no `-type`) fail with `Error: Cycle:` followed by one
  node per line, as `plan` and `validate` do; `terraform graph -type=plan -draw-cycles` still prints
  the graph with the cycle edges in red.
- OpenTofu 1.13.2: `tofu graph` (no `-type`) prints the full operation graph with `[root] ` and
  `(expand)` nodes; its `-type` accepts plan (default), plan-refresh-only, plan-destroy and apply,
  and it has `-draw-cycles` and `-plan`. Use `tofu graph -help` for your version.

## Verify
- [ ] `terraform graph -type=plan | grep -c -- '->'` is non-zero and includes provider edges.
- [ ] On a known cycle, `-draw-cycles` output contains `color = "red"`.

## Checked
- Terraform 1.17.0 `terraform graph -help`: `-plan` (implies apply), `-draw-cycles` (only with `-type`), `-type` plan/plan-refresh-only/plan-destroy/apply, `-module-depth` deprecated, `-format` dot or mermaid. Ran every variant on a three-resource config with a module: default output (simplified, plain names, `cluster_module.m` subgraph), `-type=plan` (`[root]` and `(expand)` nodes, provider diamonds), `-type=plan-destroy`, `-type=plan-refresh-only`, `-type=apply`, `-plan=tfplan`, `-format=mermaid`.
- On a deliberate two-resource cycle: `plan` and `validate` printed `Error: Cycle:` with two lines; default `graph` errored too; `graph -type=plan -draw-cycles` printed both edges with `color = "red", penwidth = "2.0"`, and rendering that through Graphviz 12.2.1 `dot -Tsvg` produced 4 red strokes.
- Changelog v1.7 (raw.githubusercontent.com/hashicorp/terraform/v1.7/CHANGELOG.md): `terraform graph` now produces a simplified resources-only graph by default.
- `-type=apply` with no `-plan` printed a graph (the skill said it errors). Uninitialised config gave `Inconsistent dependency lock file`. OpenTofu 1.13.2 `graph -help` and output as described.
