---
id: computing-software.messaging-and-integration.celery.routing-amqp-cli-hands-on
name: routing-amqp-cli-hands-on
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, routing, amqp, celery-amqp, exchange, queue, cli, celery-routing-amqp]
level: practitioner
status: docs-checked
description: "Use the celery amqp shell to declare exchanges and queues, bind, publish, get, ack and delete, plus the AMQP concepts behind Celery routing."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/routing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: inspect and administer queues and exchanges from the command line, and understand the AMQP model.

## Concepts

- A message has headers (content type, content encoding) and a body (task name, task id UUID, args, and meta-data like retries or ETA).
- Producers (publishers) send; consumers receive; the broker routes.
- Messages go to exchanges; an exchange routes to one or more queues; the message waits until consumed and is deleted when acknowledged.
- To send and receive: create an exchange, create a queue, bind the queue to the exchange.
- Exchange types: `direct` (exact routing key), `topic` (dot-separated words; `*` matches one word, `#` zero or more, so `*.news`, `usa.#`), `fanout`, `headers`.

## celery amqp shell

```console
$ celery -A proj amqp
-> connecting to amqp://guest@localhost:5672/.
-> connected.
1>
```

The prompt number counts commands; `help` lists them; tab completes. It works on non-AMQP brokers too, though not every command may be implemented. You can also pass commands as arguments.

## Session

```console
1> exchange.declare testexchange direct
2> queue.declare testqueue
ok. queue:testqueue messages:0 consumers:0.
3> queue.bind testqueue testexchange testkey
4> basic.publish 'This is a message!' testexchange testkey
5> basic.get testqueue
{'body': 'This is a message!', 'delivery_info': {'delivery_tag': 1, ...}}
6> basic.ack 1
7> queue.delete testqueue
ok. 0 messages deleted.
8> exchange.delete testexchange
```

`basic.get` polls synchronously: fine for maintenance, but services should use `basic.consume`. Unacknowledged messages are redelivered to another consumer if the channel closes. Delivery tags are unique per channel within a connection, not across connections.

## Command signatures

- `exchange.declare(exchange_name, type, passive, durable, auto_delete, internal)`: passive only checks existence; durable survives broker restart; auto_delete removes it when no queues use it.
- `queue.declare(queue_name, passive, durable, exclusive, auto_delete)`: exclusive queues can only be consumed by the current connection and imply auto_delete.
- `queue.bind(queue_name, exchange_name, routing_key)`: unbound queues receive nothing.
- `queue.delete(name, if_unused=False, if_empty=False)`
- `exchange.delete(name, if_unused=False)`

Declaring means asserting the entity exists and is operable, not necessarily creating it; whoever needs it first usually creates it.

## Checked

2026-11-07. Re-read the cited page(s) (routing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
