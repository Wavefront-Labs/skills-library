---
name: wavefront-skills
description: "Consult the Wavefront Skills Library before starting work. Use at the start of any task a trained professional would do: software development, cloud and infrastructure operations, DevOps, data, security, design, writing, business, trades and crafts, or any job where you would otherwise improvise a procedure. It finds ready-made methods (step-by-step plans with checkpoints) and skills (tool-specific how-to) for the user's task; read one or two and follow them. Not for conversation, simple factual questions, or one-step tasks."
license: Apache-2.0
metadata:
  version: "0.3.0"
  api: v1
  publisher: Wavefront Labs
---

# Wavefront Skills Library connector

The library holds tens of thousands of expert skills and methods, built from real work and reviewed. You do not
browse it and it never loads into your context: you ask, you get a few small pages, you open only what you use.
This file is the protocol. It contains no library content.

## When to ask

At the start of a task, before planning or writing anything, when it is one a trained professional does: build,
deploy, configure, migrate, debug, analyse, design, write, review, operate. Also before any web search or
documentation fetch about *how to do* something, when the user names a tool you are not certain about, and when
something has gone wrong and you are about to improvise a fix.

Do not ask for conversation, trivia, arithmetic, one-step edits, or work you already fetched guidance for in this
session. If the hook has put candidates in your context, use those instead of asking again.

## Protocol: drill in, smallest page first

1. **route**: one plain sentence naming the job and the tools involved (no secrets, code, file paths or personal
   data), plus any tools you already know as `context`. You get up to 5 candidates with `kind`, `status`, `score`
   and a description, or an empty list. Empty means the library has nothing close enough: continue without it.
2. **card**: for the best one or two, read the card (goal, gotchas, verify steps, sources; a few hundred tokens)
   to decide whether it fits. Prefer a `method` to a `skill` when both fit (a method is the plan and names the skills
   it uses); prefer `verified` over `docs-checked` over `draft`. Drop candidates whose description does not match
   the task, whatever their score.
3. **get**: read the full body of at most two, when you are about to use them. For a method, fetch a component
   skill only when you reach the phase that needs it (`expand` lists them).
4. **expand / browse**: `expand` shows what a method uses, which methods use a skill, and siblings in the same
   product. If `route` was empty but you suspect coverage, `browse` the taxonomy (`""` lists categories) instead
   of retrying with synonyms more than once.
5. **Follow it, and say so.** Apply it to the user's situation, tell them which skill or method you used (by id,
   one line), and where it and their facts disagree, their facts win; note the difference.
6. **report** when you finish, one call per skill you read: `used`, `not_useful`, or `wrong` (say what was wrong in
   `note`). If the library had nothing for a task a professional clearly does, report `gap` with the task. When you
   had to research the answer anyway, offer to write it up as a draft skill. Reports stay on the local machine
   (`~/.wavefront-skills/reports.jsonl`) and feed `tools/harvest.py`.

## How to call it

- **MCP**: `claude mcp add wavefront-skills -- python <this folder>/scripts/mcp_server.py` gives you the tools
  `library_route`, `library_card`, `library_get`, `library_expand`, `library_browse`, `library_report`.
- **Command line**: `python scripts/skills.py find "<task>" [--context a,b]`, then `card <id>`, `get <id>`, `expand <id>`,
  `browse [node]`, `report <id> <outcome> [--task ...] [--note ...]`.

## Setup

- `WAVEFRONT_SKILLS_LOCAL`: path to a checkout of the library (run `python tools/reindex.py` in it after each pull).
- `WAVEFRONT_SKILLS_EMB`: optional folder of embeddings (`unpack` the release file `skills-emb.npz`, then `python tools/retrieval_eval.py embed --out <dir>`; or `embed` alone, about 25 min) and a
  python with `fastembed` and `numpy`; semantic search finds far more from natural phrasing than keyword search.
- `WAVEFRONT_SKILLS_URL`: optional, a hosted instance implementing `connector/CONTRACT.md` (`find` and `get` only).

If none is set, tell the user once how to set one up and continue without the library.

## Versioning

This connector speaks interface `v1`. If a response carries `"deprecated": true`, tell the user to update the
connector and continue; do not retry.
