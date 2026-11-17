---
id: computing-software.web-development.django.multiple-databases-and-routers
name: multiple-databases-and-routers
category: computing-software
field: web-development
product: django
tags: [database-routers, multiple-databases, read-replicas, django-orm, django]
level: advanced
status: verified
description: "Running Django against multiple databases: DATABASES config, using() and db_for_read routers for read replicas, replication lag, migrations per database and testing."
sources:
  - https://docs.djangoproject.com/en/stable/topics/db/multi-db/
  - https://docs.djangoproject.com/en/stable/topics/testing/advanced/#topics-testing-advanced-multidb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple databases and database routers

## 1. Configuration
```python
DATABASES = {
    "default": env.db("DATABASE_URL"),            # primary (writes)
    "replica": env.db("REPLICA_URL"),             # read replica
    "analytics": env.db("ANALYTICS_URL"),          # separate app database
}
DATABASE_ROUTERS = ["core.routers.AnalyticsRouter", "core.routers.PrimaryReplicaRouter"]   # app-specific first
```

## 2. Routers
```python
class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints): return "replica"
    def db_for_write(self, model, **hints): return "default"
    def allow_relation(self, obj1, obj2, **hints):
        return {obj1._state.db, obj2._state.db} <= {"default", "replica"}
    def allow_migrate(self, db, app_label, model_name=None, **hints): return db == "default"

class AnalyticsRouter:
    route_app_labels = {"analytics"}
    def db_for_read(self, model, **hints): return "analytics" if model._meta.app_label in self.route_app_labels else None
    db_for_write = db_for_read
    def allow_migrate(self, db, app_label, **hints):
        if app_label in self.route_app_labels: return db == "analytics"
        return None if db != "analytics" else False
```
Routers are consulted in order; returning `None` passes to the next. Put app-specific routers **before** the generic replica router: with the generic router first (the order this skill used to show), `PrimaryReplicaRouter` answers for every model, so `analytics` models were read from `replica`, written to `default`, and their tables were migrated into `default` while the `analytics` database stayed empty (measured).

## 3. Replication lag
A user who just saved and is redirected may read from a replica that hasn't caught up ("my change disappeared").
- Read-your-writes: after a write, pin the request (or the user's next few seconds via a cookie/session flag) to `default`.
- Inside `transaction.atomic()` blocks, reads should go to the primary - route with a thread-local/contextvar set by middleware for non-GET requests.
- Use `.using("default")` explicitly for reads that must be fresh (payments, permissions).

## 4. Explicit selection
```python
Order.objects.using("replica").filter(...)
obj.save(using="analytics")
with transaction.atomic(using="analytics"): ...
```
Cross-database relations (ForeignKey to a model in another DB) aren't supported by the DB; Django won't enforce them.

## 5. Migrations and tests
- `python manage.py migrate --database=analytics` per database; `allow_migrate` decides what runs where.
- Tests: declare `databases = {"default", "analytics"}` on TestCase classes that touch other DBs. Mark replicas as test mirrors: `"TEST": {"MIRROR": "default"}` so tests see written data.

## Verify
- [ ] Reads after writes in the same flow hit the primary; each database receives only its migrations; tests use MIRROR for replicas.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets. Three file-backed SQLite databases (`default`, `replica` as a second alias of the same file, `analytics`) and two tiny apps.
- Run: with `[PrimaryReplicaRouter, AnalyticsRouter]`: `migrate --database=default` and `--database=analytics` put `analytics_hit` and `main_thing` in `default` and nothing in `analytics`; `Hit` reads went to `replica`.
- Run: with `[AnalyticsRouter, PrimaryReplicaRouter]`: `analytics_hit` only in the `analytics` database, `main_thing` only in `default`; `Hit` read and write went to `analytics`; `Thing.objects.using("replica")` and `.using("default")` both worked.
- Run: `django-environ` `env.db("URL")` returns a Django DATABASES dict (`django.db.backends.sqlite3` for a `sqlite:///` URL).
- Fetched: topics/db/multi-db.txt and the settings reference (`TEST` / `MIRROR` setting: "the alias of the database that this database should mirror during testing").
