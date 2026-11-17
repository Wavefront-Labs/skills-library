---
id: computing-software.web-development.wordpress.template-hierarchy
name: template-hierarchy
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, template-hierarchy, classic-themes, block-themes, template-parts, template-include, php, web-development, wordpress-themes, theme-development]
level: practitioner
status: docs-checked
description: "Using the WordPress template hierarchy: how templates are chosen for each query type, classic PHP vs block theme templates, custom templates and debugging which file renders."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/template.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/template-loader.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/general-template.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-theme.php
  - https://developer.wordpress.org/themes/basics/template-hierarchy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template hierarchy

**Goal:** put each layout in the template WordPress will actually pick, and override narrowly.

## 1. How it works
WordPress resolves the main query (single post, page, archive, search, 404...) and walks a list of candidate template files from most to least specific, using the first that exists in the child theme, then parent theme. `index.php` (classic) / `templates/index.html` (block) is the final fallback.

## 2. Key chains
| Request | Candidates (first match wins) |
|---|---|
| Single post of type `book`, slug `dune` | `single-book-dune.php` -> `single-book.php` -> `single.php` -> `singular.php` -> `index.php` |
| Page `about` (id 12) | custom template chosen in editor -> `page-about.php` -> `page-12.php` -> `page.php` -> `singular.php` -> `index.php` |
| Category `news` | `category-news.php` -> `category-5.php` -> `category.php` -> `archive.php` -> `index.php` |
| Custom taxonomy `genre` term `scifi` | `taxonomy-genre-scifi.php` -> `taxonomy-genre.php` -> `taxonomy.php` -> `archive.php` |
| CPT archive `book` | `archive-book.php` -> `archive.php` |
| Author | `author-{nicename}.php` -> `author-{id}.php` -> `author.php` -> `archive.php` |
| Front page | `front-page.php` -> (home.php if showing posts / page chain if static page) |
| Blog posts index | `home.php` -> `index.php` |
| Search / 404 | `search.php` / `404.php` -> `index.php` |
| Attachment | `{mimetype}-{subtype}.php` -> `{subtype}.php` -> `{mimetype}.php` -> `attachment.php` -> then the single/singular chain |
Block themes use the same names as `.html` files in `templates/` (e.g. `templates/single-book.html`) and parts in `parts/`.

## 3. Custom templates
Classic page template:
```php
<?php
/*
 * Template Name: Landing (no sidebar)
 * Template Post Type: page, post
 */
get_header(); /* ... */ get_footer();
```
Block themes: register in `theme.json` `customTemplates` with a matching `templates/landing.html`.

## 4. Template parts
Classic: `get_template_part( 'parts/card', get_post_type() )` loads `parts/card-book.php` then `parts/card.php`, and accepts an `$args` array (WordPress 5.5.0+). Block: `<!-- wp:template-part {"slug":"header"} /-->`.

## 5. Override programmatically (plugins)
```php
add_filter( 'template_include', function ( $template ) {
    if ( is_singular( 'event' ) ) {
        $theme = locate_template( 'single-event.php' );
        return $theme ?: plugin_dir_path( __FILE__ ) . 'templates/single-event.php';   // let themes override
    }
    return $template;
} );
```
Also the dynamic `{$type}_template` filters (for example `single_template`).

## 6. Hybrid gotcha
Block themes: templates edited in the Site Editor are saved to the database (`wp_template` posts) and take precedence over the theme file, so a file change that does nothing may mean a saved customisation exists; reset it in the Site Editor.

## Verify
- [ ] The expected template file is the one rendering (for example by temporarily adding a visible comment to it).
- [ ] Child theme overrides only the files it needs.
- [ ] Plugin templates can be overridden by the active theme.

## Checked

2026-10-25: against wordpress-develop trunk source (`template.php`, `template-loader.php`, `general-template.php`, `class-wp-theme.php`; last commit 2026-10-25) and the Gutenberg theme.json reference. Confirmed: candidate file lists for single, page, category, tag, taxonomy, archive, author, attachment, home and front page, `get_template_part` `$args` since 5.5.0, the `Template Post Type` header, `{$type}_template` hooks, `customTemplates` in theme.json. Corrected the attachment chain (adds `{subtype}.php`). Removed unconfirmed claims about the Query Monitor Template panel and the Template panel UI.

Method: documentation only; no commands were run.
