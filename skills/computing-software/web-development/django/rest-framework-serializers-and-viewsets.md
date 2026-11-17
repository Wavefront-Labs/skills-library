---
id: computing-software.web-development.django.rest-framework-serializers-and-viewsets
name: rest-framework-serializers-and-viewsets
category: computing-software
field: web-development
product: django
tags: [django, drf, django-rest-framework, serializers, viewsets, pagination, nested-writes, throttling, python, web-development, drf-serializers, drf-pagination, drf-throttling]
level: advanced
status: docs-checked
description: "Django REST Framework in practice: serializer validation order, ViewSet vs APIView tradeoffs, pagination defaults, and nested-write pitfalls."
sources:
  - https://www.django-rest-framework.org/api-guide/serializers/
  - https://www.django-rest-framework.org/api-guide/viewsets/
  - https://www.django-rest-framework.org/api-guide/pagination/
  - https://www.django-rest-framework.org/api-guide/settings/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Django REST Framework — serializers and viewsets in practice

**Goal:** build APIs where validation lives in one place, routing stays
declarative, and nested/related data doesn't silently fail to save.

## 1. Serializer validation order — know which hook runs when
1. Field-level: `to_internal_value` coerces, then each field's own validators run.
2. `validate_<field_name>(self, value)` — single-field custom checks.
3. `validate(self, attrs)` — cross-field checks (start date before end date).
Raise `serializers.ValidationError` at the earliest hook that can catch the
problem — a cross-field check belongs in `validate()`, not stuffed into one
field's `validate_x` with the other field pulled from `self.initial_data`
(fragile: `initial_data` is raw, unvalidated input, not the coerced value).

## 2. ViewSet vs APIView — pick by whether it's CRUD-shaped
- **`ModelViewSet`** + a router gives list/retrieve/create/update/destroy for
  free from one class, wired to standard REST URLs automatically
  (`router.register('orders', OrderViewSet)`). Use for genuine CRUD resources
  — this is most of a typical API.
- **`APIView`** (or a plain function with `@api_view`) when the endpoint isn't
  resource-CRUD-shaped: a `/reports/summary` aggregation, a `/checkout` action
  that does far more than create one row. Don't force a non-CRUD action into
  a ViewSet's `@action` decorator just to keep everything in one class if the
  logic doesn't actually fit the resource model — a plain view is often
  clearer.
- `@action(detail=True, methods=['post'])` on a ViewSet for a resource-scoped
  action (`/orders/5/cancel/`) is the right middle ground — still a CRUD
  resource, just a non-standard verb on it.

## 3. Pagination — set a sane default, don't ship unpaginated list endpoints
```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
}
```
Without a default, `ListAPIView`/`ModelViewSet.list()` returns every row —
fine with 50 test rows, an incident with 500,000 production rows. Cursor
pagination (`CursorPagination`) over offset-based for any list that's
actively being inserted into while paged through — DRF's docs say cursor
pagination never shows the same item twice when new items arrive, but it needs a
unique, unchanging ordering (default `-created`).

## 4. Nested writes — DRF requires explicit create() and update()
```python
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ["id", "customer", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        OrderItem.objects.bulk_create([OrderItem(order=order, **i) for i in items_data])
        return order
```
DRF's docs say the default `ModelSerializer.create()` and `.update()` do not support writable nested representations; the default methods raise an error (through `raise_errors_on_nested_writes`) instead of saving nested rows. Override `create`/`update` to pop the nested data and write the related rows explicitly.

## 5. Throttling and auth defaults worth setting explicitly
```python
"DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.UserRateThrottle"],
"DEFAULT_THROTTLE_RATES": {"user": "1000/day", "anon": "100/day"},
"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
```
DRF's out-of-the-box default permission is `AllowAny` — an API with no
explicit `DEFAULT_PERMISSION_CLASSES` override is open to the world by
default; set a deny-by-default posture at the settings level and open up
specific views explicitly, not the reverse.

## Verify
- [ ] Cross-field validation lives in `validate()`, not scattered across per-field validators reading `initial_data`.
- [ ] Every list endpoint has pagination; high-write lists use cursor pagination.
- [ ] Any serializer with nested writable fields has an explicit `create`/`update` override — verified with a test asserting the nested rows actually persisted.
- [ ] `DEFAULT_PERMISSION_CLASSES` defaults to authenticated, not DRF's `AllowAny` default.
- [ ] Throttle rates are set for both authenticated and anonymous traffic.

## Checked
Date: 2026-10-25. Documentation: Django REST framework docs source (encode/django-rest-framework main, commit of 2026-10-14: serializers, viewsets, pagination, throttling, settings) and `rest_framework/serializers.py`.
Confirmed: validation hooks (`validate_<field>`, `validate`), `ModelViewSet` with routers and `@action`, `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` default to none, cursor pagination behaviour, `DEFAULT_THROTTLE_RATES` format, `DEFAULT_PERMISSION_CLASSES` default `AllowAny`.
Corrected or removed: the claim that nested writes silently drop data with a 200 response (the default create raises an error through `raise_errors_on_nested_writes`), the "read-only by default" statement, and the offset-skip wording replaced by the documented cursor-pagination guarantee.
Method: documentation only; no commands were run.
