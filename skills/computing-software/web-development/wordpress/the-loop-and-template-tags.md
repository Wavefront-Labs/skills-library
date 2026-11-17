---
id: computing-software.web-development.wordpress.the-loop-and-template-tags
name: the-loop-and-template-tags
category: computing-software
field: web-development
product: wordpress
tags: [the-loop, wordpress-template-tags, wp-query, classic-themes, wordpress]
level: intro
status: docs-checked
description: "The Loop and template tags in classic WordPress themes: have_posts and the_post, conditional tags, custom WP_Query loops, wp_reset_postdata and pagination."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/post-template.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/general-template.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/query.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-query.php
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The Loop and template tags

## 1. The main loop
```php
<?php if ( have_posts() ) : ?>
  <?php while ( have_posts() ) : the_post(); ?>
    <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
      <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
      <p class="meta"><?php echo esc_html( get_the_date() ); ?> · <?php the_author(); ?></p>
      <?php if ( has_post_thumbnail() ) the_post_thumbnail( 'card' ); ?>
      <?php the_excerpt(); ?>
    </article>
  <?php endwhile; ?>
  <?php the_posts_pagination( [ 'mid_size' => 1 ] ); ?>   <?php // mid_size default is 2 ?>
<?php else : ?>
  <p><?php esc_html_e( 'Nothing found.', 'acme' ); ?></p>
<?php endif; ?>
```
- `the_post()` sets the global `$post` and post data so template tags work.
- WordPress already ran the main query from the URL; modify it with `pre_get_posts` rather than a new query in the template.

## 2. Template tags: echo vs get
`the_title()` echoes the current post title (pass `$display = false` to return it); `get_the_title()` returns it. Escape returned values yourself when outputting in attributes: `esc_attr( get_the_title() )`. `the_content()` applies `the_content` filters (blocks, shortcodes, embeds) - use it, not raw `$post->post_content`.

## 3. Conditional tags
`is_front_page()`, `is_home()` (blog posts index), `is_singular( 'product' )`, `is_page( 'about' )`, `is_archive()`, `is_category( 'news' )`, `is_search()`, `is_404()`. Only reliable after the main query runs (`wp` action or later).

## 4. Custom secondary loops
```php
$related = new WP_Query( [ 'post_type' => 'post', 'posts_per_page' => 3, 'post__not_in' => [ get_the_ID() ],
    'category__in' => wp_get_post_categories( get_the_ID() ), 'no_found_rows' => true, 'ignore_sticky_posts' => true ] );
while ( $related->have_posts() ) : $related->the_post(); get_template_part( 'parts/card' ); endwhile;
wp_reset_postdata();    // restore the main loop's $post
```
- Always `wp_reset_postdata()` after a custom loop's `the_post()`; avoid `query_posts()`, whose docblock says it completely overrides the main query.
- `no_found_rows => true` skips counting total rows when you don't paginate.

## 5. Modifying the main query
```php
add_action( 'pre_get_posts', function ( $q ) {
    if ( ! is_admin() && $q->is_main_query() && $q->is_post_type_archive( 'event' ) ) {
        $q->set( 'meta_key', 'start_date' ); $q->set( 'orderby', 'meta_value' ); $q->set( 'order', 'ASC' );
    }
} );
```

## Verify
- [ ] Archive pagination works including page 2+; no `query_posts`; custom loops reset postdata; output escaped where get_ functions are used.

## Checked

2026-10-25: against wordpress-develop trunk source (`post-template.php`, `general-template.php`, `query.php`, `class-wp-query.php`; last commit 2026-10-25). Confirmed: `the_title( $before, $after, $display )` signature, `the_posts_pagination` `mid_size` (default 2), `wp_reset_postdata`, `query_posts()` docblock warning, `no_found_rows`. Removed the unconfirmed claim that `the_title()` escapes for display.

Method: documentation only; no commands were run.
