---
id: computing-software.messaging-and-integration.celery.celery-chord-error-callbacks-and-expiry
name: celery-chord-error-callbacks-and-expiry
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-chord, celery, chord, link-error, result-chord-expires, canvas, error-callback]
level: practitioner
status: docs-checked
description: "Configure Celery chord behavior: error callbacks on the header, chord bookkeeping expiry, join timeout and retry interval."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Chord settings: error callbacks, expiry, timeouts

Goal: make chords report header failures and avoid the body silently never running.

## task_allow_error_cb_on_chord_header (5.3+, default disabled)
Default: with `c = chord(group([t1, t2]), t3); c.link_error(error_callback_sig)`, if any header task fails the body `t3` does not run and `error_callback_sig` is called once (for the body).

Enabled:
1. `error_callback_sig` is linked to `t1`, `t2` and `t3`.
2. If any header task fails, the callback is called for each failed header task and for the body, even though the body never ran.

Example: header `group([failingT1, failingT2])`, body `t3`, both header tasks fail: body does not run and the callback is called 3 times (twice for the header, once for the body). A `chain(header, body)` is upgraded to a chord internally and behaves the same.

## Expiry and timeouts
- `result_chord_expires` (5.7+, default same as `result_expires`): how long chord bookkeeping is kept after the chord starts or a header task finishes. With the cache backend each header result is kept that long too, never less than `result_expires`. When the chord finishes, header results get `result_expires` back. If it expires before the last header task finishes, the body never runs, so set it longer than the chord total run time. `0` means bookkeeping never expires while open (and the saved header of a chord with nested groups never expires); a chord that never completes, such as after a lost header task, then leaves bookkeeping forever. Only works with the cache and Redis backends.
- Memcached reads an expiry over 30 days as an absolute time, so keep `result_chord_expires` at 30 days or less with the cache backend.
- `result_chord_join_timeout` (default 3.0): timeout in seconds when joining a group results within a chord.
- `result_chord_retry_interval` (default 1.0): default interval for retrying chord tasks.
- `result_expires` (default 1 day) is covered in the result-backend retry and expiry skill.

## GCS note
The GCS result backend uses `firestore_project` (default `gcs_project`) for chord reference counting.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
