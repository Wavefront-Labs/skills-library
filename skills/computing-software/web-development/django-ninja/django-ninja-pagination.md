---
id: computing-software.web-development.django-ninja.django-ninja-pagination
name: django-ninja-pagination
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, pagination-paginate, pagination, paginate, cursor, limitoffset, async]
level: advanced
status: docs-checked
description: "Paginate Django Ninja list endpoints with @paginate, the built-in pagination classes, RouterPaginated, and custom or async paginators."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/pagination.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Paginate Django Ninja endpoints

Goal: return pages with metadata for list responses.

```python
from ninja.pagination import paginate

@api.get("/users", response=list[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```

`GET /api/users?limit=10&offset=0` returns `{"items": [...], "count": 57}`. Default `limit` is 100 (`NINJA_PAGINATION_PER_PAGE`); the default class comes from `NINJA_PAGINATION_CLASS` (`LimitOffsetPagination`). Pass a class to override: `@paginate(PageNumberPagination)`.

## Built-in classes
- `LimitOffsetPagination`: `limit` (100), `offset` (0); `max_limit` argument defaults to `NINJA_PAGINATION_MAX_LIMIT`.
- `PageNumberPagination`: `page` (from 1), `page_size`; constructor `page_size` defaults to `NINJA_PAGINATION_PER_PAGE`, client `page_size` capped by `max_page_size` (`NINJA_MAX_PER_PAGE_SIZE`, 100). Example: `@paginate(PageNumberPagination, page_size=50)`.
- `CursorPagination`: `cursor`, `page_size`; response has `next`, `previous` and `results` (its `items_attribute`). Args: `ordering` (default `("-pk",)` via `NINJA_PAGINATION_DEFAULT_ORDERING`; first field encodes position, should be near-unique), `page_size`, `max_page_size`.

```python
@paginate(CursorPagination, ordering=("date_joined", "id"), page_size=20)
```

## In the view
`@paginate(pass_parameter="pagination_info")` with `def list_users(request, **kwargs)` gives `kwargs["pagination_info"]`, the paginator's `Input` instance (`.limit`, `.page`, `.cursor`, ...).

## Async
`async def` views work with built-in classes (`apaginate_queryset` is called).

## Whole router or API

```python
from ninja.pagination import RouterPaginated
router = RouterPaginated()
api = NinjaAPI(default_router=RouterPaginated())
```

Every list-`response` operation is paginated with `NINJA_PAGINATION_CLASS`.

## Custom paginator
Subclass `PaginationBase` with `Input`, `Output` and `paginate_queryset(self, queryset, pagination, **params)` returning a dict matching `Output`:

```python
class SkipPagination(PaginationBase):
    class Input(Schema):
        skip: int = 0
    class Output(Schema):
        items: list[Any]
        total: int
    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        return {"items": queryset[skip : skip + 5], "total": self._items_count(queryset)}
```

`params` holds the view's arguments (`params["request"]`). Set `items_attribute: str = "results"` if `Output` uses another key. For async, subclass `AsyncPaginationBase` and add `async def apaginate_queryset`, using `await self._aitems_count(queryset)`. A plain `PaginationBase` on an `async def` view raises `ConfigError`.

## Checked

2026-11-07: Confirmed against guide/pagination.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
