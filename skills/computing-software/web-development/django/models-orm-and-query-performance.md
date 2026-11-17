---
id: computing-software.web-development.django.models-orm-and-query-performance
name: models-orm-and-query-performance
category: computing-software
field: web-development
product: django
tags: [django, orm, models, migrations, makemigrations, migrate, n-plus-one, n+1, select-related, prefetch-related, prefetch, only, defer, f-expressions, q-objects, annotate, aggregate, transactions, atomic, select-for-update, race-conditions, indexes, meta, constraints, django-debug-toolbar, assertnumqueries, explain, postgresql, python, web-development]
level: practitioner
status: docs-checked
description: "Django models and ORM: migrations workflow, fixing N+1 with select_related/prefetch_related, only/defer, F and Q, atomic transactions, select_for_update, indexes, assertNumQueries."
sources:
  - https://docs.djangoproject.com/en/stable/topics/db/models/
  - https://docs.djangoproject.com/en/stable/topics/db/optimization/
  - https://docs.djangoproject.com/en/stable/topics/migrations/
  - https://django-debug-toolbar.readthedocs.io/
  - https://docs.djangoproject.com/en/stable/ref/models/expressions/
  - https://pytest-django.readthedocs.io/en/latest/helpers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Django models, ORM and query performance — count your queries

**Goal:** model data with the database doing the integrity work, ship migrations
safely, and keep every view at a small, constant number of queries.

## 1. Models that encode the rules
```python
class Order(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["customer", "-created"])]
        constraints = [models.CheckConstraint(condition=models.Q(total__gte=0), name="order_total_gte_0")]
```
- Choose `on_delete` deliberately: `PROTECT` for financial records, `CASCADE` only for true children.
- Money is `DecimalField`, never `FloatField`.
- `CheckConstraint` took `check=` before Django 5.1 and `condition=` after (the old name is deprecated) — match your version.
- `ForeignKey` gets an index automatically; add composite indexes for your real filter + order combinations.

## 2. Migrations workflow
```bash
python manage.py makemigrations app_name
python manage.py sqlmigrate app_name 0007    # read the SQL before it hits production
python manage.py migrate
python manage.py makemigrations --check --dry-run   # in CI: fail if models and migrations disagree
```
Commit migrations with the model change. Never edit a migration that has run in a shared
environment — add a new one. Adding a NOT NULL column to a big table: add it nullable, backfill
in batches (a `RunPython` or a management command), then make it non-null. On PostgreSQL,
`AddIndexConcurrently` (in `django.contrib.postgres.operations`, with `atomic = False` on the
migration) avoids locking writes.

## 3. Find and kill N+1
```python
# 1 + N queries: each order.customer hits the DB
for o in Order.objects.all(): print(o.customer.name)
# 1 query with a JOIN — forward FK / one-to-one
Order.objects.select_related("customer")
# 2 queries — reverse FK and many-to-many
Customer.objects.prefetch_related("orders")
# Filtered prefetch
Customer.objects.prefetch_related(
    Prefetch("orders", queryset=Order.objects.filter(status="paid"), to_attr="paid_orders"))
```
Gotcha: calling `.filter()` on a prefetched relation inside the loop discards the prefetch
and queries again — use `Prefetch(..., to_attr=)` instead.

Tools: **django-debug-toolbar** (SQL panel shows duplicate queries) in development, and
lock it into tests:
```python
def test_order_list_queries(self):
    with self.assertNumQueries(3):
        self.client.get("/orders/")
```
For pytest-django the equivalent is the `django_assert_num_queries` fixture.

## 4. Load less, compute in SQL
- `.only("id", "name")` / `.defer("body")` for wide rows — but touching a deferred field later triggers one query per object.
- `.values()` / `.values_list(..., flat=True)` when you don't need model instances.
- `.exists()` not `if queryset:`; `.count()` not `len(queryset)` (unless you'll iterate anyway).
- `annotate(n=Count("orders"))` instead of counting in Python.
- `.iterator(chunk_size=2000)` for large exports to avoid loading everything into memory.
- `bulk_create` / `bulk_update` for batches (they skip `save()` and signals).
- `queryset.explain()` shows the database plan.

## 5. F, Q and race-free updates
```python
from django.db.models import F, Q
Product.objects.filter(pk=pk).update(stock=F("stock") - 1)   # atomic in SQL, no lost update
Order.objects.filter(Q(status="new") | Q(total__gt=1000), ~Q(customer__blocked=True))
```
After `obj.field = F(...)` + `save()`, Django refreshes the value on SQLite, PostgreSQL and Oracle without an extra query and defers the reload on MySQL/MariaDB; `obj.refresh_from_db()` reloads it explicitly.

## 6. Transactions and locking
```python
from django.db import transaction
with transaction.atomic():
    acct = Account.objects.select_for_update().get(pk=pk)   # row lock until commit
    acct.balance -= amount
    acct.save(update_fields=["balance"])
    transaction.on_commit(lambda: send_receipt.delay(acct.pk))
```
- `select_for_update()` only works inside `atomic()` (it raises outside one).
- Use `on_commit` for emails and task queues so a rollback doesn't send a receipt for nothing.
- `ATOMIC_REQUESTS = True` wraps every view in a transaction — simple, but holds transactions open during slow views.

## Verify
- [ ] `makemigrations --check` passes in CI; `sqlmigrate` reviewed for risky operations.
- [ ] Debug toolbar shows no duplicated queries on list pages.
- [ ] Key views have `assertNumQueries` tests that stay constant as data grows.
- [ ] Counters and balances use `F()` or `select_for_update`, not read-modify-write in Python.
- [ ] Side effects after writes run in `transaction.on_commit`.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (topics/db/optimization, ref/models/querysets, ref/models/expressions, ref/models/constraints, topics/db/transactions, ref/models/fields, ref/contrib/postgres/operations, release notes 5.1), pytest-django helpers docs, PostgreSQL CREATE INDEX docs.
Confirmed: `CheckConstraint(condition=...)` with `check` deprecated in 5.1, automatic index on `ForeignKey`, `select_related`/`prefetch_related`/`Prefetch(to_attr=)` and the chained-method cache rule, `iterator()` default chunk size 2000 (no prefetch), `bulk_create`/`bulk_update` skip `save()` and signals, `explain()`, `exists()` and `count()` guidance, `select_for_update()` requires a transaction, `on_commit`, `ATOMIC_REQUESTS`, `assertNumQueries`, `django_assert_num_queries`, `AddIndexConcurrently` with `atomic = False` (CREATE INDEX CONCURRENTLY does not lock out writes).
Corrected or removed: the F() refresh advice, which now follows the documented backend behaviour.
Method: documentation only; no commands were run.
