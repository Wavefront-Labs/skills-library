---
id: computing-software.web-development.django.migrations-data-squashing-zero-downtime
name: migrations-data-squashing-zero-downtime
category: computing-software
field: web-development
product: django
tags: [django, django-migrations, data-migrations, squashmigrations, zero-downtime, runpython, makemigrations, python, web-development]
level: practitioner
status: docs-checked
description: "Managing Django migrations: makemigrations review, RunPython data migrations, squashing, resolving conflicts, and expand/contract steps for zero-downtime deploys."
sources:
  - https://docs.djangoproject.com/en/stable/topics/migrations/
  - https://docs.djangoproject.com/en/stable/howto/writing-migrations/
  - https://docs.djangoproject.com/en/stable/ref/migration-operations/
  - https://github.com/David-Wobrock/django-migration-linter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrations: data migrations, squashing, zero downtime

**Goal:** schema changes that are reviewed, reversible and safe to deploy while old code is still running.

## 1. Everyday workflow
```bash
python manage.py makemigrations app --name add_order_status
python manage.py sqlmigrate app 0012          # read the SQL before merging
python manage.py migrate
python manage.py makemigrations --check --dry-run   # CI: fails if models and migrations differ
python manage.py showmigrations
```
Commit migrations with the model change. Never edit an applied migration; add a new one.

## 2. Data migrations
```bash
python manage.py makemigrations app --empty --name backfill_status
```
```python
def forwards(apps, schema_editor):
    Order = apps.get_model("shop", "Order")          # historical model, not an import
    Order.objects.filter(status__isnull=True).update(status="new")

class Migration(migrations.Migration):
    dependencies = [("shop", "0012_add_order_status")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
```
- Use `apps.get_model` - imported models have today's fields and custom methods, which break on old migrations.
- Batch large backfills (`iterator()` + `bulk_update` in chunks) and consider `atomic = False` on the migration for huge tables (PostgreSQL wraps each migration in a transaction).
- Always provide a reverse (`noop` is fine when safe).

## 3. Zero-downtime: expand then contract
Old and new code run side by side during a deploy, so each migration must be compatible with both:
1. **Add** nullable column / new table (deploy 1). Code writes both old and new.
2. Backfill data migration.
3. Switch reads to the new column; add `NOT NULL` / constraints (deploy 2).
4. **Remove** the old column in a later deploy - first remove it from the model with `SeparateDatabaseAndState`, or ensure no code references it.

Dangerous in one step: renaming columns/tables, adding NOT NULL without a default on big tables, changing column types, adding indexes without `CONCURRENTLY`.
```python
from django.contrib.postgres.operations import AddIndexConcurrently
class Migration(migrations.Migration):
    atomic = False
    operations = [AddIndexConcurrently("order", models.Index(fields=["created_at"], name="order_created_idx"))]
```
Django 5.0+ `db_default` sets a database-level default. Lint with `django-migration-linter`.

## 4. Conflicts
Two branches each add `0013_*`: `python manage.py makemigrations --merge`. Better: rebase and regenerate the later one if unmerged.

## 5. Squashing
```bash
python manage.py squashmigrations app 0001 0040
```
Keep the old files until every environment has applied the squashed migration, then delete them, update migrations that depend on the deleted ones, and remove the `replaces` attribute. `RunPython` and `RunSQL` operations are not optimised away unless marked `elidable=True`.

## Verify
- [ ] CI runs `makemigrations --check` and applies migrations to a fresh DB.
- [ ] Each migration reverses: `migrate app <previous>` works in staging.
- [ ] Migration on a production-sized copy completes without long table locks.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (topics/migrations, howto/writing-migrations, ref/migration-operations, ref/django-admin, ref/contrib/postgres/operations, release notes 5.0), django-migration-linter README.
Confirmed: `makemigrations --check`/`--dry-run`/`--merge`/`--name`/`--empty`, `sqlmigrate`, `RunPython.noop`, `apps.get_model`, `atomic = False` on non-atomic migrations (SQLite and PostgreSQL wrap migrations in transactions), `SeparateDatabaseAndState`, `AddIndexConcurrently`, `db_default` (Django 5.0), squash cleanup steps and `replaces`, the linter repository location.
Corrected or removed: the unsupported "reset to a fresh initial migration" alternative; the linter source URL now points at the current repository.
Method: documentation only; no commands were run.
