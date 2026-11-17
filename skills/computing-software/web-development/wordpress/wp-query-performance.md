---
id: computing-software.web-development.wordpress.wp-query-performance
name: wp-query-performance
category: computing-software
field: web-development
product: wordpress
tags: [wp-query, pre-get-posts, meta-query, no-found-rows, wordpress-performance, wordpress]
level: practitioner
status: docs-checked
description: "Efficient WP_Query: key arguments, pre_get_posts for the main query, avoiding slow meta queries and posts_per_page -1, cache flags, resetting postdata."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-query.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/query.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-meta-query.php
  - https://developer.wordpress.org/reference/hooks/pre_get_posts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WP_Query performance

## 1. A good custom query
```php
$q = new WP_Query([
  'post_type'              => 'event',
  'post_status'            => 'publish',
  'posts_per_page'         => 12,
  'paged'                  => max(1, get_query_var('paged')),
  'tax_query'              => [[ 'taxonomy' => 'event_type', 'field' => 'slug', 'terms' => ['workshop'] ]],
  'orderby'                => 'date',
  'order'                  => 'DESC',
  'no_found_rows'          => false,    // true when you do not paginate: skips counting total rows
  'update_post_term_cache' => true,
  'update_post_meta_cache' => true,
]);
while ($q->have_posts()) { $q->the_post(); get_template_part('parts/event-card'); }
wp_reset_postdata();
```
- `fields => 'ids'` when you only need ids; `no_found_rows => true` + `update_post_meta_cache => false` for widgets/related posts.
- Never `posts_per_page => -1` on unbounded data; paginate or cap.

## 2. Change the main query, do not replace it
```php
add_action('pre_get_posts', function (WP_Query $query) {
  if (is_admin() || !$query->is_main_query()) return;
  if ($query->is_post_type_archive('event')) {
    $query->set('posts_per_page', 12);
    $query->set('meta_key', 'event_date');
    $query->set('orderby', 'meta_value');
    $query->set('order', 'ASC');
  }
});
```
Do not use `query_posts()`: the core docblock says it completely overrides the main query, is not intended for plugins or themes, and recommends `pre_get_posts` instead.

## 3. Meta queries are slow
Filtering or sorting by meta values joins the postmeta table and can be slow on large sites. Prefer:
- taxonomies for filterable attributes (indexed term relationships);
- `meta_key` existence/equality on small sets, with the clause `type` (for example `NUMERIC`, `DATE`, `DATETIME`) set for correct comparisons;
- a custom table for heavy structured data;
- avoiding `LIKE '%...%'` and `OR` meta relations.

## 4. Cache
Wrap expensive queries in transients or the object cache keyed by their arguments, and invalidate on `save_post_{$post_type}`.

## 5. Measure
Use a query logger (for example `SAVEQUERIES` or a profiling plugin) to look for duplicate queries and slow meta joins.

## Verify
- [ ] Archive pages run few queries and no `-1` limits on unbounded types.

## Checked

2026-10-25: against wordpress-develop trunk source (`class-wp-query.php`, `query.php`, `class-wp-meta-query.php`; last commit 2026-10-25). Confirmed: `no_found_rows`, `update_post_term_cache` and `update_post_meta_cache` arguments (defaults true), `query_posts()` docblock warning and `pre_get_posts` recommendation, meta clause `type` values (NUMERIC, DATE, DATETIME and others). Removed unconfirmed claims about the LONGTEXT column, an index absence, persistent object cache behaviour, Query Monitor and the 50 ms threshold.

Method: documentation only; no commands were run.
