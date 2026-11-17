---
id: computing-software.systems-network-administration.linux.compile-custom-locales-with-localedef
name: compile-custom-locales-with-localedef
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, localedef, custom-locale, locale-archive, lc-time, glibc-locales, iso-8601]
level: practitioner
status: docs-checked
description: "Build custom glibc locales with localedef: copy and modify a locale source (ISO 8601 dates, Monday weeks, number formats), compile it, install it in the archive and use it."
sources:
  - https://man7.org/linux/man-pages/man1/localedef.1.html
  - https://man7.org/linux/man-pages/man5/locale.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compile custom locales with localedef

Use when no shipped locale matches what you need, e.g. English text with ISO 8601 dates and 24 h time, or a company-wide number format. (Check first whether a shipped locale already fits.)

## Compile an existing source
```bash
localedef -i en_GB -f UTF-8 en_GB.UTF-8
localedef --list-archive | grep en_GB
```
The input file is searched in the current directory and under `$I18NPATH/locales/`; charmaps under `$I18NPATH/charmaps/` (localedef(1)). Distributions ship the sources in their own i18n directory.

## Make a custom one
```bash
cp <path-to-shipped-locale-source>/en_GB ./en_GB@iso
```
Edit the categories you need. Inside a category, `copy "en_GB"` must be the only statement except in LC_COLLATE and LC_CTYPE (locale(5)), so keep `copy` for untouched categories and paste the full `LC_TIME` block from the source file, then change keys:
```
LC_TIME
abday   "Sun";"Mon";"Tue";"Wed";"Thu";"Fri";"Sat"
...
d_t_fmt "%Y-%m-%dT%H:%M:%S %Z"
d_fmt   "%Y-%m-%d"
t_fmt   "%T"
am_pm   "";""
t_fmt_ampm ""
week    7;19971130;4
first_weekday 2
END LC_TIME
```
Then compile with an explicit path:
```bash
localedef -i ./en_GB@iso -f UTF-8 en_GB.UTF-8@iso
locale -a | grep iso
LC_TIME=en_GB.UTF-8@iso date +%x        # 2026-10-18
```
- `-c` forces output despite warnings; fix warnings rather than ship them.

## Deploy
- Compiled locales go into `/usr/lib/locale/locale-archive` (default) or, with `--no-archive`, a directory beside it, which prevents system archive updates from overwriting them (localedef(1)). Rerun `localedef` from config management after glibc updates.
- Use per category: `LANG=en_GB.UTF-8 LC_TIME=en_GB.UTF-8@iso`.
- Remove: `localedef --delete-from-archive en_GB.utf8@iso`.

## Verify
- [ ] `locale -k LC_TIME | grep d_fmt` shows the new format under the custom locale.
- [ ] The locale is still listed after a glibc package update.

## Checked
2026-10-27. Checked against man-pages locale(5) and localedef(1) (man-pages 5.12 mirror, 2021-03-22). Confirmed: the copy rule and its LC_COLLATE and LC_CTYPE exceptions; the week keyword (days, base date 19971130 for Sunday and 19971201 for Monday, minimal first-week days, default 4) and the compatibility advice to keep 19971130 and set first_weekday to 1 or 2; localedef -i, -f, -c, --list-archive, --delete-from-archive, --no-archive, I18NPATH search paths and /usr/lib/locale/locale-archive. Removed: the en_DK ISO date remark, the locale-gen internals remark, hard-coded source paths, the RHEL package name, the error-message remark and the Debian regeneration claim.

Method: documentation only; no commands were run.
