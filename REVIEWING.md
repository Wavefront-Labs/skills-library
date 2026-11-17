# Reviewing skills (and proving you did)

Anyone can help check skills, with their own agent or by hand. A review is submitted as an **attestation**: a small
JSON file that records what was checked, against what, and what was found. CI checks the attestation for you; a
maintainer decides whether the skill is promoted. An attestation never changes a skill's `status` by itself.

## What a review is (protocol `docs-check/1`)

1. Pick a skill whose `status` is `draft`. Note its `version`.
2. For every concrete claim in it (command, flag, setting, number, behaviour), find the page in `sources:` that says
   so. Read the page; do not answer from memory.
3. Record each claim as `confirmed`, `contradicted`, `unverifiable` (no source says it) or `gated` (source is
   paywalled or blocked). For `confirmed` and `contradicted`, copy the sentence from the source that proves it
   (`evidence_quote`).
4. List every claim you checked and say how you chose them (`coverage`): "every command and flag" is the bar.
5. Verdict: `pass` only if nothing is contradicted and nothing material is unverifiable.
6. If something is wrong, fix it in a separate PR (bump `version`) or describe it in `suggested_edits`.

## Make the file

```
python tools/attest.py template <skill-id> --github <your-handle> > reviews/<skill-id>/<date>-<handle>.json
```

The template fills in the skill's hash and its listed sources. Fill in the rest (schema:
[`schemas/attestation.schema.json`](schemas/attestation.schema.json)), then:

```
python tools/attest.py seal  reviews/<skill-id>/<date>-<handle>.json     # writes attestation_sha256
python tools/attest.py check reviews/<skill-id>/<date>-<handle>.json --refetch
```

Open a pull request containing only that file. `reviewer.github` must be the PR author.

## What CI checks

| Check | What it catches |
|---|---|
| Skill hash matches the current file | review of an old or different version |
| Every `claim` appears verbatim in the skill | claims invented or reworded to fit |
| Every confirmed or contradicted claim names a listed source and a quote | evidence left out |
| With `--refetch`: every `evidence_quote` appears in the page as fetched today | fabricated evidence |
| Seal matches | edits made after sealing |
| `reviewer.github` equals the PR author | attestations submitted under someone else's name |

## What a maintainer still does

Reads the verdict, spot-checks a random sample of claims by hand (about one in five attestations), and promotes
the skill's `status` in a separate commit. Reviewers whose spot-checks fail stop being accepted.

## What this does and does not prove

The hash and seal show the file was not altered after sealing, and was made against this exact version of the
skill. They do not show that an agent ran the review honestly: anyone can compute a hash. What makes it hard to
fake is the re-fetch (quotes must exist in the real source), the verbatim claim check, and the human spot-check.
Pages change and some block automated fetches, so a failed re-fetch is a flag for a maintainer, not a verdict.
An agent or model name in the file is self-reported.
