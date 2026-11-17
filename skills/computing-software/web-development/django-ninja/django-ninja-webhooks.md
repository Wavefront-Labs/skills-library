---
id: computing-software.web-development.django-ninja.django-ninja-webhooks
name: django-ninja-webhooks
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, webhooks, openapi, django-tasks, hmac, payload-schema]
level: practitioner
status: docs-checked
description: "Document outgoing webhooks in Django Ninja with @api.webhook, set options, use router webhooks, and send signed payloads with Django tasks."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/webhooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: describe webhook payloads in OpenAPI, then send them yourself. Webhooks are documentation only; Ninja does not send them.

## Declare
```python
@api.webhook("order.paid")
class OrderPaid(Schema):
    id: int
    total: Decimal
```
Appears in the `webhooks` section of the OpenAPI schema (3.1). The decorator returns the class unchanged. The name is optional: `@api.webhook` alone uses the class name.

## Options
```python
@api.webhook(
    "order.refunded", method="POST", summary="Order refunded",
    description="Sent when an order is fully or partially refunded",
    tags=["orders"], operation_id="order_refunded", deprecated=False,
    include_in_schema=True,
    openapi_extra={"responses": {410: {"description": "Unsubscribe"}}},
)
class OrderRefunded(Schema): ...
```
Summary defaults to the class name ("Order Refunded"). Names must be unique within an API.

## In routers
`@router.webhook("order.paid")` works; once the router is added to the API, its (and child routers') webhooks appear. Router tags apply to webhooks without their own `tags`.

## Sending (one approach from the page)
Delivery needs decisions that are yours: subscription storage, payload signing, retries/backoff/timeouts, and which task queue.

1. Task (Django 6.0+ `django.tasks`, or the `django-tasks` package on older versions):
```python
@task
def deliver_webhook(url: str, secret: str, event: str, payload: dict) -> None:
    body = json.dumps(payload).encode()
    signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    response = requests.post(url, data=body, headers={
        "Content-Type": "application/json",
        "X-Webhook-Event": event,
        "X-Webhook-Signature": f"sha256={signature}",
    }, timeout=10)
    response.raise_for_status()  # marks the task as failed
```
Task arguments must be JSON-serializable, so pass a dict.

2. Enqueue helper, after commit:
```python
def send_webhook(event: str, payload: Schema) -> None:
    data = payload.model_dump(mode="json")
    def enqueue():
        for sub in WebhookSubscription.objects.filter(event=event):
            deliver_webhook.enqueue(sub.url, sub.secret, event, data)
    transaction.on_commit(enqueue)
```
3. Call `send_webhook("order.paid", OrderPaid(id=order.id, total=order.total))` where the event happens; reusing the Schema keeps docs and payload in sync.

Warning: the default `ImmediateBackend` runs tasks inside the request. In production configure a real worker backend in the `TASKS` setting; retries depend on the backend.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/webhooks.md from GitHub. Confirmed against the whole page: @api.webhook usage and name default, every option, router webhooks and tag inheritance, the Django tasks delivery example, JSON-serializable task arguments, on_commit enqueueing and the ImmediateBackend warning. Nothing removed.

Method: documentation only; no commands were run.
