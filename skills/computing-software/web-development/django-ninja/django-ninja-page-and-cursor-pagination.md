---
id: computing-software.web-development.django-ninja.django-ninja-page-and-cursor-pagination
name: django-ninja-page-and-cursor-pagination
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, pagination, paginate, page-number-pagination, cursor-pagination, cursor]
level: practitioner
status: docs-checked
description: "Paginate Django Ninja list views with @paginate using PageNumberPagination for totals or CursorPagination for append-only feeds such as comments."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop returning whole tables; choose page-number or cursor pagination per endpoint.

```python
from ninja.pagination import CursorPagination, PageNumberPagination, paginate
```

## Page numbers

Put `@paginate` below the router decorator. The view keeps returning a queryset and `response` stays `list[TaskOut]`.

```python
@router.get("/", response=list[TaskOut])
@paginate(PageNumberPagination, page_size=20)
def list_tasks(request, ...): ...
```

- Adds query parameters `page` (from 1) and `page_size`; the response is `{"items": [...], "count": N}`.
- The database returns only the page's rows; `count` costs one extra `COUNT` query with the same filters.
- A page has `page_size` items (20 here). Clients may ask for more up to `max_page_size`, default 100 (`?page_size=500` returns at most 100).
- `?page=9` past the end is not an error: `{"items": [], "count": 7}`. `?page=0` is a `422`.
- In OpenAPI the response becomes a generated `PagedTaskOut` with `items` and `count`.
- Weak point: if rows are inserted at the top between requests, pages shift and a client may see an item twice.

## Cursor pagination

For feeds that grow at the end (comments), use `CursorPagination`. The paginator owns the ordering, so drop any `.order_by()` from the view.

```python
@router.get("/{task_id}/comments", response=list[CommentOut])
@paginate(CursorPagination, ordering=("id",), page_size=20)
def list_comments(request, project_id: Path[int], task_id: int):
    task = get_task_or_404(request.auth, project_id, task_id)
    return task.comments.select_related("author")
```

- `ordering` sorts the queryset and its first field records the position in the cursor; make it unique or close to it (a growing id works).
- Parameters are `cursor` and `page_size`. There is no page number and no `count`.
- The response is `{"previous": ..., "next": ..., "results": [...]}`; note `results`, not `items`. `next` keeps the other query parameters, adds `cursor`, and is `null` on the last page.
- The cursor is a position, not an offset, so inserts do not cause skipped or repeated items when following the same `next` link.
- It fetches one extra row to detect a next page, so there is no `COUNT` query: fast on large tables, but a UI cannot show "page 3 of 5".
- The cursor is encoded, not signed. A crafted one can only move within the queryset the view returns. A cursor that is not valid base64 returns a `422` with `{"detail": [{"cursor": "Invalid Cursor"}]}`.

Choose page numbers when the UI needs totals; choose cursors for feeds and large tables.

## Checked

2026-11-07: Confirmed against tutorial/part-5.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
