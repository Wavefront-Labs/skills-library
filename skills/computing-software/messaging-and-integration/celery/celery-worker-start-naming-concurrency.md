---
id: computing-software.messaging-and-integration.celery.celery-worker-start-naming-concurrency
name: celery-worker-start-naming-concurrency
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-worker-start, celery, worker, hostname, concurrency, multi, logfile, prefork]
level: practitioner
status: docs-checked
description: "Start Celery workers, name multiple nodes with %h/%n/%d, size concurrency, and use per-process log and pid file variables."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Start, name and size Celery workers

Goal: run one or more named workers on a host with sane concurrency and per-node file paths.

Start in the foreground: `celery -A proj worker -l INFO` (`celery worker --help` lists options). For production use a daemonization tool, not the foreground command.

Several workers on one machine each need a unique node name via `-n/--hostname`:

```console
$ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1@%h
$ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker2@%h
```

Hostname variables: `%h` hostname with domain, `%n` hostname only, `%d` domain only, `%%` literal percent. For host george.example.com, `worker1@%h` gives `worker1@george.example.com`, `worker1@%n` gives `worker1@george`, `worker1@%d` gives `worker1@example.com`.

Paths for `--logfile`, `--pidfile`, `--statedb` also expand: `%p` full node name, `%h`, `%n`, `%d`, `%i` prefork pool process index (0 for MainProcess), `%I` index with separator. With `-n worker1@example.com -c2 -f %n-%i.log` you get worker1-0.log (main), worker1-1.log, worker1-2.log. With `%n%I.log` you get worker1.log, worker1-1.log, worker1-2.log. The number is the process index, not a pid or count, so it stays within the process limit across recycling.

Escaping gotchas:
- Starting `celery worker` directly: use `%%` for a literal percent (`logs/%%n-%n.log`).
- Through `celery multi`, values are formatted twice, so a literal percent in log/pid paths needs `%%%%` (`--logfile=logs/%%%%n-%n.log` becomes `logs/%n-worker.log`). `%i` and `%I` pass through multi untouched.
- Under supervisor, escape `%` as `%%h`.
- Since 5.7 a leading `~` in `--workdir`, `--pidfile`, `--logfile` is expanded for the user running `celery multi`, not the `--uid` user.

Concurrency: default is multiprocessing (prefork), with `--concurrency` defaulting to the CPU count. Since 5.7 `--concurrency=auto` sizes the prefork pool from the cgroup CPU quota and affinity mask (Linux only; a no-op for threads, gevent, eventlet, solo), useful in containers or CPU-limited systemd units. More processes is not always better, and several workers (for example 3 with 10 processes each) may beat one; experiment.

## Checked

2026-11-07. Re-read the cited page(s) (workers) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
