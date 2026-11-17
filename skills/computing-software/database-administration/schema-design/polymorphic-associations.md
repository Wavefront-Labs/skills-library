---
id: computing-software.database-administration.schema-design.polymorphic-associations
name: polymorphic-associations
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-patterns, polymorphic-association, exclusive-arcs, supertype-table, foreign-keys, commentable, referential-integrity]
level: practitioner
status: verified
description: "Model one table referencing several parent types (comments on posts or photos) with exclusive-arc FKs or a supertype table instead of type+id columns without FKs."
sources:
  - https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/
  - https://guides.rubyonrails.org/association_basics.html#polymorphic-associations
  - https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-CHECK-CONSTRAINTS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polymorphic associations

**Goal:** "a comment belongs to a post OR a photo OR a video" with real referential integrity.

## The ORM default (and its problem)
```sql
CREATE TABLE comments (id bigint PRIMARY KEY, commentable_type text, commentable_id bigint, body text);
```
`commentable_id` cannot have a foreign key (it points to different tables), so orphans and wrong-type IDs accumulate; deletes do not cascade; joins need a CASE per type.

## Option 1: exclusive arcs (nullable FK per parent + CHECK)
```sql
CREATE TABLE comments (
  id bigint PRIMARY KEY,
  post_id  bigint REFERENCES posts(id)  ON DELETE CASCADE,
  photo_id bigint REFERENCES photos(id) ON DELETE CASCADE,
  body text NOT NULL,
  CHECK (num_nonnulls(post_id, photo_id) = 1)       -- PostgreSQL; elsewhere: (post_id IS NOT NULL)::int + ... = 1
);
CREATE INDEX ON comments (post_id) WHERE post_id IS NOT NULL;
CREATE INDEX ON comments (photo_id) WHERE photo_id IS NOT NULL;
```
Good for a handful of parent types; adding a type = add a column.

## Option 2: supertype table (common parent)
```sql
CREATE TABLE commentables (id bigint PRIMARY KEY, kind text NOT NULL CHECK (kind IN ('post','photo')));
CREATE TABLE posts  (id bigint PRIMARY KEY REFERENCES commentables(id), ...);
CREATE TABLE photos (id bigint PRIMARY KEY REFERENCES commentables(id), ...);
CREATE TABLE comments (id bigint PRIMARY KEY, commentable_id bigint NOT NULL REFERENCES commentables(id), body text);
```
Scales to many types; parents get IDs from the supertype. To ensure a post's ID is of kind 'post', add `kind` to the child with a composite FK `(id, kind)`.

## Option 3: separate join tables
`post_comments(post_id, comment_id)`, `photo_comments(photo_id, comment_id)` with FKs. Simple, but "all comments of X" needs a UNION.

## Keeping the ORM
ORM polymorphic relations (Rails `polymorphic: true`, Django generic relations) store type+id by default; they can be rebuilt on option 1 (custom accessors) or option 2 (parent model). If you keep type+id, add triggers or periodic orphan checks.

## Verify
Deleting a post removes its comments; inserting a comment with both or neither parent fails the CHECK (all three checked on PostgreSQL 18); an orphan check query returns 0 rows.
