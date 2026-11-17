---
id: computing-software.web-development.litestar.litestar-repository-tutorial
name: litestar-repository-tutorial
category: computing-software
field: web-development
product: litestar
tags: [litestar, repository-tutorial, sqlalchemy, repository, bulk-operations, pagination, slug, advanced-alchemy]
level: practitioner
status: docs-checked
description: "Walkthrough of the Litestar repository tutorial: Author/Book models, repository methods, bulk operations, controller injection and a slug-key extension."
sources: [https://docs.litestar.dev/latest/tutorials/repository-tutorial/01-modelling-and-features.html, https://docs.litestar.dev/latest/tutorials/repository-tutorial/02-repository-introduction.html, https://docs.litestar.dev/latest/tutorials/repository-tutorial/03-repository-controller.html, https://docs.litestar.dev/latest/tutorials/repository-tutorial/04-repository-other.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar repository tutorial

Goal: model authors and books, use the repository standalone and in a controller, then extend it.

## Method

1. Model `Author` on `UUIDBase` (`id`, `name`, `dob`) with a `books` relationship. Model `Book` on `UUIDAuditBase` with `author_id` as a `ForeignKey("author.id")`; the audit base adds timestamp columns. Table names are deduced from the class name (`EventLog` becomes `event_log`).
2. Spanner only: `BigIntBase` and `BigIntAuditBase` are not supported there.
3. Repository methods: `get`, `get_one`, `get_one_or_none`, `list`, `list_and_count` (returns rows plus total), `get_or_create`, `create`, `create_many`, `update`, `update_many`, `upsert`, `upsert_many`, `delete`, `delete_many`. Bulk operations use dialect-specific efficiencies and multi-row `RETURNING` when the driver supports it; oversized `IN` lists are split into several queries automatically.
4. Standalone use: subclass `SQLAlchemyAsyncRepository[Author]`, set `model_type = Author`, and wrap `AuthorRepository(session=db_session)` in an async context manager that rolls back on exception and commits on success.
5. The examples call `repo.add(...)`, `repo.update(obj)`, `repo.delete(id)`, `repo.get_one_or_none(id=id)`; the bulk example uses `add_many`, `list_and_count(LimitOffset(limit=10, offset=0))`, `delete_many([...ids])` and `count()`.
6. In a controller: write a provider returning `AuthorRepository(session=db_session)` (the SQLAlchemy plugin supplies the session). Pass `statement=select(AuthorModel).options(selectinload(AuthorModel.books))` to override the default query. The list route takes a `LimitOffset` filter for pagination. A sync version uses the identical API with `SQLAlchemySyncRepository`.
7. Extending: add a `SlugKey` mixin (`slug` column, `String(length=100)`, unique) and a repository subclass with `get_available_slug(value_to_slugify, **kwargs)`. If the slug already exists, random digits are appended. "Follow the Yellow Brick Road!" becomes `follow-the-yellow-brick-road`.

## Gotchas

- The slug approach costs one extra query per insert.
- Do not expose integer primary keys in URLs (a security concern per the page); slugs are friendlier than UUIDs.

## Verify

Per the tutorial's bulk example, after `delete_many` on the selected rows, `count()` reports the remaining rows.

## Checked

2026-11-07. Read the full cited page(s) (tutorials/repository-tutorial/01-modelling-and-features.html, tutorials/repository-tutorial/02-repository-introduction.html, tutorials/repository-tutorial/03-repository-controller.html, tutorials/repository-tutorial/04-repository-other.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
