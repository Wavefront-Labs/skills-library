# Instructions for AI agents

You are an LLM agent working with this repository. Two jobs: **use** the library to do your own task, or **add to it**.
Humans: the same information is in [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Use the library (before you research or reason a task out)

Ask first, then work. Do it for any job a trained professional would do (build, deploy, configure, debug, analyse,
design, write, operate), and before web research about *how to do* something.

1. `route`: one plain sentence naming the job and the tools (no secrets, code or personal data). You get up to 5
   candidates `{id, kind, status, score, description}`, or nothing. Nothing means the library has no coverage: carry on without it.
2. `card <id>`: goal, gotchas, verify steps and sources in a few hundred tokens. Prefer a `method` (a plan that names
   the skills it uses) over a `skill`, and `verified` over `docs-checked` over `draft`. Drop a candidate whose
   description does not match the task, whatever its score.
3. `get <id>`: the full file. Read at most two. For a method, fetch component skills only when you reach their phase (`expand <id>` lists them).
4. Follow it, tell the user which id you used, and where it disagrees with the user's facts, the user's facts win.
5. `report <id> used|not_useful|wrong|gap`. Reports stay on the local machine.

How to get these operations:

- **MCP server** (any MCP client): run `python connector/wavefront-skills/scripts/mcp_server.py` as a stdio server with
  `WAVEFRONT_SKILLS_LOCAL=<path to this repo>`. Claude Code: `claude mcp add -e WAVEFRONT_SKILLS_LOCAL=<path to this repo> wavefront-skills -- python <path>/connector/wavefront-skills/scripts/mcp_server.py`.
- **Command line** (any agent that can run commands): `python connector/wavefront-skills/scripts/skills.py find "<task>"`, then `card`, `get`, `expand`, `browse`, `report`.
- **Plain search, no setup beyond `pip install -r requirements.txt && python tools/reindex.py`:** `python tools/serve.py search <words>` and `python tools/serve.py get <id>`.
- **Agent Skills loaders** (Claude Code and others): copy `connector/wavefront-skills/` into the skills folder. It carries the protocol above and no library content.
- Better matching from natural phrasing needs semantic search; see step 3 of [connector/README.md](connector/README.md) (a prebuilt embedding file is attached to each release, so you do not embed 51K skills yourself).

## Add to the library

Never fabricate. A skill is worth adding only when you can write it from behaviour you verified (commands you ran,
pages you read), and a library skill must not be a restatement of general knowledge.

1. Search first (`route` or `serve.py search`). Extend or correct an existing skill rather than duplicate it.
2. Pick the path with the taxonomy guide in CONTRIBUTING.md (`category.field.product.name`), then scaffold:
   `python tools/new_skill.py <category> <field> <product> <name> "<one-line description, max 200 chars>"`
3. Write the body: exact commands, settings, numbers, failure modes, a self-check. 50-150 lines. Frontmatter fields,
   levels and the evidence rules are in [SCHEMA.md](SCHEMA.md); the description and `tags` are what search matches
   on, so put the words a person would use there.
4. New skills are `status: draft`, with `sources:` listing what you checked against. **Never set `docs-checked` or
   `verified` yourself.** A maintainer promotes the status after checking the claims. State what is unconfirmed.
5. Changing an existing skill: bump `version` and set `updated` to today. Moving one: keep the old id in `aliases`. Ids are permanent.
6. `python tools/lint.py` must pass (about 6 minutes on the full tree; CI runs it on every pull request).
7. One skill or one coherent change per pull request. Commit with `git commit -s` (Signed-off-by agrees to Apache-2.0).
   Open the pull request from a fork against `main`; use the PR template.

Never include secrets, credentials, personal data, machine-specific paths, or copied copyrighted text. Content that
helps attack systems you do not own is out of scope; the security fields are defensive.
