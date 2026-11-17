---
id: computing-software.database-administration.supabase.redirect-urls
name: redirect-urls
category: computing-software
field: database-administration
product: supabase
tags: [redirect-urls, site-url, wildcards, deep-links, preview-deployments]
level: practitioner
status: docs-checked
description: "Configure Supabase Auth Site URL and redirect allow-list: glob wildcard rules, Netlify and Vercel previews, mobile deep links and error fragments."
sources:
  - https://supabase.com/docs/guides/auth/redirect-urls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make Auth redirects work in every environment without opening them wide.

`redirectTo` must match an entry in the Redirect URLs list (URL Configuration page). The Site URL is the default redirect and defaults to `http://localhost:3000`; change it to production, since email confirmation and password reset depend on it. Local and self-hosted projects use `auth.additional_redirect_urls` in the config file.

Wildcards (separator characters are `.` and `/`):
- `*` any sequence of non-separator characters.
- `**` any sequence of characters.
- `?` any single non-separator character.
- `\c` literal c; `[!{ character-range }]` characters not in the range.

Examples: `http://localhost:3000/*` matches `/foo` but not `/foo/bar`; `http://localhost:3000/**` matches both; `http://localhost:3000/?` matches `/a` not `/foo`; `http://localhost:3000/[!a-z]` matches `/1` not `/a`. Use `**` for local development and previews; for production set the exact path.

Previews:
- Netlify: additional URLs `http://localhost:3000/**` and `https://**--my_org.netlify.app/**`.
- Vercel: `http://localhost:3000/**` and `https://*-<team-or-account-slug>.vercel.app/**`, with `NEXT_PUBLIC_SITE_URL` set to production.

Mobile: Site URL such as `com.supabase://login-callback/`, extras like `com.supabase.staging://login-callback/`.

Email templates: when using `redirectTo`, replace `{{ .SiteURL }}` with `{{ .RedirectTo }}`.

Failures still redirect, with details in the URL fragment: parse `window.location.hash`, check whether `error_code` starts with `4`, and show `error_description`.

## Checked

Confirmed against the page: redirectTo vs Redirect URLs list, Site URL default and importance, auth.additional_redirect_urls for local config, wildcard table and examples, separator characters, Netlify and Vercel patterns, NEXT_PUBLIC_SITE_URL, mobile deep link examples, SiteURL vs RedirectTo email templates, error fragment handling. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/auth/redirect-urls (apps/docs/content on GitHub master), read in full.
