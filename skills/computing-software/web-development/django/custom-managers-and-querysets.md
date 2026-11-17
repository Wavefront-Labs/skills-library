---
id: computing-software.web-development.django.custom-managers-and-querysets
name: custom-managers-and-querysets
category: computing-software
field: web-development
product: django
tags: [django, model-managers, custom-querysets, as-manager, orm, chainable-queries, python, web-development]
level: practitioner
status: verified
description: "Encapsulating query logic in Django custom QuerySets and managers: chainable methods, as_manager/from_queryset, default manager pitfalls and related managers."
sources:
  - https://docs.djangoproject.com/en/stable/topics/db/managers/
  - https://docs.djangoproject.com/en/stable/ref/models/querysets/
  - https://docs.djangoproject.com/en/stable/ref/models/options/#default-manager-name
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom managers and querysets

**Goal:** query rules (published, visible to user, active) defined once and chainable everywhere.

## 1. QuerySet methods first
```python
class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published", published_at__lte=timezone.now())
    def by(self, user):
        return self.filter(author=user)
    def with_comment_count(self):
        return self.annotate(n_comments=models.Count("comments"))

class Article(models.Model):
    ...
    objects = ArticleQuerySet.as_manager()
```
```python
Article.objects.published().by(request.user).with_comment_count().order_by("-published_at")
```
Methods on the QuerySet chain in any order; methods only on a Manager don't chain.

## 2. Manager with extra non-chainable helpers
```python
class ArticleManager(models.Manager.from_queryset(ArticleQuerySet)):
    def create_draft(self, **kw):
        return self.create(status="draft", **kw)
```

## 3. Overriding get_queryset - carefully
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")

class Article(models.Model):
    objects = models.Manager()          # declare first: becomes the default manager
    published = PublishedManager()
```
The **first** manager defined is `_default_manager`, used by the admin, `dumpdata`, related lookups in some cases, and generic views. A filtering default manager hides rows from the admin and can break data migrations. Set `Meta.default_manager_name` explicitly when in doubt. `Meta.base_manager_name` controls related-object access (`article.author`) - never filter there.

## 4. Soft delete pattern
```python
class SoftDeleteQuerySet(models.QuerySet):
    def delete(self): return self.update(deleted_at=timezone.now())
    def alive(self): return self.filter(deleted_at__isnull=True)
```
Expose `objects = ... .alive()`-style manager plus `all_objects`. Add a partial unique constraint `condition=Q(deleted_at__isnull=True)` so soft-deleted rows don't block re-creation. `QuerySet.delete()` is overridden here, but `instance.delete()` is not: it still hard-deletes the row (override `Model.delete()` too).

## 5. Related managers
`author.article_set.published()` works because reverse relations use the default manager's class with QuerySet methods.

## 6. Where logic belongs
Query filters -> QuerySet. Row behaviour -> model methods. Multi-model workflows -> service functions.

## Verify
- [ ] Views contain no repeated `filter(status="published", ...)` (grep).
- [ ] Admin still shows all rows (default manager unfiltered).
- [ ] Unit tests for each QuerySet method using `assertQuerySetEqual`.

## Checked
Django 6.1.2, DRF 3.18.3, drf-spectacular 0.30.0 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: `ArticleQuerySet.as_manager()` chain `published().by(user).with_comment_count().order_by(...)` returned the annotated row; `Manager.from_queryset(...)` with `create_draft` worked; `user.article_set.published()` works on the reverse manager.
- Run: the first declared manager is `_default_manager` (a filtering `published` manager declared first hid the draft row from the default manager; declared second it did not); `_base_manager` is a plain Manager.
- Run: soft-delete QuerySet `delete()` set `deleted_at`, the partial `UniqueConstraint(condition=Q(deleted_at__isnull=True))` allowed re-creating the slug and blocked a second live duplicate (IntegrityError); `instance.delete()` hard-deleted the row.
- Checked: `TestCase.assertQuerySetEqual` exists.
