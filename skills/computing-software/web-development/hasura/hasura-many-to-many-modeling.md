---
id: computing-software.web-development.hasura.hasura-many-to-many-modeling
name: hasura-many-to-many-modeling
category: computing-software
field: web-development
product: hasura
tags: [hasura, many-to-many, junction-table, relationships, data-modeling]
level: practitioner
status: docs-checked
description: "Model a many-to-many link in Hasura with a bridge table, two foreign keys, and relationships from both sides through the bridge."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/common-patterns/data-modeling/many-to-many.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: relate articles and tags in both directions.

Steps from the docs:
1. Create a bridge table, for example:

```sql
article_tag (
  id SERIAL PRIMARY KEY,
  article_id INT,
  tag_id INT,
  UNIQUE (article_id, tag_id)
)
```
The unique constraint can be skipped if the same pair may appear several times.
2. Add foreign keys from `article_id` to `articles(id)` and from `tag_id` to `tags(id)`.
3. Create relationships (names as in the docs):
   - on `articles`: array relationship `article_tags` using `article_tag :: article_id -> id`,
   - on `tags`: array relationship `tag_articles` using `article_tag :: tag_id -> id`,
   - on `article_tag`: object relationship `tag` (using `tag_id`) and object relationship `article` (using `article_id`).
4. Query through the bridge: `articles { article_tags { tag { tag_value } } }`, or from the other side `tags { tag_articles { article { title } } }`.

Insert related data in one request with nested inserts: pass `article_tags: { data: [ { tag: { data: {...}, on_conflict: {...} } } ] }` on the article. The docs use `on_conflict` so a tag that already exists does not fail; it can be left out if conflicts never happen.

Extra columns on the bridge table (the docs use `tagged_at`) can be fetched through `article_tags`.

Gotcha: queries go through the intermediate fields `article_tags` and `tag_articles`. The docs describe flattening with extra views, but advise against it because permissions and relationships then have to be managed on the views too.

## Checked
2026-11-07. Read in full the single cited page (many-to-many.mdx, as shown in the GitHub file view; it embeds no snippet files, only GraphiQL query components which were read inline).
Confirmed: bridge table with unique constraint note, foreign keys, the four relationships and their names, the nested insert shape with `data` and `on_conflict`, the `tagged_at` example, the flattening-view caution.
Removed: "Track all three tables" (the page does not say it), the invented Verify step, and the claim that no direct articles-to-tags field exists (reworded to what the page says about views).
Method: documentation only; no commands were run.
