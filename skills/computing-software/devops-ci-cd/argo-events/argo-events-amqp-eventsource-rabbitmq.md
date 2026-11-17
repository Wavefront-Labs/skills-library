---
id: computing-software.devops-ci-cd.argo-events.argo-events-amqp-eventsource-rabbitmq
name: argo-events-amqp-eventsource-rabbitmq
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, amqp-eventsource, rabbitmq, exchange, routing-key, pika]
level: practitioner
status: docs-checked
description: "Consume RabbitMQ or other AMQP messages with the AMQP EventSource and know the event data fields it publishes."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/setup/amqp.md", "https://github.com/argoproj/argo-events/blob/master/docs/eventsources/ha.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events amqp eventsource rabbitmq

The AMQP EventSource listens to messages on a message queue. The CloudEvent `data` carries: `contentType`, `contentEncoding`, `deliveryMode` (non-persistent 1 or persistent 2), `priority` (0 to 9), `correlationId`, `replyTo`, `expiration`, `messageId`, `timestamp`, `type`, `appId`, `exchange`, `routingKey` and `body`.

Walkthrough from the docs:
1. Run RabbitMQ locally in the cluster (a Service on port 5672 plus a ReplicationController running the `rabbitmq` image) and wait for the pod.
2. Port-forward: `kubectl -n argo-events port-forward <rabbitmq-pod-name> 5672:5672`.
3. Apply `examples/event-sources/amqp.yaml` and check the EventSource pod logs to confirm it subscribed to the exchange.
4. Apply `examples/sensors/amqp.yaml`.
5. Publish with pika:

```python
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_publish(exchange='test', routing_key='hello', body='{"message": "hello"}')
```

6. `argo list` shows the triggered workflow.

AMQP is listed as an Active-Passive EventSource type: with `spec.replicas > 1` only one Pod serves traffic and the rest stand by (EventSource High Availability page).

## Checked

2026-11-04. Confirmed against the AMQP EventSource page (event data fields, RabbitMQ Service/ReplicationController setup, port-forward, example manifests, pika publish, `argo list`) and the EventSource High Availability page (AMQP is Active-Passive). Removed the advice to filter on `routingKey` and `exchange` in Sensor data filters, which the pages do not state.
Method: documentation only; no commands were run.
