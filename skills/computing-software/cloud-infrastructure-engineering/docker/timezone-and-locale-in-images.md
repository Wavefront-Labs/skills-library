---
id: computing-software.cloud-infrastructure-engineering.docker.timezone-and-locale-in-images
name: timezone-and-locale-in-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, tz-env, locale-env, tzdata, lang, utf-8, environment-variables]
level: practitioner
status: docs-checked
description: "Set timezone and locale in container images: tzdata and TZ, mounting /etc/localtime, C.UTF-8 vs generated locales, Alpine and distroless differences, and Go embedded tzdata."
sources: ["https://docs.docker.com/reference/dockerfile/#env", "https://pkg.go.dev/time/tzdata", "https://hub.docker.com/_/postgres"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timezone and locale in images

Keep UTC for servers and logs and convert at the edge; set a timezone only when software
genuinely needs local time (schedulers, reports).

## Timezone
```dockerfile
# install your distro's tzdata package, then set TZ
ENV TZ=Europe/London
```
- Runtime alternative: `docker run -e TZ=America/New_York`.
- Zone names need a zone database in the image. For Go programs you can embed one: import
  `_ "time/tzdata"` in the main package or build with `-tags timetzdata`; the Go docs say it
  is used when the time package cannot find tzdata files on the system, and adds about 450 KB.
- Check what your own base image ships before assuming it has zone data.

## Locale
```dockerfile
# Debian-based postgres image, from the postgres README: build the locale, then set LANG
RUN localedef -i de_DE -c -f UTF-8 -A /usr/share/locale/locale.alias de_DE.UTF-8
ENV LANG de_DE.utf8
```
- The postgres README says init scripts run in sorted order by the current locale, which
  defaults to `en_US.utf8` in that image, and that Alpine-based variants support ICU
  locales starting with Postgres 15.
- Set the locale in the image before the database's first start, since `initdb` runs then.

## Verify
```bash
docker run --rm <image> date                      # timezone abbreviation
docker run --rm -e TZ=Asia/Tokyo <image> date
```

## Checked
Date: 2026-10-26. Documentation: Go `time/tzdata` package source (golang/go), docker-library postgres README (locale section). Confirmed: embedded tzdata import and `timetzdata` build tag, fallback behaviour and size note, the postgres locale recipe and default, ICU on Alpine from Postgres 15. Removed as unconfirmed: package-install commands per distro, "glibc silently uses UTC", host `/etc/localtime` mount, distroless tzdata claim, JVM/Node/Python timezone claims, generic C.UTF-8 and locale-gen recipes, symptom list, Alpine musl locale claim (Alpine and Debian wiki pages are not in a public GitHub repo).
Method: documentation only; no commands were run.
