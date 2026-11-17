# Wavefront Skills Library

An open library of expert skills and methods for AI agents, organised
**category → field → product → skill** and built so an agent can consult tens of thousands of
skills (eventually far more) while carrying almost nothing in its context. Apache-2.0.

A **skill** is one technique a professional would know: the exact commands, settings, numbers,
failure modes and a self-check, in 50-150 lines. A **method** is a recipe: which skills to use for
an outcome, in what order, with measurable gates. Every file carries a review `status`, so you
can see how far it has been checked.

<!-- skills-status:start -->
**Review status:** <!-- STATUS:START -->2,686 verified · 31,149 docs-checked · 1,738 gated · 15,947 draft of 51,520 skills<!-- STATUS:END -->. Drafts are written but not yet checked against sources; the status in each file says which you are reading.
<!-- skills-status:end -->

## Using it from your agent (or any LLM)

The library is meant to be *asked*, not read. The agent states the job, gets a short ranked list, opens the one or
two files that fit, and follows them. That replaces research it would otherwise do from scratch. The agent carries
about 250 tokens of "how to ask", never the catalogue.

**Setup (5 minutes, once):**

```bash
git clone https://github.com/Wavefront-Labs/skills-library.git && cd skills-library
pip install -r requirements.txt && python tools/reindex.py     # builds skills.index.jsonl (about 6 min)
```

Then pick how your LLM reaches it:

| Your setup | What to do |
|---|---|
| **Claude Code, or any MCP client** | Run the MCP server: `claude mcp add -e WAVEFRONT_SKILLS_LOCAL=<path to the clone> wavefront-skills -- python <path>/connector/wavefront-skills/scripts/mcp_server.py`. Other clients: add a stdio server that runs that script with the same env var. The agent gets six tools (`library_route`, `card`, `get`, `expand`, `browse`, `report`) and their descriptions teach the protocol. |
| **Agents that load Agent Skills** | Copy `connector/wavefront-skills/` into your skills folder (`~/.claude/skills/`). It holds the protocol only. |
| **Make it automatic (Claude Code)** | Add the hook from [`connector/README.md`](connector/README.md): the library is consulted on every real prompt and before any web search, and stays silent when nothing fits. |
| **Any other LLM or script** | Point it at [`AGENTS.md`](AGENTS.md) (written for an LLM to read), or paste the five-step protocol from it into your system prompt. The agent calls `python tools/serve.py search <words>` and `python tools/serve.py get <id>`, or `python connector/wavefront-skills/scripts/skills.py find "<task>"`. |

Search quality: keyword search needs the skill's own words; semantic search finds the right skill from natural
phrasing (79% vs 29% in our blind test). It needs `pip install fastembed numpy` and an embedding folder: download
`skills-emb.npz` from the latest release, run `python tools/retrieval_eval.py unpack skills-emb.npz --out <dir>`,
and set `WAVEFRONT_SKILLS_EMB=<dir>`. Without it everything still works on keyword search.

Or browse: [`SKILLS.md`](SKILLS.md) lists the categories; each `INDEX.md` lists one level down; the skill files are
plain Markdown with YAML frontmatter. Interface details are in [`connector/CONTRACT.md`](connector/CONTRACT.md).

## Reading a skill

Frontmatter tells you what you are holding:

- `status`: `draft` (written, not yet checked), `docs-checked` (claims checked against the official
  documentation), `verified` (executed end to end), `gated` (could not be reviewed: paywalled or blocked
  sources; treat with care).
- `level`: `intro`, `practitioner`, `advanced`, `sme`.
- `sources`, `version`, `updated`, and `aliases` (old ids, if the skill ever moved).

Ids are permanent. `category.field.product.name` is also the file path, and other skills and methods refer to
skills by id.

## Contributing

Contributions are welcome: new skills, corrections, methods, and taxonomy fixes. The bar is that a reader can
act on the skill correctly; the format is strict so that a library this size stays searchable. **Every pull
request is checked automatically against the schema** (`tools/lint.py`, the id/version rules, the index build),
and a maintainer reviews it, may edit it for consistency, and promotes its status.

**As a person:**

1. Fork the repo, clone your fork, run the setup above.
2. Search first (`python tools/serve.py search <words>`) so you extend rather than duplicate. Wrong or outdated
   skill? Fix it in place (bump `version`, set `updated`) or open an issue with the skill id.
3. Scaffold: `python tools/new_skill.py <category> <field> <product> <name> "<one-line description>"`, write the
   body from verified behaviour, list your `sources`. Placement help is in [`CONTRIBUTING.md`](CONTRIBUTING.md).
4. `python tools/lint.py`, commit with `git commit -s`, open a pull request from your fork to `main`.

**With an LLM agent:** point it at [`AGENTS.md`](AGENTS.md). It has the same steps as a checklist, including the
rules an agent must not break: new skills are `status: draft`, never self-promoted to `docs-checked` or `verified`,
no invented commands, no secrets. Review what your agent wrote before you open the PR; you are the contributor.

Rules for everyone: new contributions land as `status: draft`. Write from verified behaviour and say what is
unconfirmed. Don't paste copyrighted text or anything you can't license under Apache-2.0; never include secrets,
personal data or machine-specific paths. By submitting you agree your contribution is Apache-2.0 (sign off with `-s`).
See also [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) and [`SECURITY.md`](SECURITY.md).

## Layout
```
SKILLS.md              the categories and how to search
SCHEMA.md              the skill file contract
CONTRIBUTING.md        how to add or change skills
AGENTS.md              the same, written for an LLM agent (use and contribute)
skills/<category>/<field>/<product>/<name>.md    the skills and methods
taxonomy/              where a skill should go: categories, fields, products, coverage specs
tools/                 new_skill.py  lint.py  reindex.py  serve.py  retrieval_eval.py
connector/             the connector skill, hook, interface contract and evaluation harness
```

`taxonomy/` is the map; `skills/` is the territory. A product can exist in the taxonomy with no skills
under it yet.

## Stats
<!-- STATS:START (generated by tools/reindex.py — do not edit by hand) -->
_29/29 categories started, 51520 skills total._

| category | fields with skills | skills |
|---|---|---|
| computing-software | 32 | 40202 |
| creative-arts | 19 | 5837 |
| engineering-technology | 24 | 1585 |
| health-medicine | 47 | 393 |
| law-government | 26 | 281 |
| handcrafts | 32 | 231 |
| sports-recreation | 26 | 221 |
| architecture-construction | 22 | 184 |
| repair-maintenance | 23 | 182 |
| transportation-logistics | 20 | 162 |
| agriculture-environment | 18 | 157 |
| defence-public-safety | 19 | 151 |
| religion-philosophy | 21 | 148 |
| sales-marketing | 25 | 146 |
| business-finance | 25 | 143 |
| natural-sciences | 17 | 138 |
| manufacturing-production | 14 | 135 |
| hospitality-culinary | 19 | 128 |
| mind-self | 18 | 121 |
| energy-mining-utilities | 13 | 113 |
| media-communication | 17 | 109 |
| human-services | 13 | 104 |
| personal-care-services | 15 | 101 |
| social-sciences | 14 | 100 |
| languages-linguistics | 13 | 99 |
| mathematics | 14 | 99 |
| relationships-social | 15 | 96 |
| humanities | 15 | 86 |
| education-training | 10 | 68 |
| **total** | **586** | **51520** |
<!-- STATS:END -->

## Licence

Apache-2.0 for everything in this repository: skill text, methods, taxonomy and tools. See [`LICENSE`](LICENSE).
