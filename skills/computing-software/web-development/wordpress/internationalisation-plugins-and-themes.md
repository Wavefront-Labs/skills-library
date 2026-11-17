---
id: computing-software.web-development.wordpress.internationalisation-plugins-and-themes
name: internationalisation-plugins-and-themes
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, wordpress-i18n, text-domain, gettext, translate-wordpress, wp-i18n-make-pot, php, web-development]
level: practitioner
status: docs-checked
description: "Making WordPress plugins and themes translatable: text domains, __()/_e()/_n()/_x() with escaping, placeholders, JS translations with wp_set_script_translations, POT generation."
sources:
  - https://developer.wordpress.org/plugins/internationalization/how-to-internationalize-your-plugin/
  - https://developer.wordpress.org/apis/internationalization/internationalization-functions/
  - https://developer.wordpress.org/cli/commands/i18n/make-pot/
  - https://developer.wordpress.org/reference/functions/wp_set_script_translations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Internationalisation of plugins and themes

**Goal:** every user-facing string translatable via translate.wordpress.org or bundled files, in PHP and JavaScript.

## 1. Text domain
The text domain must match the plugin slug (for wordpress.org-hosted plugins, the slug in the plugin URL). Header: `Text Domain: acme-events` and `Domain Path: /languages` (leading slash) if bundling files. Since WP 4.6 the `Text Domain` header is optional because it must equal the slug, and plugins translated on translate.wordpress.org no longer need `load_plugin_textdomain()` if `Requires at least` in readme.txt is 4.6 or higher.

## 2. Functions
```php
echo esc_html__( 'Upcoming events', 'acme-events' );
esc_html_e( 'No events found.', 'acme-events' );
printf( esc_html( _n( '%s event', '%s events', $count, 'acme-events' ) ), number_format_i18n( $count ) );
echo esc_html_x( 'Post', 'verb: publish', 'acme-events' );       // context disambiguates
/* translators: 1: event title, 2: date */
printf( esc_html__( '%1$s starts on %2$s', 'acme-events' ), esc_html( $title ), esc_html( date_i18n( get_option( 'date_format' ), $ts ) ) );
```
Rules: literal strings and literal text domain (tools parse source, so no variables); whole sentences, no concatenation; numbered placeholders when there are several; a `translators:` comment directly above for any placeholder; escape the output with the escaping variants (`esc_html__`, `esc_html_e`).

## 3. JavaScript
```php
wp_register_script( 'acme-editor', plugins_url( 'build/editor.js', __FILE__ ), [ 'wp-i18n' ], $ver );
wp_set_script_translations( 'acme-editor', 'acme-events', plugin_dir_path( __FILE__ ) . 'languages' );
```
```js
import { __, _n, sprintf } from "@wordpress/i18n";
sprintf( _n( "%d event", "%d events", n, "acme-events" ), n );
```

## 4. Generate files
```bash
wp i18n make-pot . languages/acme-events.pot --exclude=node_modules,vendor
wp i18n make-json languages                       # JS translations from .po
```

## Checked
2026-10-31. Confirmed on the developer.wordpress.org plugin i18n handbook, `wp i18n make-pot`, `make-json` and `wp_set_script_translations` pages: text domain must match the slug and be a literal, WP 4.6 behaviour, Domain Path, translators comments, placeholders and no concatenation. Removed: WP 6.7 notice, make-php and --no-purge, block.json textdomain, the locale-formatting section and the PHPCS item (not on those pages).
Method: documentation only; no commands were run.

## Verify
- [ ] `wp i18n make-pot` produces no warnings (missing translators comments, variables as domains).
- [ ] Switching the site to a test locale with a sample .mo shows translated PHP and JS strings.
