---
id: computing-software.networking-hardware-and-wireless.apache-httpd.rewrite-per-directory-and-htaccess
name: rewrite-per-directory-and-htaccess
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-rewrite, per-directory, htaccess, rewritebase, rewriteoptions]
level: advanced
status: docs-checked
description: "Handle mod_rewrite in Directory and .htaccess context: patterns without leading slash, RewriteBase, FollowSymLinks, END vs L, and rule inheritance."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html
  - https://httpd.apache.org/docs/2.4/rewrite/flags.html
  - https://httpd.apache.org/docs/2.4/rewrite/avoid.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_rewrite per-directory context
## Requirements
`RewriteEngine On` plus `Options FollowSymLinks` or `SymLinksIfOwnerMatch`.

## Behaviour
- The directory prefix is stripped before matching, so patterns never start with `/`. Use `^/` only in server or vhost context.
- Relative substitutions use `RewriteBase`. It is required unless the request and substitution are under DocumentRoot, or the request is mapped via Alias or mod_userdir (2.4.16+).
- `L` has caveats in per-directory context; `END` also prevents further execution of rewrite rules in that context.
- `PT` is implied.
- `T=` needs `-` as the substitution here or the type is lost.

## Inheritance
Rules at the same level are overridden by default. `RewriteOptions Inherit` merges them; also `InheritBefore`, `InheritDown`, `InheritDownBefore`, `IgnoreInherit` (2.4.8+), `MergeBase`.

## Ordering
In server or vhost context mod_rewrite runs before mod_alias; in `.htaccess` mod_alias runs first.

## Other options
`AllowNoSlash` (DirectorySlash off), `AllowAnyURI` (security risk, not recommended), `LegacyPrefixDocRoot` (pre-2.4.26 behaviour).

## Checked
2026-11-04. Confirmed against the mod_rewrite reference, the RewriteRule flags page and the "when not to use mod_rewrite" page: per-directory requirements and prefix stripping, RewriteBase exceptions (2.4.16), PT implied, T= with dash, RewriteOptions values and versions, module ordering. Removed: the "prefer main config ... load once" advice (not on the pages).
Method: documentation only; no commands were run.
