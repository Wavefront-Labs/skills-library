---
id: computing-software.web-development.django.model-inheritance
name: model-inheritance
category: computing-software
field: web-development
product: django
tags: [model-inheritance, proxy-models, abstract-models, multi-table-inheritance, django-orm, django]
level: practitioner
status: verified
description: "Choosing Django model inheritance: abstract bases, multi-table inheritance and its join cost, proxy models, related_name placeholders and Meta inheritance."
sources:
  - https://docs.djangoproject.com/en/stable/topics/db/models/#model-inheritance
  - https://docs.djangoproject.com/en/stable/topics/db/models/#proxy-models
  - https://django-polymorphic.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model inheritance

## 1. Abstract base classes (default choice)
```python
class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name="%(app_label)s_%(class)s_created")
    class Meta:
        abstract = True
        ordering = ["-created_at"]

class Invoice(TimeStamped):
    number = models.CharField(max_length=20, unique=True)
```
No table for the base; fields are copied into each child table. Use `%(class)s` / `%(app_label)s` in `related_name` or reverse accessors clash. Children inherit abstract `Meta` (ordering etc.) only if they declare no `Meta` of their own; a child with its own `class Meta:` loses the parent's `ordering` unless it extends it: `class Meta(TimeStamped.Meta): ...` (measured: ordering `['-x']` kept with `Meta(Base.Meta)`, `[]` with a bare `Meta`).

## 2. Multi-table inheritance (concrete parent)
```python
class Place(models.Model): name = models.CharField(max_length=100)
class Restaurant(Place): serves_pizza = models.BooleanField(default=False)
```
Two tables joined by an implicit `OneToOneField` (`place_ptr`). Every `Restaurant` query joins `Place`; `Place.objects.all()` returns `Place` instances (access `place.restaurant` to downcast, one query each). Useful when you genuinely need to query all parents together; otherwise the join cost and awkward downcasting make it a poor default. `django-polymorphic` returns the right subclasses automatically (with extra queries).

## 3. Proxy models
```python
class PublishedPost(Post):
    objects = PublishedManager()
    class Meta:
        proxy = True
        verbose_name = "published post"
```
Same table, different Python behaviour: managers, methods, default ordering, a separate admin registration, different permissions. Cannot add fields.

## 4. Decision
| Need | Use |
|---|---|
| Share fields/methods, query children separately | abstract |
| Query all subtypes as one set, subtype-specific fields | multi-table (or one table + JSONField / nullable columns) |
| Same data, different behaviour or admin | proxy |

## Gotchas
- Changing between inheritance styles later needs data migrations; decide early.
- Constraints/indexes in an abstract `Meta` need `%(app_label)s_%(class)s` in their `name` (documented in the constraints reference; the name became `shop_d1_x_pos` for child `D1`).

## Verify
- [ ] `print(Restaurant.objects.all().query)` shows the expected join (or none for abstract); migrations create the intended tables.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: abstract base with `related_name="%(app_label)s_%(class)s_created"` created distinct reverse accessors `shop_invoice_created` and `shop_receipt_created`; `Invoice.objects.all().query` has no join; abstract `Meta.ordering` is inherited by a child only when the child's Meta extends the parent's.
- Run: multi-table `Restaurant(Place)` has an implicit `OneToOneField` `place_ptr`, its query joins `shop_place`, `Place.objects.get()` returns a `Place` and `place.restaurant` downcasts; a proxy model shares the parent's table and `concrete_model`.
- Run: `%(app_label)s_%(class)s_x_pos` expanded per child. Fetched: topics/db/models.txt (abstract related_name rules) and ref/models/constraints.txt (name placeholders).
