---
id: computing-software.networking-hardware-and-wireless.squid.error-page-directory
name: error-page-directory
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, error-directory, error-pages, custom-errors]
level: intro
status: draft
description: "Replace Squid error pages by copying the default templates and pointing error_directory at them."
sources:
  - https://www.squid-cache.org/Doc/config/error_directory/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# error_directory
Default: send error pages in the client's preferred language. To customise, copy the default error/template files to another directory and set `error_directory` to it.

Warning from the page: using this option disables multi-language support on error pages.
