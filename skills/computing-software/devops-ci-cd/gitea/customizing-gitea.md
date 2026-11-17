---
id: computing-software.devops-ci-cd.gitea.customizing-gitea
name: customizing-gitea
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-custom-dir, gitea, custom-templates, extra-links-tmpl, gitea-custom-theme, options-label-yaml, receive-cert-nonce-seed, ctx-csp-script-nonce]
level: practitioner
status: docs-checked
description: "Customize Gitea via the custom dir: public assets, template overrides and hooks (extra_links, footer), DumpVar, themes, labels, locales, readmes, signed pushes."
sources: ["https://docs.gitea.com/administration/customizing-gitea/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customizing Gitea

Everything lives in `CustomPath` (default `custom/` under the work path; see it with `gitea help`, on the Site Administration Configuration tab, or override with `GITEA_CUSTOM` or `--custom-path`, the flag wins). Config is `CustomConf`, default `$GITEA_CUSTOM/conf/app.ini`. **A full restart is needed** to see config/template changes.

## Public files
`$GITEA_CUSTOM/public/` is a webroot but only serves `robots.txt`, `.well-known/` and `assets/`; `assets/image.png` is served at `/assets/image.png`. Symlinks are followed.

## Overriding embedded resources
Place a replacement at the same relative path under the custom dir: `options/gitignore/C++`, `templates/home.tmpl`, etc. Get the original with the `gitea embedded` tool or the source `templates/` of the matching release (templates change between versions). Do not touch `{{ }}` blocks unless you understand them. Pages run under a Content-Security-Policy: inline scripts need `<script nonce="{{ctx.CspScriptNonce}}">`.
Hook templates in `templates/custom/`: `extra_links.tmpl` (navbar), `extra_links_footer.tmpl`, `extra_tabs.tmpl` (repo tabs, markup in `templates/repo/header.tmpl`), `header.tmpl` (end of `<head>`, CSS/analytics), `body_outer_pre.tmpl`, `body_inner_pre.tmpl`, `body_inner_post.tmpl`, `body_outer_post.tmpl`, `footer.tmpl` (JS). Links should use class `item` and `{{AppSubUrl}}`, e.g. `<a class="item" href="{{AppSubUrl}}/assets/impressum.html">Impressum</a>`.
Discover variables: temporarily set `RUN_MODE = dev`, add `{{ $ | DumpVar }}` to a template, restart; then use e.g. `{{.Repository.Name}}`. Switch back to prod afterwards.
Logo/favicon: replace `assets/logo.svg` / `assets/favicon.svg` in a source checkout, `make generate-images`, copy the outputs (`logo.svg`, `logo.png`, `avatar_default.png`, `apple-touch-icon.png`, `favicon.svg`, `favicon.png`) to `public/assets/img/`.
Mail bodies: copy from `templates/mail` keeping the path (see `gitea-mail-template`).

## options/ files (no file extension)
gitignore (rules file in `options/gitignore`), license text in `options/license`, readme in `options/readme` (variables `{Name}`, `{Description}`, `{CloneURL.SSH}`, `{CloneURL.HTTPS}`, `{OwnerName}`), locale overrides in `options/locale`. New locale also needs `[i18n]` `LANGS = en-US,foo-BAR` and `NAMES = English,FooBar`; these are overrides, so copy the default list too; the first entry is the fallback language. Labels (1.19+) YAML in `options/label`:
```yaml
labels:
  - name: "foo/bar"
    exclusive: true     # scoped labels use / as delimiter
    color: aabbcc
    description: Some label
```
Reactions: `[ui] REACTIONS = +1, -1, laugh, confused, heart, hooray, eyes`.

## Themes and fonts
Built in: `gitea-light`, `gitea-dark`, `gitea-auto`. `[ui] DEFAULT_THEME` sets the default, `THEMES` the allowed list (empty means all). A custom theme is `public/assets/css/theme-<name>.css`; display name via `gitea-theme-meta-info { --theme-display-name: "..." }`, and a dark theme must set `--is-dark-theme: true` in `:root` (the Monaco editor follows it). Fonts: override `--fonts-proportional`, `--fonts-monospace`, `--fonts-emoji` with `!important`.

## git config (1.20+)
Signed pushes: `[git.config] receive.certNonceSeed = <secret random string>` (anti-replay nonce). Gitea already sets `receive.advertisePushOptions = true` and does not read `/etc/gitconfig`. Clients use `git push --signed` or `git config --global push.gpgSign if-asked`.

## Checked

2026-11-03: read https://docs.gitea.com/administration/customizing-gitea/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
