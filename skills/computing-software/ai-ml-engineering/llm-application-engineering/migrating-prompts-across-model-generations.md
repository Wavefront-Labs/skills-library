---
id: computing-software.ai-ml-engineering.llm-application-engineering.migrating-prompts-across-model-generations
name: migrating-prompts-across-model-generations
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, prompt-migration, model-migration, prompt-regression, model-upgrade, claude-api]
level: practitioner
status: docs-checked
description: "Move prompts and code to a new model generation safely: API breaking changes, removing dated prompt cruft, effort/thinking re-tuning, eval-gated rollout and rollback."
sources:
  - https://docs.claude.com/en/docs/about-claude/models/migrating-to-claude-4
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
  - https://docs.claude.com/en/docs/about-claude/model-deprecations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating prompts across model generations

**Reality:** a new model is a new dependency version. Prompts tuned for the old one can get worse, and request shapes can break.

## 1. API surface changes (fix before evaluating)
Read the provider's migration notes. Recent Claude examples:
- Prefilled assistant messages on the last turn return a 400 error starting with Claude 4.6 models; the best-practices page lists migrations per prefill use case (structured outputs for format forcing, clearer prompting for refusals, context reminders in the user turn).
- Extended thinking with `budget_tokens` is deprecated on Opus 4.6 and Sonnet 4.6 and returns a 400 error on Claude 4.7 and later; use adaptive thinking and control depth with the effort setting (see the per-model configuration table).
- Check each model's section of the best-practices page for other changed request or response behaviour before evaluating.

## 2. Prompt cruft to remove
- Aggressive language ("CRITICAL: You MUST use this tool when...") written to cure undertriggering: Opus 4.5 and 4.6 are more responsive to the system prompt and may now overtrigger; plain wording ("Use this tool when...") is the documented fix.
- Prompts that told the model to be more thorough: Opus 4.6 explores more up front, so tune that guidance down or lower effort.
- Workarounds for old bugs (JSON repair instructions, prefill tricks).
- Keep: domain facts, output contracts, safety rules, examples that define style.

## 3. Re-tune knobs
- Effort calibration differs by model: sweep effort levels on your eval, and lower effort if the model thinks more than you want.
- Output length and verbosity often change (the best-practices page has a communication style and verbosity section); adjust instructions or `max_tokens`.
- Re-baseline cost with token counting on the new model.

## 4. Eval-gated rollout
1. Run the full eval on old vs new (same prompts), then on new with migrated prompts.
2. Review diffs on failures, not just aggregate scores.
3. Shadow or canary a small traffic share; compare user-facing metrics.
4. Keep the old model ID and prompt version deployable for rollback until the new one is stable.

## Verify
- [ ] Migration PR lists API changes, prompt edits, eval results per slice, and the rollback plan.

## Checked
2026-11-01. Confirmed on the Claude prompting best-practices page: prefill 400 error from Claude 4.6, `budget_tokens` deprecated on Opus/Sonnet 4.6 and 400 on 4.7 and later, adaptive thinking and effort, softening aggressive tool language, Opus 4.6 up-front exploration. Removed: model ids, forced `tool_choice` 400 claim, sampling-param claim, default effort claim, `refusal` stop-reason claim, step-script claim.
Method: documentation only; no commands were run.
