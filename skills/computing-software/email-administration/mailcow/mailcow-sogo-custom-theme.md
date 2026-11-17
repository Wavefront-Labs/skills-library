---
id: computing-software.email-administration.mailcow.mailcow-sogo-custom-theme
name: mailcow-sogo-custom-theme
category: computing-software
field: email-administration
product: mailcow
tags: [sogo, custom-theme, sogo-conf, groupware-webmail, memcached, theme-reset]
level: advanced
status: docs-checked
description: "Apply a custom SOGo theme in mailcow by editing custom-theme.js, extracting the generated CSS and mounting it through a compose override."
sources: ["https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customising the SOGo theme

SOGo provides webmail, contacts and calendars. On builds after 28 January 2021 the theme is changed through `data/conf/sogo/custom-theme.js`, which ships with a commented example based on AngularJS Material theming.

Procedure after editing the JavaScript: set `SOGoUIxDebugEnabled = YES;` in `data/conf/sogo/sogo.conf`, restart `sogo-mailcow` and `memcached-mailcow`, open SOGo in a browser and in the developer console (Firefox first needs `allow pasting`) run a snippet that copies the text of the stylesheets with the `md-theme-style` attribute. Save that minified CSS as `data/conf/sogo/custom-theme.css`, set `SOGoUIxDebugEnabled = NO;` and mount the file via `docker-compose.override.yml` into `sogo-mailcow` at the SOGo `theme-default.css` path (with the `:z` option). Then bring the stack up again.

The docs link the AngularJS Material theming documentation for palette options, and use `custom-theme.js` as a starting point once its comments are removed.

Reset: `git fetch ; git checkout origin/master data/conf/sogo/custom-theme.js`, and remove the CSS override.

## Checked

2026-11-09. The cited SOGo page only links to the design page, so the source was replaced with the Customize design page, where the SOGo theme steps live. Confirmed there: the 28 January 2021 build note, custom-theme.js, SOGoUIxDebugEnabled, restart commands, Firefox allow pasting, the md-theme-style console snippet, custom-theme.css, the compose override mount with :z, and the reset steps. No other changes.

Method: docs-checked 2026-11-09 against the SOGo theme and reset sections of the Customize design page (u_e-mailcow_ui-design.en.md); the old SOGo page was read and does not cover theming.
