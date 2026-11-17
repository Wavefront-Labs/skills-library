---
id: computing-software.web-development.wordpress.theme-check-and-directory-submission
name: theme-check-and-directory-submission
category: computing-software
field: web-development
product: wordpress
tags: [theme-check, theme-directory, theme-review, wordpress-themes, wordpress]
level: practitioner
status: docs-checked
description: "Preparing a theme for the WordPress.org directory: Theme Check, review requirements, licensing, escaping and prefixing, readme, screenshot and submission."
sources:
  - https://make.wordpress.org/themes/handbook/review/required/
  - https://wordpress.org/plugins/theme-check/
  - https://developer.wordpress.org/themes/releasing-your-theme/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Theme Check and directory submission

## 1. Automated checks
- Install the **Theme Check** plugin and fix every Required item (it reports Required, Warning, Recommended and Info). It runs the same automated tests WordPress.org uses, but it is not perfect: every submitted theme is also hand-reviewed.
- Test the theme with content, using the test data from the Theme Checklists, not just the automated check.

## 2. Key review requirements
- **GPL-compatible** licence for all code, images and fonts; declare licence and copyright for bundled resources in `readme.txt`.
- `style.css` header: Theme Name, Author, Description, Version, Requires at least, Tested up to, Requires PHP, License, License URI, Text Domain .
- **No plugin territory**: no CPTs, shortcodes, analytics, SEO meta, or custom blocks that content depends on (recommend plugins instead).
- **Security**: escape all output (`esc_html`, `esc_attr`, `esc_url`, `wp_kses_post`), sanitise inputs, nonces for any forms.
- **Prefix** everything the theme defines in the public namespace (options, functions, global variables, constants, post meta, script/style handles) with a unique prefix of at least four letters; handles of third-party assets are not prefixed.
- Bundle all scripts, images, videos and other resources in the theme zip (Google Fonts is the only exception); no CDN or similar services, and no fetching remote files or data without the user's explicit consent.
- Translation-ready: all strings in `__()`/`esc_html__()` with the theme's text domain.
- No obtrusive upselling, and no upselling on the front end.
- Include a valid `readme.txt`; document any user data collected in it.
- `screenshot.png` must be no bigger than 1200 x 900 px and must not look like an advertisement.

## 3. Block themes extra
Required files are `style.css`, `readme.txt`, `theme.json` and `index.html`; `index.html` goes inside a `templates` folder.

## 4. Accessibility-ready tag
Optional, but if claimed: skip links, keyboard navigation, visible focus, contrast, heading structure, form labels - reviewed by the accessibility team.

## 5. Submission
Check the required theme files, test thoroughly with content, and follow the theme review guidelines before submitting for review. Follow the current submission steps on the Theme Handbook.

## Verify
- [ ] Theme Check shows no Required failures; test content renders correctly; readme lists licences for all assets; no plugin-territory functionality.

## Checked
2026-11-01. Confirmed against the Theme Review required-items page, the Theme Check plugin page and the Releasing Your Theme handbook page: GPL-compatible licence, style.css headers, prefix rule (four letters), no CDN or remote resources (Google Fonts excepted), no upselling, screenshot limit, required files, and the Theme Check report categories. Removed: Plugin Check, phpcs standards, WP_DEBUG_LOG, Unit Test file name, text-domain/folder rule, upload URL and queue details, patterns folder.
Method: documentation only; no commands were run.
