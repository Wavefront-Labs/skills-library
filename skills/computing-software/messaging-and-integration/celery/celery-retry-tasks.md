---
id: computing-software.messaging-and-integration.celery.celery-retry-tasks
name: celery-retry-tasks
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-retry, task-retry, autoretry-for, retry-backoff, retry-jitter, max-retries, python]
level: practitioner
status: docs-checked
description: "Retry Celery tasks with self.retry, countdown and default_retry_delay, or automatically via autoretry_for with exponential backoff, jitter and max_retries."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: re-run a task after recoverable errors, manually or automatically.

## Manual retry
```python
@app.task(bind=True)
def send_twitter_status(self, oauth, tweet):
    try:
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
        raise self.retry(exc=exc)
```
- `retry` sends a new message with the same task id to the same queue, and records a `RETRY` state.
- It raises the `Retry` exception, so code after it is not reached; this is normal unless the `throw` argument is False.
- `exc` supplies exception info for logs and stored results. When `max_retries` is exceeded the current exception is re-raised; if no `exc` was given, `MaxRetriesExceededError` is raised; if no current exception exists, `exc` itself is raised.
- `max_retries` defaults to 3; `None` retries forever. Retry is never automatic unless you call `self.retry` or use `autoretry_for`.
- Delay: `default_retry_delay` (default 3 minutes, in seconds, int or float) or `countdown=60` on the call:
```python
@app.task(bind=True, default_retry_delay=30 * 60)
def add(self, x, y):
    try: something_raising()
    except Exception as exc: raise self.retry(exc=exc, countdown=60)
```

## Automatic retry (4.0)
```python
@app.task(autoretry_for=(FailWhaleError,), retry_kwargs={'max_retries': 5})
def refresh_timeline(user): return twitter.refresh_timeline(user)
```
Use `autoretry_for=(Exception,)` to retry on any error. `retry_kwargs` are passed to the internal `retry` call.

## Exponential backoff (4.2)
`retry_backoff=True` delays 1, 2, 4, 8 seconds...; a number is a factor (3 gives 3, 6, 12, 24). Default is `False`. `retry_backoff_max` caps the delay (default 600 seconds). `retry_jitter` (default `True`) treats the computed delay as a maximum and picks a random value between zero and it. Since 5.3, `dont_autoretry_for` lists exceptions excluded from `autoretry_for`.

These options can also be class attributes on a Task subclass (4.4): `autoretry_for`, `max_retries`, `retry_backoff`, `retry_backoff_max`, `retry_jitter`.

Since 5.7 retries preserve an `ignore_result` override passed to `apply_async` or `send_task`.

## Checked

2026-11-07. Re-read the cited page(s) (tasks) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Changed: reworded the throw wording to match the page.

Method: documentation only; no commands were run.
