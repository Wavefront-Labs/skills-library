---
id: computing-software.web-development.django.drf-nested-writable-serializers
name: drf-nested-writable-serializers
category: computing-software
field: web-development
product: django
tags: [nested-serializers, writable-nested-serializers, drf-serializers, django-rest-framework, django]
level: advanced
status: verified
description: "Writable nested serializers in DRF: create and update for parent and children, nested validation, transactions, matching child ids, and flat alternatives."
sources:
  - https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
  - https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
  - https://github.com/beda-software/drf-writable-nested
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writable nested serializers

DRF nested serializers are read-only by default for writes: `.create()`/`.update()` raise errors with nested data unless you implement them.

## 1. Create
```python
class LineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)            # needed to match on update
    class Meta: model = OrderLine; fields = ["id", "product", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    lines = LineSerializer(many=True)
    class Meta: model = Order; fields = ["id", "customer", "note", "lines"]

    def validate_lines(self, lines):
        if not lines: raise serializers.ValidationError("At least one line is required.")
        return lines

    @transaction.atomic
    def create(self, validated):
        lines = validated.pop("lines")
        order = Order.objects.create(**validated)
        OrderLine.objects.bulk_create(OrderLine(order=order, **l) for l in lines)
        return order
```

## 2. Update with child matching
```python
    @transaction.atomic
    def update(self, order, validated):
        lines = validated.pop("lines", None)
        for k, v in validated.items(): setattr(order, k, v)
        order.save()
        if lines is not None:                                   # PATCH without lines leaves them alone
            existing = {l.id: l for l in order.lines.all()}
            keep = set()
            for data in lines:
                lid = data.pop("id", None)
                if lid in existing:
                    line = existing[lid]
                    for k, v in data.items(): setattr(line, k, v)
                    line.save(); keep.add(lid)
                elif lid is None:
                    keep.add(OrderLine.objects.create(order=order, **data).id)
                else:
                    raise serializers.ValidationError({"lines": [f"Line {lid} does not belong to this order."]})
            order.lines.exclude(id__in=keep).delete()
        return order
```
- Reject child ids from other parents (IDOR via nested ids).
- Decide and document semantics: does omitting a child delete it (replace) or keep it (merge)?
- Wrap in a transaction so partial failures roll back.
- Prefetch `lines` in the viewset queryset to avoid N+1 on reads.

## 3. Libraries and alternatives
- `drf-writable-nested` implements this generically (`WritableNestedModelSerializer`); review its update semantics before adopting.
- Often simpler: separate endpoints for children (`/orders/1/lines/`), or accept primary keys (`PrimaryKeyRelatedField`) for existing related objects instead of nested writes.

## 4. Validation errors
Nested errors for `many=True` come back keyed by the input index in DRF 3.18: `{"lines": {"1": {"quantity": ["A valid integer is required."]}}}` - clients map them by index. Older DRF returned a list aligned with the input (`[{}, {...}]`); that format is deprecated and will be removed in DRF 3.20, and `REST_FRAMEWORK["LIST_SERIALIZER_ERRORS_AS_DICT"] = False` still selects it with a warning.

## Verify
- [ ] Create, replace, partial update and child deletion covered by tests; foreign child ids rejected; failures leave no partial writes.

## Checked
Django 6.1.2, DRF 3.18.3, drf-spectacular 0.30.0 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: the create and update code as written. POST created the order and its lines; PATCH without `lines` kept the lines; PUT with `[{id, qty 5}, {no id}]` updated one line and created one; PUT with a single new line deleted the omitted ones; a line id belonging to another order -> 400 (the original message was a bare string, now a list); a bad quantity on the second line gave an index-keyed error.
- Run: a plain `ModelSerializer` with a nested `many=True` field and no `create()` raised `AssertionError: The .create() method does not support writable nested fields by default.`
- Found: DRF 3.18.3 `ListSerializer` errors are `{index: errors}` by default; the old list format needs `LIST_SERIALIZER_ERRORS_AS_DICT = False` and warns that it is removed in 3.20 (serializers.py source; 3.18.2 release notes mention the compatibility setting).
- Checked: `drf-writable-nested` 0.7.2 exists on PyPI.
