# Library interface (v1)

The operations any server in front of the library offers. `tools/librarian.py` implements all six over a local
checkout; `connector/wavefront-skills/scripts/mcp_server.py` exposes them over MCP; a hosted instance returns the
same shapes as JSON and may implement only `find` and `get`. The library is Apache-2.0: there is no
authentication and no metering beyond what a host needs to protect a shared instance.

## Principles

- **Zero standing cost.** The agent carries "how to ask" (about 250 tokens of tool descriptions), not a catalogue.
- **Drill in.** Every response is a small bounded page; the agent expands only the branch it needs.
- **Silence beats noise.** Below a relevance bar the answer is an empty list. A wrong candidate costs more than none.
- **Trust is visible.** `status`, `level`, `version`, `updated` and `sources` travel with every result.
- **Pull only.** The library never pushes bodies into context; the agent fetches what it uses.
- **The loop closes.** `report` says what worked, so the library learns what to fix and what to write.

## Operations

| Operation | Input | Returns |
|---|---|---|
| `route` (`GET /v1/find`) | `task`, optional `context` (tools already known), `k <= 10` | up to `k` of `{id, kind, status, level, score, description}`, methods above skills at equal relevance; `[]` when nothing is close enough |
| `card` | `id` | `{id, kind, status, level, version, updated, description, goal?, gotchas?, verify?, sources?, tokens_est, body_tokens_est}` |
| `get` (`GET /v1/skills/{id}`) | `id` | `{notice, id, kind, status, version, updated, body}` |
| `expand` | `id` | `{uses?, used_by_methods?, siblings, siblings_total}` (a method's component skills; the methods that use a skill; same-product skills) |
| `browse` | `node` (`""`, `category`, `category.field`, `category.field.product`), `offset` | `{node, total, offset, children}`; children are nodes with `count` and a one-line `summary`, or skills at the leaf |
| `report` | `id`, `outcome` (`used`, `not_useful`, `wrong`, `gap`), `task?`, `note?` | `{logged}`; appended to a local log, nothing leaves the machine |

Every response that carries library text starts with the licence `notice`. Gated skills are not returned by default;
drafts are, with their status visible. Old ids keep resolving after a move (aliases). A deprecated interface version
answers normally and adds `"deprecated": true`.

## Retrieval

Semantic search (embeddings) fused with ranked keyword search. The decision to answer or stay silent uses both: speak
when the top cosine is clearly high, or moderately high and the keyword search independently agrees. Methods get a
small boost. See `tools/librarian.py` (`route`, `_speak`) and `tools/retrieval_eval.py` for how it is tested.

## Errors and privacy

`404` no such skill; `429` rate limited (a shared host protecting itself). Bodies are `{"error": "<short reason>"}`.
A host should log query text only for retrieval quality, briefly, and never tie it to a person; clients send a
one-sentence summary with no secrets, paths, code or personal data, and servers truncate `task` at 300 characters.
