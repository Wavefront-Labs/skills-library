---
id: computing-software.web-development.wordpress.shortcodes
name: shortcodes
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, shortcodes, add-shortcode, shortcode-atts, output-escaping, php, web-development]
level: practitioner
status: docs-checked
description: "Writing WordPress shortcodes safely: add_shortcode handlers that return output, shortcode_atts defaults, escaping, enclosing content, asset loading and block alternatives."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/shortcodes.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/default-filters.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/widgets/class-wp-widget-text.php
  - https://developer.wordpress.org/plugins/shortcodes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shortcodes

**Goal:** shortcodes that return escaped markup, accept validated attributes, and don't break the page layout.

## 1. Register
```php
add_action( 'init', function () {
    add_shortcode( 'acme_events', 'acme_events_shortcode' );
} );

function acme_events_shortcode( $atts, $content = null, $tag = '' ) {
    $atts = shortcode_atts( [ 'count' => 5, 'category' => '' ], $atts, $tag );   // $tag enables shortcode_atts_{tag} filter
    $count = min( 20, max( 1, absint( $atts['count'] ) ) );
    $q = new WP_Query( [
        'post_type' => 'event', 'posts_per_page' => $count, 'no_found_rows' => true,
        'category_name' => sanitize_title( $atts['category'] ),
    ] );
    ob_start();
    echo '<ul class="acme-events">';
    while ( $q->have_posts() ) { $q->the_post();
        printf( '<li><a href="%s">%s</a></li>', esc_url( get_permalink() ), esc_html( get_the_title() ) );
    }
    echo '</ul>';
    wp_reset_postdata();
    return ob_get_clean();                       // RETURN, never echo
}
```
A shortcode handler must return its output; echoing prints it before the surrounding content instead of in place.

## 2. Attributes are untrusted
Anyone who can edit post content can write shortcodes with arbitrary attributes. Treat every attribute as untrusted input: cast, allowlist, escape.

## 3. Enclosing shortcodes
```php
add_shortcode( 'acme_note', function ( $atts, $content = null ) {
    return '<aside class="acme-note">' . do_shortcode( wp_kses_post( $content ) ) . '</aside>';
} );
```
`[acme_note]Text with [other]shortcodes[/other][/acme_note]` - call `do_shortcode()` to process nested ones.

## 4. Assets only when used
Enqueue inside the handler: `wp_enqueue_style( 'acme-events' )` (registered earlier) - a style enqueued while the content renders may print late, so for critical CSS check `has_shortcode( $post->post_content, 'acme_events' )` in `wp_enqueue_scripts`.

## 5. Naming and conflicts
Prefix tags (`acme_`). `add_shortcode()` rejects empty names and names containing spaces or the reserved characters `& / < > [ ] =`. Core runs `do_shortcode` on `the_content`, on text widget content (`widget_text_content`) and on block widget content (`widget_block_content`); elsewhere call `do_shortcode()` yourself.

## 6. Prefer blocks for new UI
Blocks give editor previews and structured attributes. Keep shortcodes for backward compatibility or classic-editor sites.

## Verify
- [ ] `[acme_events count="9999" category="<script>"]` renders safely and caps the count.
- [ ] Output appears in place, not at the top of the content.
- [ ] Shortcode assets load only on pages using it.

## Checked

2026-10-25: against wordpress-develop trunk source (`shortcodes.php`, `default-filters.php`, `class-wp-widget-text.php`; last commit 2026-10-25). Confirmed: `add_shortcode( $tag, $callback )` name validation and reserved characters, `shortcode_atts( $pairs, $atts, $shortcode )` and the `shortcode_atts_{$shortcode}` filter, `has_shortcode`, `do_shortcode` filters on `the_content`, `widget_text_content` and `widget_block_content`. Removed unconfirmed claims about hyphen conflicts, footer style printing, CVE frequency and `widget_text` since 4.9.

Method: documentation only; no commands were run.
