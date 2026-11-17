---
id: computing-software.messaging-and-integration.celery.celery-bootsteps-and-custom-consumers
name: celery-bootsteps-and-custom-consumers
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-extending, celery, bootsteps, consumerstep, blueprint, kombu, gossip, qos]
level: advanced
status: docs-checked
description: "Extend Celery workers with ConsumerStep custom Kombu consumers and Worker or Consumer bootsteps, with requires declarations, install and shutdown rules."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/extending.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extend workers with bootsteps and custom consumers

Goal: run your own Kombu consumer or lifecycle hook inside the Celery worker.

Custom consumer: subclass `bootsteps.ConsumerStep`, implement `get_consumers(self, channel)` returning `kombu.Consumer` objects, started whenever the connection is established:

```python
class MyConsumerStep(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [Consumer(channel, queues=[my_queue],
                         callbacks=[self.handle_message], accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        message.ack()

app.steps['consumer'].add(MyConsumerStep)
```

`callbacks` take `(body, message)`; `on_message` takes a single `(message,)` callback and does not decode the payload (call `message.decode()`). Publish with `app.producer_or_acquire(producer)` and `producer.publish(..., serializer='json', exchange=..., routing_key=..., declare=[my_queue], retry=True)`.

Blueprints: bootsteps belong to one of two blueprints, Worker (starts first: event loop/Hub, pool, Timer, then the Consumer blueprint) and Consumer (restarted on every broker connection loss; includes heartbeat, control command consumer, task consumer). Consumer steps must be restartable; `shutdown` is called at worker shutdown.

Declare what you use via `requires`, for example `requires = {'celery.worker.components:Pool'}` for `worker.pool`; likewise `...:Hub` (only amqp/redis async transports), `...:Timer`, `...:Statedb` (only with `statedb`), `celery.worker.autoscaler:Autoscaler`. Consumer steps: `celery.worker.consumer.connection:Connection`, `...events:Events`, `...gossip:Gossip`, `...heart:Heart`, `...tasks:Tasks` (for `task_consumer` and `strategies`). Gossip exposes `gossip.on.node_join`, `node_leave`, `node_lost` (lost does not mean offline; use a timeout). `consumer.qos.increment_eventually(1)`, `decrement_eventually(1)`, `set(10)` change prefetch; `consumer.add_task_queue(name, ...)` persists across reconnects.

Timer example: `worker.timer.call_repeatedly(30.0, self.detect, (worker,), priority=10)` in `start`, cancel the returned ref in `stop`.

Install classes (not instances): `app.steps['worker'].add(MyWorkerStep)`, `app.steps['consumer'].update([StepA, StepB])`. Order comes from the `requires` dependency graph. Step hooks: `__init__(self, parent, **kwargs)`, `start`, `stop`, `shutdown` (Consumer only), `terminate`.

Gotcha: `stop` and `shutdown` run inside a signal handler, where Python logging is not reentrant, so prints are not logged then and your methods must be reentrant. Use `--loglevel=debug` to see boot order.

Task log messages can be customised by overriding `celery.app.trace.LOG_SUCCESS`, `LOG_REJECTED` etc. (format strings receive name and id, some also `exc` or return value).

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/extending.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
