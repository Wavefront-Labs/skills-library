---
id: computing-software.ai-ml-engineering.langchain.langsmith-online-evaluators-and-monitoring
name: langsmith-online-evaluators-and-monitoring
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langsmith, online-evaluation, production-monitoring, feedback, automation-rules, annotation-queues]
level: practitioner
status: docs-checked
description: "Monitor LLM apps in production with LangSmith online LLM-judge evaluators and automation rules: filters, sampling, thread rules, backfill and retention."
sources:
  - https://docs.langchain.com/langsmith/online-evaluations-llm-as-judge
  - https://docs.langchain.com/langsmith/rules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LangSmith online evaluators and automation rules

**Goal:** know when production quality drops without waiting for complaints, and route bad traces to review or into datasets.

## Online LLM-as-a-judge evaluators
In the UI: Tracing, pick a tracing project (or agent environment), open the **Evaluators** tab, click **+ Evaluator**, then create an LLM-as-a-Judge evaluator from scratch, attach an existing one, or start from a template.

1. **Filter** which runs trigger it. Examples from the docs: runs with unsatisfactory user feedback, runs that invoke a specific tool call, runs matching metadata (such as a `plan_type`), or runs where another evaluator's score meets a condition (a chained evaluator, for example `correctness` below 0.5). The filter builder uses the same fields as trace filtering.
2. **Sampling rate** controls the percentage of filtered runs that trigger the evaluator; for example 0.1 evaluates 10 percent of traces, which helps control cost.
3. **Backfill:** in the Configure Evaluator panel choose Source (Runs or Threads), expand Advanced and toggle "Apply to past runs from date". Backfill is possible only when the rule is created and runs as a background job; progress is visible in the evaluator's Logs.
4. **Spend limit:** LLM cost per evaluator is capped weekly (an organization-wide default applies, org admins can override per evaluator); at the limit LangSmith pauses the evaluator until Monday 12AM UTC or the limit is raised.

Saving a custom LLM-as-a-judge evaluator in the UI saves its prompt to the prompt hub automatically (filter Prompts by "Used in Evaluators"). Prompt names look like `eval_<evaluator_name>_<8 random characters>`.

Other judge options: a decision model that returns typed answers recorded under separate feedback keys; multimodal traces can be mapped into the prompt via base64 content or attachments (template variables such as `{{attachment.file_name}}` or `{{attachments}}`). Multi-turn (thread-level) evaluators exist on a separate page.

## Automation rules
A rule is defined by an **item type** (Runs or Threads), a **filter**, a **sampling rate** and an **action**. Actions: add to annotation queue, add to dataset, trigger webhook, extend data retention (runs rules also support online and code evaluators). Examples from the docs: send traces with negative feedback to an annotation queue, send 10 percent of traces to a queue for spot checks, post low evaluator scores to a webhook, extend retention for errored traces.

- In the form the sampling rate is a percentage from 0 to 100; the API field `sampling_rate` takes a decimal from 0 to 1.
- Each rule runs on its own polling schedule, so a webhook rule may fire before an evaluator rule has scored a run. Use a feedback filter on the downstream rule (for example on the feedback key) to make the dependency explicit.
- Within one rule, actions run in this order: annotation queue, dataset, webhook, online evaluator, code evaluator, extend retention, alert.
- Apply a rule to past runs with "Apply to Past Runs" and a "Backfill From" date, at creation only.
- View rule logs from the Automations tab (Logs button).

### Thread rules
Item type Threads waits until a thread is idle (default 10 minutes, minimum 2, set per project and shared with multi-turn evaluators), then acts once on the whole thread. Allowed actions: add to annotation queue (thread item, rubric feedback only), add to dataset (one example per thread), trigger webhooks. Limits: only runs from the past 7 days are eligible and at most 500 threads per execution. Thread filters add Trace Count and Thread ID fields; other fields match if any trace in the thread matches.

## Retention side effects
An online evaluator or a rule with retention extension enabled upgrades matching traces to extended retention (higher cost). Defaults per action: add to dataset off, annotation queue on, webhook off. Online evaluator creators can opt out when the project default is base retention. A thread rule with the toggle on upgrades every trace in the thread.

## Verify
- [ ] An injected bad answer (in staging) receives a low online score and, via a rule, lands in the annotation queue.
- [ ] The evaluator's Logs show runs processed at roughly the sampling rate.

## Checked
Method: docs-checked 2026-11-09 against https://docs.langchain.com/langsmith/online-evaluations-llm-as-judge and https://docs.langchain.com/langsmith/rules (both read in full). Dropped the user-feedback code, dashboards and alerts, judge-drift and PII gotchas, and the annotation-queues source, none of which were confirmed from pages read.
