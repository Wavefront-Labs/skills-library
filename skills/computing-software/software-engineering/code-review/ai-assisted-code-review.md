---
id: computing-software.software-engineering.code-review.ai-assisted-code-review
name: ai-assisted-code-review
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, review-process, ai-code-review, llm, copilot-code-review, review-bots, human-in-the-loop]
level: practitioner
status: draft
description: "Use AI-assisted code review responsibly: where LLM reviewers help, configuring repo guidance, triaging false positives, security and privacy limits, and keeping humans accountable."
sources:
  - https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review
  - https://docs.anthropic.com/en/docs/claude-code/github-actions
  - https://docs.gitlab.com/user/project/merge_requests/duo_in_merge_requests/
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AI-assisted code review

LLM reviewers (GitHub Copilot code review, Claude Code GitHub Actions, GitLab Duo, CodeRabbit, Qodo and others) read a diff and leave comments. Treat them as a fast first-pass reviewer, not an approver.

## Where they help
- Catching obvious bugs: null handling, off-by-one, unhandled errors, resource leaks, wrong variable used.
- Consistency with nearby code, missing tests for new branches, outdated docs/comments.
- Summarising large PRs for human reviewers; explaining unfamiliar code.
- Applying repo-specific rules written in plain language.

## Where they are weak
- Business intent and product correctness ("is this the right behaviour?").
- Cross-system effects not visible in the diff (callers in other repos, data migrations, deployment order).
- Confident false positives and hallucinated APIs; style opinions that contradict the codebase.
- Security assurance: useful hints, but not a replacement for SAST, threat modelling, or security review.

## Setup
- **Repo guidance file:** give the reviewer the project's standards (GitHub `.github/copilot-instructions.md`; Claude Code `CLAUDE.md`; tool-specific config). Include architecture boundaries, error-handling conventions, things to ignore (generated code, formatting).
- Scope: run on ready-for-review PRs, skip drafts and generated/lock files; limit comment volume (summary plus top findings) to avoid noise fatigue.
- Ask for severity labels and concrete fixes; suppress pure style comments (formatters handle those).
- Make AI comments non-blocking; required approval stays human (branch protection unchanged).

## Triage discipline
- Authors resolve each AI comment explicitly: fix, or dismiss with a short reason. Track the false-positive rate; tune instructions or disable categories that are mostly noise.
- Reviewers still read the diff; an AI "looks good" never substitutes for review. The approving human is accountable.

## Security and privacy
- Know where code is sent and retained; use enterprise agreements with no training on your code; respect data residency.
- **Prompt injection:** PR content (comments, docs, test data) can contain instructions aimed at the AI. Run AI reviewers with least privilege (read-only tokens, no secrets in the environment, no ability to merge or push to protected branches), especially on PRs from forks.
- Do not paste secrets or customer data into chat-based review tools.

## Measuring value
Compare before/after: time to first review, defects caught pre-merge vs escaped, reviewer time per PR, and the proportion of AI comments acted upon.

## Verify
- [ ] Branch protection still requires human approval; AI reviewer token cannot approve or merge.
- [ ] Guidance file exists and is reviewed when conventions change; false-positive rate tracked monthly.
