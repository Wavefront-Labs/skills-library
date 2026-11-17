---
id: computing-software.messaging-and-integration.celery.celery-single-execution-task-lock
name: celery-single-execution-task-lock
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-task-lock, cache-lock, memcached, mutual-exclusion, idempotent, django, python]
level: practitioner
status: docs-checked
description: "Ensure a Celery task runs only one at a time per key using an atomic cache.add lock with expiry, with the lock released safely before timeout."
sources:
  - https://docs.celeryq.dev/en/stable/tutorials/task-cookbook.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: prevent two workers from running the same job concurrently (the cookbook example imports an RSS feed identified by the MD5 of its URL).

Approach: a lock in the Django cache framework, reachable by all workers. The cache key expires after a timeout in case something unexpected happens ("and something always will"), so the task's run time should not exceed that timeout.

Requirement: the cache backend's `.add` must be atomic. `memcached` is known to work well.

```python
import time
from celery import task
from celery.utils.log import get_task_logger
from contextlib import contextmanager
from django.core.cache import cache
from hashlib import md5
from djangofeeds.models import Feed

logger = get_task_logger(__name__)
LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes

@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    status = cache.add(lock_id, oid, LOCK_EXPIRE)  # fails if key exists
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)

@task(bind=True)
def import_feed(self, feed_url):
    feed_url_hexdigest = md5(feed_url).hexdigest()
    lock_id = '{0}-lock-{1}'.format(self.name, feed_url_hexdigest)
    logger.debug('Importing feed: %s', feed_url)
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            return Feed.objects.import_feed(feed_url).url
    logger.debug('Feed %s is already being imported by another worker', feed_url)
```

Details to keep:
- The lock id combines the task name and the digest of the argument that identifies the work.
- `cache.add` fails if the key already exists; the task then logs and skips.
- Release only if the lock was acquired and the timeout has not been exceeded, which lessens the chance of releasing an expired lock now owned by someone else. The page notes memcache delete is very slow, but it is needed to keep the atomic `add` semantics.
- `self.app.oid` is stored as the lock value; the task is `bind=True` so it can read `self.name`.

## Checked

2026-11-07. Re-read the cited page(s) (task-cookbook) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Changed: reworded cache.add outcome to match the cookbook comment.

Method: documentation only; no commands were run.
