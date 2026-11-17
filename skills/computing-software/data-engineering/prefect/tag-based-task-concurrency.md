---
id: computing-software.data-engineering.prefect.tag-based-task-concurrency
name: tag-based-task-concurrency
category: computing-software
field: data-engineering
product: prefect
tags: [tag-concurrency, tags, slots, task-runs, limits]
level: practitioner
status: docs-checked
description: "Cap concurrent Prefect task runs per tag: how limits are checked, the zero limit, the retry wait setting and the backing global limit name."
sources:
  - https://docs.prefect.io/v3/concepts/tag-based-concurrency-limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: limit how many task runs with a tag are `Running` at once.

Facts:
- Each tag-based limit is backed by a global concurrency limit named `tag:{tag_name}` (Prefect 3.4.19+), which can show in the UI or API.
- A task with several tags runs only if all its tags have capacity.
- Tags without a limit are unlimited.
- A limit of `0` aborts immediately any task run with that tag rather than delaying it.
- Limits are checked whenever a task run tries to enter `Running`.
- When slots are full the transition is delayed and the client is told to retry after 30 seconds by default. Change the wait with `PREFECT_SERVER_TASKS_TAG_CONCURRENCY_SLOT_WAIT_SECONDS`.

Compared with global concurrency limits: those are a general mechanism for any Python operation; tag limits are specific to Prefect tasks, though both can achieve similar outcomes.

Use cases the page lists:
- database connections: tag tasks `database` and set the limit to the allowed connection count (the example is 10)
- API rate limiting: tag tasks that call an external API
- resource contention: limit memory-intensive tasks

The concept page does not show the CLI or code for creating the limit.

## Checked
2026-11-08. Confirmed against the tag-based concurrency limits concept page: backing global limit named tag:{tag_name} from 3.4.19, all-tags rule, unlimited without a limit, zero limit aborts, check on entering Running, 30 second retry and the PREFECT_SERVER_TASKS_TAG_CONCURRENCY_SLOT_WAIT_SECONDS setting, and the three use cases. Removed the pointer to a how-to guide that was not read.
Method: documentation only; no commands were run.
