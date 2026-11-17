---
id: computing-software.ai-ml-engineering.llm-application-engineering.writing-clear-and-direct-prompt-instructions
name: writing-clear-and-direct-prompt-instructions
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, clear-instructions, prompt-engineering, system-prompts, context, claude]
level: practitioner
status: docs-checked
description: "Write prompts a capable new colleague could follow: task context, audience and success criteria, ordered steps, positive instructions with reasons, and output format."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
  - https://platform.openai.com/docs/guides/prompt-engineering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Clear and direct instructions with context

**Goal:** the model does the intended task on the first try because the prompt says what, why, for whom and in what form - not because of magic phrases.

## The colleague test
Show the prompt to a smart colleague with no project context. If they would ask questions before starting, the model will guess. Answer those questions in the prompt.

## What to include
1. **Purpose and audience:** "These summaries go to on-call engineers deciding whether to page a second responder within 2 minutes."
2. **Context the model cannot know:** product names, definitions, internal policies, what has been tried.
3. **The task, specifically:** "Summarise the incident timeline in at most 5 bullets, then state severity (SEV1-SEV4) with one sentence of justification."
4. **Steps when order matters:** numbered list.
5. **Success criteria and edge cases:** what to do when data is missing, conflicting or out of scope ("If the log has no error lines, say 'No errors found' and stop").
6. **Output format:** exact structure; for machine consumption use structured outputs rather than prose instructions.

## Phrasing that works
- Say what to do, not only what to avoid: "Write in flowing paragraphs" beats "Don't use bullet points".
- Give the reason: "Never use ellipses because a text-to-speech engine reads this" lets the model generalise.
- Calibrate emphasis: current models follow instructions closely; ALL-CAPS "CRITICAL / MUST" often causes over-application. Use normal emphasis and reserve strong wording for true invariants.
- Ask explicitly for the level of effort or scope you want ("Include as many relevant features as possible" vs "minimal change only") - modern models do what is asked, not more.
- Separate instructions, context and data with XML tags or headings so the model does not treat document text as instructions.

## Example
Weak: `Summarize this ticket.`
Strong:
```
You triage support tickets for a B2B billing product. Agents read your summary to decide routing.
<ticket>{ticket}</ticket>
Write:
1. One-sentence problem statement in the customer's terms.
2. Category: one of billing_error, refund_request, access_issue, other.
3. Facts the agent must verify (amounts, dates, invoice ids) as a list.
If the ticket mixes several issues, summarise the one the customer asks to resolve first and mention the others in one line.
```

## Iterate with evidence
Change one thing at a time and re-run a small eval set of real cases. Keep a log of prompt versions and scores; prompts drift into contradictory rule piles without it.

## Checked
2026-11-01. Confirmed against Anthropic's prompt-engineering guide: the colleague test, text-to-speech ellipses example, flowing-prose example, softening CRITICAL/MUST language, XML tags to separate content types. Removed the eval-set size. The OpenAI guide was not used.
Method: documentation only; no commands were run.

## Verify
- [ ] Prompt states purpose, audience, task, edge-case handling and format.
- [ ] No contradictory or stale rules (read it top to bottom).
- [ ] Eval score recorded for the current version.
