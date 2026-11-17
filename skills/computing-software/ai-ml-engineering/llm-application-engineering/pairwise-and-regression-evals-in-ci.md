---
id: computing-software.ai-ml-engineering.llm-application-engineering.pairwise-and-regression-evals-in-ci
name: pairwise-and-regression-evals-in-ci
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-evaluation, pairwise-evaluation, eval-regression-ci, llm-as-judge, position-bias, promptfoo]
level: practitioner
status: docs-checked
description: "Compare prompt/model versions with pairwise judging (position swapping, win rates with CIs) and run LLM regression evals in CI with thresholds, caching and cost limits."
sources:
  - https://arxiv.org/abs/2306.05685
  - https://www.promptfoo.dev/docs/integrations/github-action/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pairwise comparison and regression evals in CI

**Goal:** every prompt, model or retrieval change is evaluated automatically, and you can tell "better" from "noise".

## Pairwise judging
For open-ended outputs, "which is better, A or B?" is commonly more reliable than absolute 1-10 scores (practitioner advice).
- **Known judge biases:** the MT-Bench / Chatbot Arena paper (Zheng et al.) examines position, verbosity and self-enhancement biases and limited reasoning ability in LLM judges, and reports that strong judges such as GPT-4 reached over 80% agreement with human preferences, the same level as agreement between humans.
- **Mitigations (practitioner advice; the abstract says the paper proposes some, details not read):** run each pair twice with order swapped and count a win only if consistent, otherwise a tie; instruct against favouring length and check win rate by length difference; use a different model family as judge where possible; validate against human labels on a sample.
- Report **win rate with a confidence interval** (bootstrap over cases or binomial CI). 54% on 100 cases is not a significant win.

## Regression suite in CI
Pipeline on every PR touching prompts, tools, retrieval or model config (practitioner pattern):
1. Run the golden set through the candidate; cache LLM responses by input hash + config to avoid paying twice for unchanged cases.
2. Grade: deterministic checks first (schema, contains/not-contains, citations exist), then judges.
3. Compare with the baseline (main branch results stored as an artifact).
4. Fail the build on: any must-pass case failing, aggregate score drop beyond a threshold, latency/cost regression beyond budget.
5. Post a summary table to the PR.

### promptfoo GitHub Action (from its docs)
- `promptfoo/promptfoo-action@v1` runs a before vs. after evaluation on pull requests that modify prompt files. The workflow triggers on `pull_request` with `paths` (for example `prompts/**`) and needs `pull-requests: write` permission to post results.
- Inputs: `github-token`, `prompts` (glob of prompt files) and `config` (path to the promptfoo config) are required; `openai-api-key` and `cache-path` are optional. Check the docs for the current Node.js version requirement on the runner.
- Caching: the action caches LLM requests and outputs (for example with `actions/cache` on `~/.cache/promptfoo`) to save cost and time on later runs.
- Results are posted to the PR, with a link to the web viewer for before/after comparison.

## Handling nondeterminism (practitioner advice)
- Temperature 0 does not guarantee identical outputs; for flaky cases run 3 samples and require 2/3.
- Separate "must-pass" (deterministic, critical) from "scored" cases; only must-pass cases block individually.

## Cost control (practitioner advice)
Cap cases per PR (smoke set) and run the full suite nightly or before release; use cheaper judges where they agree with the expensive one.

## Verify
- [ ] Judge agreement with human labels measured (a common bar is about 80% on a sample) before trusting it.
- [ ] CI posts a baseline-vs-candidate table on PRs.
- [ ] Win rates reported with CIs and swapped-order consistency.

## Checked
Method: docs-checked 2026-11-09 against the arXiv abstract page for 2306.05685 (full paper not read) and the promptfoo GitHub Action page (read in full). Dropped: the LangSmith and OpenAI evals sources (not read), the specific promptfoo assertion types (not on the page read), and "judges favour the first answer" as a stated finding (the abstract names position bias only). CI pipeline, thresholds and cost-control sections are practitioner guidance.
