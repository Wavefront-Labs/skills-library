---
id: computing-software.messaging-and-integration.celery.canvas-stamping-visitors
name: canvas-stamping-visitors
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, canvas, stamping, stampingvisitor, result-extended, debugging, celery-canvas-stamping]
level: practitioner
status: docs-checked
description: "Label Celery canvas signatures with stamp and custom StampingVisitor classes, including stamped_headers rules and callback stamping."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/canvas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: since Celery 5.3, label a signature and its parts (groups, chains, chords, callbacks) with metadata for debugging, using the Visitor pattern.

## Simple stamp

```python
sig1 = add.si(2, 2)
sig1_res = sig1.freeze()
g = group(sig1, add.si(3, 3))
g.stamp(stamp='your_custom_stamp')
res = g.apply_async()
sig1_res._get_task_meta()['stamp']   # ['your_custom_stamp']
```

For stamps to be useful in results, set `result_extended = True`.

## Custom visitor

Subclass `StampingVisitor` and implement the hooks you need: `on_signature(self, sig, **headers)`, `on_group_start`, `on_group_end`, `on_chain_start`, `on_callback(self, callback, **header)`, `on_errback(self, errback, **header)`. Hooks return a dict of stamps (`on_group_end` returns None in the page's example).

```python
class MonitoringIdStampingVisitor(StampingVisitor):
    def on_signature(self, sig, **headers) -> dict:
        return {'monitoring_id': uuid4().hex}

sig_example.stamp(visitor=MonitoringIdStampingVisitor())
group_example.stamp(visitor=MonitoringIdStampingVisitor())
chord_example.stamp(visitor=MonitoringIdStampingVisitor())
chain_example.stamp(visitor=MonitoringIdStampingVisitor())
```

Each task gets a different monitoring id in the example.

An `InGroupVisitor` example tracks state with `on_group_start` (set `self.in_group = True`, return `{"in_group": [self.in_group], "stamped_headers": ["in_group"]}`) and `on_group_end` (reset it).

## stamped_headers is optional

- Omitted: every key in the returned dict is treated as a stamp.
- Present: only the listed keys are stamps, e.g. `{'monitoring_id': ..., 'other_data': 'value', 'stamped_headers': ['monitoring_id']}` stamps only `monitoring_id`.

## Callbacks

Stamping also applies to callbacks and errbacks implicitly via `on_callback` and `on_errback`. Warning: the callback must be linked to the signature before stamping.

```python
c = chord([add.s(1, 1), add.s(2, 2)], xsum.s())
c.link(signature('sig_link'))
c.link_error(signature('sig_link_error'))
c.stamp(visitor=CustomStampingVisitor())
```

Result: header and body options get `{'header': 'value', 'stamped_headers': ['header']}`; the linked callback also gets `'on_callback': True` and the errback `'on_errback': True`, each added to its `stamped_headers`.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/canvas.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
