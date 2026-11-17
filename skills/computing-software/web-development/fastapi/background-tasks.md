---
id: computing-software.web-development.fastapi.background-tasks
name: background-tasks
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, background-tasks, add-task, after-response, celery]
level: practitioner
status: docs-checked
description: "Run work after the FastAPI response is sent with BackgroundTasks and add_task, including use in dependencies and when to choose Celery instead."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/background-tasks.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Background tasks

Goal: do slow work (email, file processing) after returning the response.

## Method
- Declare a parameter typed `BackgroundTasks` in the path operation function; FastAPI creates and passes it.
- The task is a plain function; `def` or `async def` both work.
- Call `background_tasks.add_task(func, arg1, kw="value")`: first the function, then positional args, then keyword args.
- `BackgroundTasks` also works in dependencies and sub-dependencies. FastAPI reuses one object, so all tasks merge and run after the response.
- Import from `fastapi`, not `starlette.background.BackgroundTask` (no `s`). That one needs you to build it and return a Starlette `Response` containing it.

## When not to use
For heavy computation that need not share memory with the app, or must run in other processes or servers, use a bigger tool like Celery (needs a queue such as RabbitMQ or Redis). For small jobs using the app's own objects, BackgroundTasks suffices.

## Verify
Hit the endpoint; the response returns first, then the task output (e.g. a log file line) appears.

## Checked

Confirmed on the cited FastAPI background-tasks tutorial page: the `BackgroundTasks` parameter, `def` or `async def` task functions, `add_task` arguments, dependency and sub-dependency use with merged tasks, the Starlette `BackgroundTask` note and the Celery caveat. Removed (not stated on the page): the claim that tasks run after all middleware and after yield-dependency exit code.

Method: docs-only read of cited pages, 2026-11-08
