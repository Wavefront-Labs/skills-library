# Connector skill

`wavefront-skills/` teaches an agent how to consult the library: when to search, how to phrase the query,
how to pick a method or skill, how many to fetch. It contains no library content. With the hook installed,
the lookup happens on every real prompt and before any web research, so the agent gathers what is already
known before reasoning it out.

It follows the Agent Skills open standard (a folder with `SKILL.md`; frontmatter `name` and `description`;
optional `scripts/`). The `description` is the trigger, so it is tested the same way methods are.

## Install (Claude Code)

1. Copy `wavefront-skills/` to `~/.claude/skills/` (or `.claude/skills/` in a project).
2. Point it at a library checkout: set `WAVEFRONT_SKILLS_LOCAL` to the repo path (user settings `env` block
   works). Run `python tools/reindex.py` in the checkout after pulling; the hook searches `skills.index.jsonl`.
3. Optional but recommended, the hook (`scripts/prompt_hook.py`): semantic search with a silence threshold,
   on `UserPromptSubmit` and on `PreToolUse` for `WebSearch|WebFetch`. It needs a Python with `fastembed` and
   `numpy`, and embeddings (`WAVEFRONT_SKILLS_EMB`): download the release file `skills-emb.npz` and run `python tools/retrieval_eval.py unpack skills-emb.npz --out <dir>` then `... embed --out <dir>`, or build them from scratch with `embed` alone (about 25 min).
   Settings snippets are in the script's docstring.

Other agents that read `SKILL.md`: put the folder where they load skills from; the script works the same.

## Files

- `wavefront-skills/SKILL.md`: the protocol the agent follows.
- `wavefront-skills/scripts/skills.py`: `find` and `get`, over a local checkout or a hosted instance.
- `wavefront-skills/scripts/prompt_hook.py`: the Claude Code hook.
- `CONTRACT.md`: the interface a hosted instance implements.
- `eval/`: retrieval and behaviour tests (`live_pilot.py`, `ab_test.py`).
