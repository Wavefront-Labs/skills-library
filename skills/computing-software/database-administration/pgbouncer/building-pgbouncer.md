---
id: computing-software.database-administration.pgbouncer.building-pgbouncer
name: building-pgbouncer
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, install, autoconf, meson, build]
level: practitioner
status: docs-checked
description: "Build dependencies and commands for PgBouncer with Autoconf or the experimental Meson build."
sources:
  - https://www.pgbouncer.org/install.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: compile and install PgBouncer from source.

Dependencies: Libevent 2.0+, pkg-config, OpenSSL 1.0.1+ for TLS, a C11-capable compiler. Optional: c-ares (alternative to evdns), LDAP libraries, PAM libraries. The Meson build also needs Meson 0.58+ and Ninja; Autoconf needs GNU Make 3.81+. Autoconf is the recommended build for production and packaging; Meson is experimental and expected to become the default.

Autoconf:

```
./configure --prefix=/usr/local
make
make install
```

Meson:

```
meson setup build --prefix=/usr/local
meson compile -C build
meson install -C build
```

Building from Git (Autoconf) needs generated files first, plus autoconf, automake, libtool and pandoc:

```
git clone https://github.com/pgbouncer/pgbouncer.git
cd pgbouncer
./autogen.sh
./configure
make
make install
```

Everything installs under /usr/local by default. Run `./configure --help` for options. With Meson you can build straight from a checkout (pandoc is needed for man pages) and `meson configure build` lists the -D options.

Optional features: Meson auto-detects PAM, LDAP and systemd (`-Dpam`, `-Dldap`, `-Dsystemd` default auto; set enabled or disabled). Autoconf requires explicit `--with-pam`, `--with-ldap`, `--with-systemd`.

systemd support enables Type=notify (Type=notify-reload on systemd 253+) and socket activation; the source tree has etc/pgbouncer.service and etc/pgbouncer.socket examples.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
