---
id: computing-software.systems-network-administration.linux.debconf-and-dpkg-reconfigure
name: debconf-and-dpkg-reconfigure
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apt, dpkg, debconf, dpkg-reconfigure, debconf-set-selections, preseed, noninteractive, debian, ubuntu, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Answer Debian package configuration questions: re-run them with dpkg-reconfigure, preseed answers with debconf-set-selections, and inspect the debconf database."
sources:
  - https://manpages.debian.org/bookworm/debconf/dpkg-reconfigure.8.en.html
  - https://manpages.debian.org/bookworm/debconf/debconf-set-selections.1.en.html
  - https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# debconf and dpkg-reconfigure

**Goal:** change answers you gave at install time (timezone, locales, postfix mode, keyboard),
and install packages that ask questions without a human present.

## 1. Re-run a package's questions
```bash
dpkg-reconfigure tzdata
dpkg-reconfigure locales
dpkg-reconfigure postfix                 # re-ask the package's questions
dpkg-reconfigure -plow unattended-upgrades   # -p priority: low shows every question
```
`-f`/`--frontend` selects the frontend. If debconf is normally set to the noninteractive frontend, `dpkg-reconfigure` uses the dialog frontend instead so you can answer.

## 2. Inspect what's stored
```bash
apt install debconf-utils
debconf-get-selections | grep -E '^postfix'      # owner, question, type, value
```
`debconf-get-selections` is in the `debconf-utils` package.

## 3. Preseed for unattended installs
```bash
cat <<'EOF' | debconf-set-selections
postfix postfix/main_mailer_type select Satellite system
postfix postfix/mailname string host1.example.com
postfix postfix/relayhost string [smtp.example.com]:587
tzdata tzdata/Areas select Europe
tzdata tzdata/Zones/Europe select London
EOF
DEBIAN_FRONTEND=noninteractive apt-get install -y postfix
```
Each input line is: owning package, question name, question type, answer (to end of line). Check the format first: `debconf-set-selections -c file` (checks only, saves nothing). Find question names by installing once interactively on a test box and running `debconf-get-selections`.

## 4. Config file prompts (conffiles)
Not debconf, but they block automation the same way:
```bash
apt-get -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" -y upgrade
```
`confold` keeps your modified file (new one saved as `.dpkg-dist`), `confnew` takes the
maintainer's. `confdef` uses the default when there is one.

## Gotchas
- Seed values only for packages that are or will be installed, and avoid leaving stale shared values (debconf-set-selections(1), WARNING section).
- Preseeding after the package is installed does not change its configuration until you reconfigure.

## Verify
- [ ] `debconf-get-selections | grep <pkg>` shows the values you preseeded.
- [ ] The resulting config file (e.g. `postconf relayhost`) reflects them.
- [ ] A CI/automated install completes with no prompt hang.

## Checked

Checked against dpkg-reconfigure(8) and debconf-set-selections(1) on manpages.debian.org (bookworm), and dpkg(1) for `--force-conf*` (guillemj/dpkg).
Confirmed: `-f` frontend selection and the noninteractive-to-dialog behaviour, `-p` priority, set-selections input format and `-c/--checkonly`, debconf-get-selections ships in debconf-utils, `--force-confdef/confold/confnew` meaning.
Removed as unconfirmed: debconf-show, database file paths, tzdata/locales override remark, password cleartext remark, Docker ARG advice, openssh-server reconfigure and `-f noninteractive` reconfigure examples.

Method: documentation only; no commands were run.
