---
id: computing-software.messaging-and-integration.celery.celery-task-design-best-practices
name: celery-task-design-best-practices
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-best-practices, ignore-results, sync-subtasks, delay-on-commit, race-conditions, granularity, django]
level: practitioner
status: docs-checked
description: "Avoid common Celery task design traps: stored results nobody reads, blocking on subtasks, passing model objects, transaction races (delay_on_commit), granularity, data locality."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: design tasks that are safe and efficient in a distributed setting.

## Ignore results you do not need
`@app.task(ignore_result=True)`, or globally `task_ignore_result`. Per call: `mytask.apply_async((1, 2), ignore_result=True)` and `.get()` then returns `None`. Precedence: global `task_ignore_result`, then the task `ignore_result` option, then the execution option. Default is to store results when a backend is configured.

## Do not wait on subtasks
Calling `.get()` inside a task is inefficient and may deadlock if the pool is exhausted. Use a chain:
```python
chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
chain()
```
Celery refuses synchronous subtasks by default; `.get(disable_sync_subtasks=False)` overrides it, but that is not recommended.

## Granularity
Prefer many smaller tasks over a few long ones so tasks do not block the worker, but too fine-grained tasks lose to message overhead.

## Data locality
Run workers close to the data; cache or preload data; a distributed cache such as memcached is the easiest way to share data between workers.

## State
Tasks must assert the world is as expected; for example, if a search index must be rebuilt at most every 5 minutes, the task enforces it, not the caller. Do not pass Django model objects as arguments: a queued task with an old copy overwrites newer edits. Pass the id and re-fetch inside the task:
```python
@app.task
def expand_abbreviations(article_id):
    article = Article.objects.get(id=article_id)
```
Smaller messages are also cheaper.

## Database transactions
Inside `@transaction.atomic`, a task can start before the commit and not find the row. Use `expand_abbreviations.delay_on_commit(article.pk)` (Celery 5.4+, wraps Django `on_commit`). Older: `transaction.on_commit(functools.partial(expand_abbreviations.delay, article.pk))`. `on_commit` needs Django 1.9+.

## Workers need identical code
Only the task name is sent, so keep workers on the same software version as the client.

## Checked

2026-11-07. Re-read the cited page(s) (tasks) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Changed: removed an unconfirmed version tag on the per-call ignore_result option.

Method: documentation only; no commands were run.
