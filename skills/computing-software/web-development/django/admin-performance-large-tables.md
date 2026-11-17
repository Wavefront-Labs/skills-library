---
id: computing-software.web-development.django.admin-performance-large-tables
name: admin-performance-large-tables
category: computing-software
field: web-development
product: django
tags: [django-admin, admin-performance, list-select-related, show-full-result-count, paginator, admin-queries, large-tables]
level: practitioner
status: docs-checked
description: "Keeping Django admin fast on large tables: select_related, avoiding COUNT(*) with show_full_result_count, custom paginators, indexed search and FK widgets."
sources:
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.show_full_result_count
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.paginator
  - https://docs.djangoproject.com/en/stable/topics/db/optimization/
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/filters/
  - https://www.postgresql.org/docs/current/catalog-pg-class.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admin performance on large tables

**Goal:** admin changelists and edit pages stay fast on tables with millions of rows.

## 1. Find the slow queries
django-debug-toolbar on the admin page (or `django.db.backends` logging): look for N+1 queries per row, `COUNT(*)` on the whole table, `LIKE '%…%'` scans and huge `<select>` option lists.

## 2. Fixes
| Symptom | Fix |
|---|---|
| One query per row for FK columns | `list_select_related = ("customer", "customer__account")` |
| Computed column hitting related managers | Annotate in `get_queryset` (`.annotate(line_count=Count("lines"))`) and display the annotation |
| Extra full-table `COUNT(*)` for the "(N total)" figure on filtered pages | `show_full_result_count = False` (shows "(Show all)" instead of the total) |
| Count still slow on Postgres | Custom paginator using the planner estimate (`pg_class.reltuples` is only an estimate and is `-1` if the table was never vacuumed or analyzed) when unfiltered: `SELECT reltuples FROM pg_class WHERE relname=…` |
| Search scanning the table | Prefix/exact lookups (`^field`, `=field`) on indexed columns, trigram GIN index for `icontains`, or Postgres full-text search via `get_search_results` override |
| Edit page renders 100k-option selects | `autocomplete_fields` or `raw_id_fields` |
| `list_filter` on FK builds a huge option list | `RelatedOnlyFieldListFilter` (lists only related objects that are in use) or a custom `SimpleListFilter` |
| Sorting by unindexed column | Restrict `sortable_by` to indexed columns |

```python
class EstimatedCountPaginator(Paginator):
    @cached_property
    def count(self):
        if self.object_list.query.where:            # filtered: real count
            return super().count
        with connection.cursor() as c:
            c.execute("SELECT reltuples::bigint FROM pg_class WHERE relname = %s", [self.object_list.model._meta.db_table])
            return c.fetchone()[0]
class EventAdmin(admin.ModelAdmin):
    paginator = EstimatedCountPaginator
    show_full_result_count = False
```

## 3. Changelist defaults
`list_per_page` sets the page size; `list_max_show_all` (default 200) controls when the "Show all" link appears.

## Verify
- [ ] Changelist renders in < 1 s with ~constant query count.
- [ ] No sequential scans in `EXPLAIN` for default list + common filters.
- [ ] Edit page with FKs loads without giant selects.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (ref/contrib/admin and filters pages), PostgreSQL master docs (pg_class, pg_trgm).
Confirmed: `show_full_result_count`, `list_select_related`, `paginator`, `sortable_by`, `autocomplete_fields`, `raw_id_fields`, `RelatedOnlyFieldListFilter`, search prefixes (`^`, `=`, `@`), `list_per_page`, `list_max_show_all`, `reltuples` semantics, trigram indexes for LIKE and ILIKE.
Corrected or removed: the "two COUNT queries" and "(N total)" description (the setting avoids one full-table count and shows "Show all"); the unsupported date_hierarchy index advice, autocomplete filter package and default-ordering advice.
Method: documentation only; no commands were run.
