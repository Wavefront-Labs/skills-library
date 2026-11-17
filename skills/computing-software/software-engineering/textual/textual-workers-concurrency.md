---
id: computing-software.software-engineering.textual.textual-workers-concurrency
name: textual-workers-concurrency
category: computing-software
field: software-engineering
product: textual
tags: [textual, workers, work-decorator, concurrency, async, thread, exclusive, cancel]
level: practitioner
status: docs-checked
description: "Run slow Textual tasks without freezing the UI using run_worker or the work decorator, exclusive workers, thread workers, cancellation and worker state events."
sources: [https://textual.textualize.io/guide/workers/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual workers and concurrency

Goal: keep the UI responsive during network, subprocess or CPU-heavy work.

## Method

A message handler blocks the app's other messages until it returns, so slow work inside it makes input laggy. Run it as a worker instead.

- `self.run_worker(self.update_weather(city), exclusive=True)` schedules a coroutine in the background and returns a `Worker`.
- `exclusive=True` cancels all earlier workers first, so a late response for "Pari" cannot overwrite the one for "Paris".
- The `@work` decorator (from `textual`) takes the same arguments and turns a method into a function that starts a worker when called, with no `await`:

```python
@work(exclusive=True)
async def update_weather(self, city: str) -> None:
    ...
```

- Result: `worker.result` is `None` until completion. `await worker.wait()` waits but blocks that handler. Prefer worker events.
- Cancel with `Worker.cancel`; this raises `CancelledError` inside a coroutine.
- Errors: by default an exception exits the app and shows the traceback. Pass `exit_on_error=False` to `run_worker` or `@work` to prevent that.
- Lifetime: `app.workers` lists workers. Workers are tied to the node that created them, so removing the widget or popping the screen cleans them up; exiting cancels all. `worker.state` is a `WorkerState`: PENDING, RUNNING, CANCELLED, ERROR (see `worker.error`) or SUCCESS (see `worker.result`).
- Events: a worker sends `Worker.StateChanged` to its node; handle with `on_worker_state_changed(self, event: Worker.StateChanged)`.
- Threads: for non-async APIs use `thread=True`, with a regular function:

```python
@work(exclusive=True, thread=True)
def update_weather(self, city: str) -> None:
    worker = get_current_worker()
    ...
    if not worker.is_cancelled:
        self.call_from_thread(weather_widget.update, weather)
```

  `get_current_worker` is in `textual.worker`.

## Gotchas

- In thread workers do not call UI methods or set reactives directly; use `App.call_from_thread`. `post_message` is thread-safe; for many UI updates post custom messages.
- Threads cannot be cancelled like coroutines; check `worker.is_cancelled`.
- `@work` on a regular function without `thread=True` raises an exception.

## Checked
2026-11-07. Read in full: Workers guide. Confirmed: run_worker and exclusive, @work decorator and its arguments, worker.result and wait, Worker.cancel and CancelledError, exit_on_error=False, app.workers, node-tied lifetime, WorkerState values, Worker.StateChanged, thread=True, call_from_thread, get_current_worker, post_message thread-safe, exception for @work without thread=True. Removed: the Verify section (the --dev run command is a docs example, not a result).
Method: documentation only; no commands were run.
