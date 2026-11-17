---
id: computing-software.web-development.django.postgres-full-text-search-and-arrayfield
name: postgres-full-text-search-and-arrayfield
category: computing-software
field: web-development
product: django
tags: [django-full-text-search, arrayfield, searchvector, trigramsimilarity, gin-index, django]
level: advanced
status: docs-checked
description: "Using django.contrib.postgres: ArrayField lookups, full-text search with SearchVector/SearchQuery/SearchRank and stored tsvectors, trigram similarity, GIN indexes and extensions."
sources:
  - https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/
  - https://docs.djangoproject.com/en/stable/ref/contrib/postgres/fields/
  - https://www.postgresql.org/docs/current/textsearch.html
  - https://www.postgresql.org/docs/current/pgtrgm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Postgres full-text search and ArrayField

Add `"django.contrib.postgres"` to `INSTALLED_APPS`.

## 1. ArrayField
```python
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
class Article(models.Model):
    tags = ArrayField(models.CharField(max_length=40), default=list, blank=True)
    class Meta: indexes = [GinIndex(fields=["tags"])]
Article.objects.filter(tags__contains=["django"])      # has all
Article.objects.filter(tags__overlap=["django", "vue"]) # has any
Article.objects.filter(tags__len__gt=3)
```
Good for small denormalised lists; use a related table when items need attributes or referential integrity.

## 2. Full-text search
```python
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
vector = SearchVector("title", weight="A", config="english") + SearchVector("body", weight="B", config="english")
query = SearchQuery(q, search_type="websearch", config="english")   # websearch syntax (quoted phrases, OR, - exclusion); needs PostgreSQL 11+
results = (Article.objects.annotate(rank=SearchRank(vector, query))
           .filter(rank__gte=0.05).order_by("-rank"))
```
Computing vectors per query is slow on big tables. Store them:
```python
from django.contrib.postgres.search import SearchVectorField
class Article(models.Model):
    search = models.GeneratedField(
        expression=SearchVector("title", weight="A", config="english") + SearchVector("body", weight="B", config="english"),
        output_field=SearchVectorField(), db_persist=True)       # Django 5.0+
    class Meta: indexes = [GinIndex(fields=["search"])]
Article.objects.filter(search=query)
```
(Older versions: `SearchVectorField` updated by a trigger or `update(search=vector)` in a signal/task.)
Highlight snippets with `SearchHeadline`.

## 3. Fuzzy matching (typos, names)
```python
from django.contrib.postgres.operations import TrigramExtension   # in a migration: operations = [TrigramExtension()]
from django.contrib.postgres.search import TrigramSimilarity
Author.objects.annotate(sim=TrigramSimilarity("name", q)).filter(sim__gt=0.3).order_by("-sim")
```
Index with `GinIndex(fields=["name"], opclasses=["gin_trgm_ops"], name="author_name_trgm")`.

## 4. When to move on
For needs beyond PostgreSQL text search, consider a dedicated search engine.

## Verify
- [ ] `EXPLAIN` shows the GIN index used for search queries; websearch syntax ("exact phrase", -term) behaves as expected.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (ref/contrib/postgres/search, fields, operations, indexes), PostgreSQL master docs (textsearch websearch_to_tsquery, pgtrgm).
Confirmed: `ArrayField` lookups (`contains`, `overlap`, `len`), `SearchVector`, `SearchQuery(search_type="websearch")` requiring PostgreSQL 11+, `SearchRank`, `SearchHeadline`, `GeneratedField(..., db_persist=True)` with `SearchVectorField` (Django 5.0), `TrigramExtension`, `TrigramSimilarity`, `GinIndex`, `opclasses=["gin_trgm_ops"]`, websearch quote, OR and dash semantics.
Corrected or removed: the unsupported statements about when to move to OpenSearch, Meilisearch or Typesense.
Method: documentation only; no commands were run.
