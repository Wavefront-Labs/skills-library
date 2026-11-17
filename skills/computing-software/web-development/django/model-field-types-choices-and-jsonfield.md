---
id: computing-software.web-development.django.model-field-types-choices-and-jsonfield
name: model-field-types-choices-and-jsonfield
category: computing-software
field: web-development
product: django
tags: [django-field-types, jsonfield, textchoices, model-fields, django]
level: practitioner
status: verified
description: "Choosing Django model field types: CharField vs TextField, DecimalField for money, TextChoices and IntegerChoices, JSONField querying and indexing, UUIDs, nulls and defaults."
sources:
  - https://docs.djangoproject.com/en/stable/ref/models/fields/
  - https://docs.djangoproject.com/en/stable/topics/db/queries/#querying-jsonfield
  - https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Field types, choices and JSONField

## 1. Picking types
| Data | Field | Notes |
|---|---|---|
| Short strings | `CharField(max_length=...)` | `max_length` required (optional on PostgreSQL since 4.2) |
| Long text | `TextField` | |
| Money | `DecimalField(max_digits=12, decimal_places=2)` | never `FloatField` |
| Timestamps | `DateTimeField(auto_now_add=True)` / `auto_now=True` | `USE_TZ = True` stores UTC |
| Public ids | `UUIDField(default=uuid.uuid4, editable=False, unique=True)` | avoid enumerable ids in URLs |
| Booleans | `BooleanField(default=False)` | nullable tri-state: `null=True` |
| Email/URL/slug | `EmailField`, `URLField`, `SlugField` | add validation only |
| Files | `FileField`/`ImageField(upload_to=...)` | stores a path; files in storage backend |
| Generated | `GeneratedField(expression=..., output_field=..., db_persist=True)` (5.0+) | computed by the DB |

- `null=True` is about the database; `blank=True` is about form validation. For strings use `blank=True` with empty string, not `null=True` (two "empty" values).
- `db_default=Now()` (5.0+) sets defaults in the database, useful for rows inserted outside Django.

## 2. Choices
```python
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"
    status = models.CharField(max_length=20, choices=Status, default=Status.PENDING)   # 5.0+: pass the enum directly
# usage: order.status == Order.Status.PAID ; order.get_status_display()
```
- Choices are validated by forms/`full_clean()`, not the database: add a `CheckConstraint(condition=Q(status__in=Order.Status.values), name="order_status_valid")` for integrity (`condition=` is the argument from Django 5.1; the old `check=` was deprecated in 5.1 and removed in 6.0). An insert with a value outside the list raised `IntegrityError`.
- Changing choices creates a migration (no-op SQL) - keep it.

## 3. JSONField
```python
class Event(models.Model):
    payload = models.JSONField(default=dict)          # callable default, never {} literal
Event.objects.filter(payload__user__id=42)
Event.objects.filter(payload__tags__contains=["vip"])  # containment: not supported on SQLite or Oracle (raises NotSupportedError)
Event.objects.filter(payload__has_key="refund")
Event.objects.annotate(country=KT("payload__address__country"))   # KT() extracts text (4.2+)
```
- `JSONField(default={})` fails system check `fields.E010` (use `dict`). Index frequent lookups on PostgreSQL: `GinIndex(fields=["payload"])` for containment/has_key, or an expression index on a key.
- Use JSON for truly schemaless data (webhook payloads, settings); promote fields you filter/sort on to real columns.
- Validate the shape in the form/serializer or with a schema validator; the DB won't.

## Verify
- [ ] No floats for money; nullable strings justified; choices enforced by a constraint; JSON lookups used in hot paths have indexes (check `EXPLAIN`).

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets. PostgreSQL-only statements were read from the docs, not run (no PostgreSQL here).
- Run: `TextChoices` with `choices=Status` (5.0+), `get_status_display()`, `db_default=Now()`, `GeneratedField(expression=F("w")*F("h"), output_field=IntegerField(), db_persist=True)` (value 6 read back), `CheckConstraint(condition=...)` rejecting a bad value.
- Run: JSONField `payload__user__id=42`, `has_key`, `KT("payload__address__country")` worked on SQLite; `contains` raised NotSupportedError on SQLite; `JSONField(default={})` raised `fields.E010`.
- Fetched: 4.2 release notes (CharField `max_length` optional on PostgreSQL, `KT()` added), 5.0 notes (`db_default`, `GeneratedField`, choices enum), 5.1 and 6.0 notes (`CheckConstraint` `check` deprecated then removed), topics/db/queries.txt (`contains` / `contained_by` unsupported on Oracle and SQLite), contrib/postgres/indexes.txt (`GinIndex`).
