---
id: computing-software.messaging-and-integration.celery.celery-unit-test-tasks-with-mocks
name: celery-unit-test-tasks-with-mocks
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-testing, celery, unit-test, mock, retry, eager, pytest-celery, bound-task]
level: practitioner
status: docs-checked
description: "Unit test Celery tasks by mocking collaborators and retry, and understand why task_always_eager is not suitable; choose between celery.contrib.pytest and pytest-celery."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/testing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit test Celery tasks with mocks

Goal: test task logic and retry behaviour without a broker.

Testing has two parts: unit and integration via `celery.contrib.pytest` (mock based), and smoke/production via `pytest-celery` >= 1.0.0 (Docker based). Installing pytest-celery also installs the `celery.contrib.pytest` infrastructure, but the two APIs are not compatible with each other.

For unit tests the preferred method is mocking. Eager mode (`task_always_eager`) is by definition not suitable: you test an emulation of a worker with many discrepancies from reality. Eagerly executed tasks also do not write results to the backend by default; see `task_store_eager_result`.

Keep tasks like web views: handle serialization, headers, retries, and put real logic elsewhere. Example task:

```python
@app.task(bind=True)
def send_order(self, product_pk, quantity, price):
    price = Decimal(price)  # json serializes this to string.
    product = Product.objects.get(product_pk)
    try:
        product.order(quantity, price)
    except OperationalError as exc:
        raise self.retry(exc=exc)
```

`bind=True` means the first argument is the task instance (`self`), giving access to task methods and attributes. Tests patch the collaborator and `retry`, call the task function directly, and assert:

```python
from unittest.mock import patch
from pytest import raises
from celery.exceptions import Retry

class test_send_order:

    @patch('proj.tasks.Product.order')  # patch Product in the module above
    def test_success(self, product_order):
        product = Product.objects.create(name='Foo')
        send_order(product.pk, 3, Decimal(30.3))
        product_order.assert_called_with(3, Decimal(30.3))

    @patch('proj.tasks.Product.order')
    @patch('proj.tasks.send_order.retry')
    def test_failure(self, send_order_retry, product_order):
        product = Product.objects.create(name='Foo')
        send_order_retry.side_effect = Retry()
        product_order.side_effect = OperationalError()
        with raises(Retry):
            send_order(product.pk, 3, Decimal(30.6))
```

The patch target is the name as seen from the module under test (`proj.tasks.Product.order`). Setting `side_effect` on the patched methods makes them raise the errors you want, so the retry path is exercised without a worker.

## Checked

2026-11-07. Re-read the cited page(s) (testing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
