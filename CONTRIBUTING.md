# Contributing to the Wavefront Skills Library

You are adding to a catalogue of human expertise meant to scale to 100k+ skills, written
for people and for agents alike. Follow this exactly. Inconsistency is the only thing that breaks a library this
size. If in doubt, match what already exists.

## The golden rules
0. **Search before you add.** Grep `skills.index.jsonl` for the capability, its
   synonyms and the tool name. If a skill already covers it, improve that file
   instead of adding a near-duplicate. Duplicates are the main way a library this
   size rots.
1. **One skill = one file** at `skills/<category>/<field>/<product>/<name>.md`.
2. **Write skills from VERIFIED behaviour, never guessed.** If you haven't done it
   or can't cite it, mark `status: draft` and say what's unconfirmed. A skill the
   reader can't act on correctly is worse than no skill.
3. **Tags + description are the search surface.** A skill nobody can find by tag
   does not exist. Tag generously and specifically (tools, techniques, synonyms,
   exact names like `rhubarb`, `kokoro`, `ffmpeg`).
4. **Never hand-edit or commit generated files**: `skills.index.jsonl` and every
   `INDEX.md` are git-ignored and rebuilt by `reindex`.
5. **Always finish with lint + reindex** (see Workflow). CI rejects anything that
   fails lint.
6. **Ids are permanent.** Never rename or move a merged skill without putting its old
   id in `aliases` (see SCHEMA.md). Any change to a merged skill bumps `version` and
   sets `updated`.
7. **One session, one worktree.** Several sessions may write skills at once. Never
   edit in a checkout another session uses: make your own worktree (see Workflow).

## Contributing from outside (pull requests)
Fork the repository, make a branch, and follow the Workflow below (a worktree is optional
when you are the only one working in your clone). Then open a pull request against `main`.

- One skill, or one coherent change, per pull request.
- New skills land as `status: draft`. Write from verified behaviour, say what is unconfirmed,
  and list your `sources`. A maintainer reviews the PR, may edit it for consistency with the
  rest of the library, and promotes the status once the claims have been checked.
- `python tools/lint.py` must pass; CI runs it on every pull request.
- By submitting, you agree your contribution is licensed under Apache-2.0 like the rest of
  the library. Add `Signed-off-by: Your Name <you@example.com>` to your commits
  (`git commit -s`) to say so.
- Not sure where a skill belongs or whether it already exists? Open an issue first with the
  one-line description; placement questions are quick to answer.

## Workflow (every contribution)
```bash
# 0. once per clone: tools need PyYAML; hooks rebuild the git-ignored indexes
pip install -r requirements.txt && git config core.hooksPath .githooks
# 0b. every task: your own worktree and branch, never a shared checkout
git fetch && git worktree add ../skills-library-<task> -b <branch> origin/main && cd ../skills-library-<task>
python tools/reindex.py   # build the indexes in the new worktree
# 1. search first (rule 0), then scaffold at the right path
python tools/new_skill.py <category> <field> <product> <name> "one-line description"
# 2. write the body (the actual craft/knowledge) and fill tags + description
# 3. validate + rebuild (and check you bumped versions / kept ids)
python tools/lint.py --changed-since origin/main && python tools/reindex.py
# 4. commit (see Commit convention)
```

## Choosing the path (taxonomy decision guide)
Pick the most specific existing branch; only create a new one when nothing fits.
- **category** (tier 1) — broad domain of human endeavour. MUST be one of the
  canonical categories in `SKILLS.md` (anchored to O*NET + academic disciplines).
  Do not invent a new category without good reason; if you must, add it to the
  canonical list in `SKILLS.md` in the same commit.
- **field** (tier 2) — the discipline or profession, e.g. `animation`, `cardiology`,
  `structural-engineering`. Prefer the name a practitioner would use.
- **product** (tier 3) — an **application** (a specific tool: `blender`, `photoshop`,
  `react`, `autocad`, our own `vectorcraft`) OR a **craft** (tool-agnostic know-how:
  `echocardiography`, `load-bearing-walls`, `screenwriting`).
  **Never a project.** What you learn building something (a film, an app, a client
  job) goes into the application or craft skill it is really about; the project can
  appear only as a worked example. A Photoshop-class technique learned in our own
  `photocraft` tool is still useful to Photoshop, GIMP and Krita users: write it under
  the tool you used, and tag the equivalents (`photoshop`, `gimp`, `krita`,
  `raster-editor`) so their users find it.
- **name** — the single capability, kebab-case (`cel-shading`, `reading-an-echo`).

When unsure between two branches, grep `skills.index.jsonl` for siblings and follow
the pattern already established.

## The skill file (see SCHEMA.md for the full contract)
Required frontmatter: `id, name, category, field, product, tags, level, status,
description`. Rules enforced by `tools/lint.py`:
- path segments and `name` are lowercase-kebab-case;
- `category`/`field`/`product`/`name` MUST equal the folder path;
- `id` = `<category>.<field>.<product>.<name>`, unique;
- `description` ≤ 200 chars, one line, quoted, concrete (it shows in search results);
- `category` is in the canonical list in `SKILLS.md`;
- `tags` ≥ 1, lowercase;
- `level` ∈ {intro, practitioner, advanced, sme}; `status` ∈ {stub, draft, unreviewed-low-risk, gated, verified}. `unreviewed-low-risk` = tier "low" by `tools/triage.py` (no checkable specifics), no agent review yet. `gated` = checked as far as free sources allow, paywalled parts carry the marker `(gated: unconfirmed, source is paywalled or blocked)`. `verified` = every concrete claim fetched, run or computed.

Body: whatever makes the reader able to DO the thing — exact commands/flags, API
calls, node graphs, settings, numbers, failure modes, and a short self-check.
Link related skills by their `id` in prose when useful.

## Methods (recipes): the second genre of file

Skills are **ingredients**; a method is the **recipe**. A skill says how to do one
thing well. A method says *which skills to bundle, in what order, and to what
measured standard*, to produce a specific outcome at a specific quality tier.

A library of ingredients alone makes you re-derive the meal every time. That is the
gap methods close.

**Methods are ordinary skill files** — same path, same frontmatter, same lint. They
are NOT a separate tree and NOT a new frontmatter type. Two reasons: `tools/reindex.py`
emits a fixed field list, so an invented key (`kind:`) would never reach search while
`tags` do; and a parallel section would have to be duplicated under every field and
would fork lint, CI and the API. Deciding the plan for an outcome is itself expert
work, so it passes the library's own test for what a skill is.

### The convention
- **Path:** a dedicated **tier-3 product named `methods`** inside the field:
  `skills/<category>/<field>/methods/<outcome>.md`. One `methods` product per field,
  created only when that field has a recipe worth writing.
- **Why tier 3, not a tier-4 file inside an existing product.** A recipe is
  tool-agnostic know-how (a craft), and most fields have no single craft product that
  could host it — a cooking field has `knife-skills` and `sauces`, and a
  beef-wellington recipe belongs in neither. Putting methods at tier 3 keeps them in
  the same place in every field, which matters when recipes are swept across all
  areas; hiding them inside whichever product seemed closest does not scale.
- **Filename:** the outcome and its tier, e.g. `stylized-series-tier.md`. No
  `method-` prefix — the `methods` product already says what it is.
- **Tags:** MUST include `method` and `recipe` (this is how they are found — grep
  `skills.index.jsonl` for `"method"`), plus the outcome and tier.
- **Status:** `verified` only if the method has been executed end to end. A method
  whose conclusion is "do not attempt this tier, here is the arithmetic" may be
  `draft` while the negative conclusion itself is verified — say so in the body.

### Required shape
1. **Outcome** — what this produces, in one paragraph.
2. **Ingredients** — a table of the component skill `id`s, by phase. This is the
   bundling, and it is the point of the file.
3. **Ordering law** — why this order (usually dependency, not importance).
4. **Phases** — each with its skills and an explicit **Gate**: the measurable
   condition for moving on. Prefer numbers over impressions.
5. **Acceptance criteria** — how you know the outcome hit the tier.
6. **Failure modes** — what this method exists to prevent.
7. **Verify** — as for any skill.

### The rule that keeps the two genres apart
**A method owns no technique of its own.** Every "how" is a link to a skill id. If
you catch yourself explaining a technique inside a method, that content belongs in a
skill — write or update the skill and link it. Conversely, if a skill starts
dictating what to do before and after itself, that ordering belongs in a method.

Reference implementations:
`creative-arts.animation.methods.stylized-series-tier` (a tier to aim at) and
`creative-arts.animation.methods.feature-cg-tier` (a tier to refuse, with the
arithmetic). Copy their shape.

## Make it findable (retrieval)

A consumer's agent will usually find a skill from how a person *phrases a job*, not from the
skill's own jargon. Measured 9 Nov 2026 on 24 blind phrasings of one method: keyword matching found
it in the top 3 only 29% of the time, semantic search 79%. So:

- Write `description` (<= 200 chars) and `tags` in the words a person would use, including
  synonyms: a retirement method needs *retire, sunset, wind down, decommission, mothball, tear
  down, shut down*, not just the one verb the author happened to pick.
- For a method, say when to use it ("Use when winding down a service") in the description.
- Test with `tools/retrieval_eval.py` and a **blind** query set (queries written by someone who
  has not read the skill). Queries you write yourself after reading the skill only measure your
  own vocabulary. Query sets live in `eval/queries/`.

## Writing a good skill (quality bar)
- Lead with the goal in one line, then the method.
- Be specific and runnable: exact commands, versions, parameters — not "use the X tool".
- Capture the non-obvious: the gotcha, the calibration, the thing that bit you.
- End with a verification step (how to know it worked).
- `verified` only if you actually confirmed it; else `draft` with the gap named.

## Commit convention
- Branch from `main` in your own worktree, open a PR (CI must pass: lint, the
  `--changed-since` id/version check, and the serve self-test).
- Message: `add <category>/<field>/<product>/<name>` or `update <id>: <what changed>`.
- Normal prose in the body (not telegraphic). Never commit the generated manifest or
  `INDEX.md` files (they are git-ignored).

## Content you must not put in a skill
This library is public under Apache-2.0, so every skill must be safe to show a stranger
and free of anything we have no right to publish.
- **No secrets.** No API keys, tokens, passwords, connection strings or private URLs.
  Use placeholders like `<API_KEY>` and say where the real value comes from.
- **No personal or client data.** No names, emails, addresses, account numbers or
  anything identifying a client, employer or project that isn't public. Generalise
  the lesson ("a 30fps episode pipeline") instead of naming the project.
- **No machine-specific paths** like `C:\Users\<you>\...`. Use relative paths or
  `<PROJECT_ROOT>`.
- **Write it yourself; don't copy.** Paraphrase vendor docs, books, courses and
  forum answers in your own words and list them in `sources:`. Short quotes are fine.
  Do not paste copyrighted text, code under a licence incompatible with Apache-2.0, or
  paywalled material: we cannot publish it.

## Coverage specs (how we know a subject is complete)
"Every product has a skill" is a floor, not completeness. For a subject that needs to be
*complete*, add `taxonomy/coverage/<category>.<field>.<product>.yaml`: a scope and a list of
canonical topics taken from **external** structures (certification blueprints, the official
docs table of contents, SIG/working-group lists), each with `match` keywords. Never derive the
topic list from the skills we already have — the point is to measure the library against the
subject, not against itself.

- `python tools/coverage_check.py` reports covered/GAP per topic (CI runs it; gaps don't fail
  PRs). `--strict` exits 1 on gaps; `--markdown` prints the issue body.
- A topic is covered when an in-scope skill has a tag equal to a keyword or the keyword appears
  in its id/name. Tag generously so the check can see your work.
- The scheduled `coverage` workflow opens/updates a `coverage-gap` issue with the gaps, and (when
  `ANTHROPIC_API_KEY` is set) asks Claude what the *spec itself* is missing, so the checklist
  grows too. Filling the gaps is agent work; editing the spec is a reviewed change.

### Depth

Breadth is "every canonical topic has a skill". Depth is "every task inside that topic has a skill". A topic may
carry `subtopics`, each with the same `id`/`name`/`match` shape, taken from the source's own sub-sections (a manual
page's headings, an exam objective's bullet list). `coverage_check.py` reports depth as the percentage of subtopics
with a matching skill. Target: at least 90% depth per subject before calling an area done.

```yaml
  - id: hpa
    name: Horizontal Pod Autoscaler
    match: [hpa, horizontal-pod-autoscaler]
    subtopics:
      - {id: hpa-custom-metrics, name: Scaling on custom and external metrics, match: [custom-metrics, external-metrics]}
      - {id: hpa-behavior, name: Scale-up/scale-down behaviour and stabilisation windows, match: [stabilization-window, scaling-behavior]}
```

## Do not
- Do not auto-surface skills via native `SKILL.md` here — it does not scale; this
  library is searched, not listed. Reserve `SKILL.md` for the rare always-on skill.
- Do not dump unverified bulk content as `verified`.
- Do not edit or commit generated files.
- Do not move or rename a merged skill without an alias, or change one without bumping `version`.
