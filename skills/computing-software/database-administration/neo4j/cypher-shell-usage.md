---
id: computing-software.database-administration.neo4j.cypher-shell-usage
name: cypher-shell-usage
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, cypher-shell-options, cypher-shell-file, cypher-shell-format, cypher-shell, neo4j-admin, browser, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Command-line client"
sources:
  - https://neo4j.com/docs/operations-manual/current/cypher-shell/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cypher-shell

Goal: script against Neo4j.
- Example: `cypher-shell -a neo4j://host -u neo4j -p <PASSWORD> -d mydb -f script.cypher --format plain`.
- `--format` takes auto, verbose or plain; `--non-interactive` is documented; `:param` and `:begin`/`:commit`/`:rollback` are shell commands.
Verify: exit code non-zero on failure in CI.

## Checked

2026-11-02. Confirmed in the Cypher Shell page (synopsis with -a, -u, -p, -d, -f, --format {auto,verbose,plain}, --non-interactive; `:param`, `:begin`). Removed: the environment-variable credentials advice (not read on the page) and the exit-code claim kept only as a check to perform.
Method: documentation only; no commands were run.
