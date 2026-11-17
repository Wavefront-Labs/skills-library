---
id: computing-software.web-development.django.model-constraints-and-indexes
name: model-constraints-and-indexes
category: computing-software
field: web-development
product: django
tags: [django, django-constraints, django-indexes, uniqueconstraint, checkconstraint, partial-index, gin-index, python, web-development]
level: practitioner
status: gated
description: "Enforcing integrity and speed in Django models with Meta.constraints and Meta.indexes: UniqueConstraint, CheckConstraint, conditional and functional indexes, validation."
sources:
  - https://docs.djangoproject.com/en/stable/ref/models/constraints/
  - https://docs.djangoproject.com/en/stable/ref/models/indexes/
  - https://docs.djangoproject.com/en/stable/ref/contrib/postgres/indexes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model constraints and indexes

**Goal:** the database enforces business rules and supports the actual query patterns.

## 1. Constraints
```python
from django.db.models import Q, F, UniqueConstraint, CheckConstraint
from django.db.models.functions import Lower

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start = models.DateTimeField(); end = models.DateTimeField()
    email = models.EmailField()
    cancelled = models.BooleanField(default=False)

    class Meta:
        constraints = [
            CheckConstraint(condition=Q(end__gt=F("start")), name="booking_end_after_start"),   # 'check=' was deprecated in 5.1 and REMOVED in 6.0 (TypeError on 6.1.2)
            UniqueConstraint(fields=["room", "start"], condition=Q(cancelled=False), name="uniq_active_room_start"),
            UniqueConstraint(Lower("email"), name="uniq_email_ci"),
        ]
```
- `unique_together` still works but `UniqueConstraint` is preferred (conditions, expressions, `nulls_distinct` in 5.0+, `deferrable`).
- Model `full_clean()` / ModelForms validate constraints (`validate_constraints`) since 4.1 (release notes; run: `full_clean()` reported "Constraint ... is violated."), giving friendly errors; the DB is the final guard (`IntegrityError`).
- PostgreSQL exclusion constraints (`django.contrib.postgres.constraints.ExclusionConstraint`) prevent overlapping ranges (classes import with psycopg installed; behaviour on a live PostgreSQL was not run: gated: unconfirmed, source is paywalled or blocked).

## 2. Indexes
```python
    class Meta:
        indexes = [
            models.Index(fields=["room", "-start"], name="booking_room_start_idx"),
            models.Index(fields=["email"], condition=Q(cancelled=False), name="booking_active_email_idx"),
            models.Index(Lower("email"), name="booking_lower_email_idx"),
        ]
```
- `ForeignKey` gets an index automatically; `unique=True` and unique constraints create indexes.
- Composite index order = query order: equality columns first, then range/order columns.
- `db_index=True` on a field is fine for single columns; prefer `Meta.indexes` for names you control.
- PostgreSQL: `GinIndex` for JSONField/ArrayField/full-text, `BrinIndex` for huge append-only timestamp tables, `opclasses=["varchar_pattern_ops"]` for `LIKE 'x%'`.

## 3. Prove it with EXPLAIN
```python
print(Booking.objects.filter(room_id=1).order_by("-start").explain(analyze=True))
```
Look for `Index Scan` vs `Seq Scan` on PostgreSQL (SQLite shows `SEARCH shop_booking USING INDEX booking_room_start_idx`, which is what the example above printed on Django 6.1.2/SQLite; the PostgreSQL plan was not run here). Indexes cost writes and storage - add for real slow queries (pg_stat_statements, debug toolbar).

## 4. Deploying on big tables
Adding indexes locks writes; use `AddIndexConcurrently` (non-atomic migration). Adding a constraint validates all rows; on PostgreSQL add `NOT VALID` via `RunSQL` then `VALIDATE CONSTRAINT` separately for huge tables. (gated: unconfirmed, source is paywalled or blocked; no PostgreSQL server here. `AddIndexConcurrently` exists with `atomic = False`, checked by import.)

## Verify
- [ ] Inserting violating data raises `IntegrityError` (test it).
- [ ] Slow-query endpoints show index scans in `explain()`.
- [ ] Migrations for large tables use concurrent index creation.
