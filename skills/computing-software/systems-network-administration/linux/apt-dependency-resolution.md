---
id: computing-software.systems-network-administration.linux.apt-dependency-resolution
name: apt-dependency-resolution
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apt, dpkg, debian, ubuntu, apt-get, apt-cache, dependency-resolution, held-packages, broken-packages, apt-pinning, apt-mark, dpkg-scripts, policy, sysadmin, package-management, dpkg-l, apt-policy, apt-autoremove]
level: advanced
status: docs-checked
description: "Debug apt/dpkg dependency conflicts, held packages, and broken installs by understanding dpkg's dependency fields and apt's solver."
sources:
  - https://www.debian.org/doc/debian-policy/ch-relationships.html
  - https://manpages.debian.org/testing/apt/apt-get.8.en.html
  - https://manpages.debian.org/testing/apt/apt_preferences.5.en.html
  - https://manpages.debian.org/testing/apt/apt-mark.8.en.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# apt/dpkg dependency resolution — reading the solver's reasoning

**Goal:** when `apt install` refuses, or `apt upgrade` wants to remove half
the system, read *why* from the dependency fields involved instead of
reaching for `--force` — and know the handful of commands that fix a broken
install without guessing.

## 1. The two layers
`dpkg` is the low-level tool: installs/removes individual `.deb` files,
tracks installed state, runs maintainer scripts (`preinst`/`postinst`/etc),
but **has no network access and no automatic dependency resolution** — ask
it to install a package whose dependency isn't present and it just fails.
`apt`/`apt-get` is the layer on top: fetches `.deb`s from repositories and
*solves* the dependency graph, then hands the actual install off to `dpkg`.
Almost every "it won't install" problem is apt's solver saying no, not
dpkg's mechanics — the fix lives at the apt layer.

```bash
dpkg -l | grep ^ii          # installed packages (ii = install ok installed)
dpkg -l | grep -v ^ii        # anything NOT cleanly installed — rc, iU, iF etc are trouble
apt-cache policy <pkg>       # candidate version, installed version, and which repo/priority wins
apt-cache depends <pkg>      # full dependency tree as declared
apt-cache rdepends <pkg>     # reverse: what depends on this package (check before removing anything)
```

## 2. Dependency field semantics (what the solver is actually satisfying)
- `Depends`: a package is not configured unless everything in its `Depends` is
  configured (a `Provides:` virtual package can satisfy it).
- `Recommends`: a strong, but not absolute, dependency; apt installs them unless
  `--no-install-recommends` (config item `APT::Install-Recommends`) is given.
- `Suggests`: the package may be more useful with these; apt does not install them unless `--install-suggests` is given.
- `Conflicts`: dpkg refuses to unpack the two packages at the same time; a stronger
  restriction than `Breaks`.
- `Breaks`: dpkg refuses to unpack the breaking package until the broken package is
  deconfigured; Debian Policy says to prefer it over `Conflicts` in most cases.
- `Provides`: a virtual package name multiple real packages can satisfy
  (e.g. several mail transport agents all `Provide: mail-transport-agent`).

`apt-cache show <pkg>` prints all of these for the candidate version — read
it before assuming a conflict is a bug rather than working as declared.

## 3. Reading a refusal
```
The following packages have unmet dependencies:
 foo : Depends: libbar (>= 2.0) but 1.5 is installed
E: Unable to correct problems, you have held broken packages.
```
This says exactly what's missing — a version constraint, not just presence.
```bash
apt-cache policy libbar          # see what version is actually available vs installed
apt list --upgradable             # is a newer libbar waiting on a held package or pinning rule?
apt-mark showhold                 # list of packages explicitly held back
apt-mark unhold libbar            # remove a hold if that's what's blocking the resolution
```

## 4. Fixing a broken state
```bash
sudo dpkg --configure -a          # finish any half-configured package (interrupted install)
sudo apt --fix-broken install     # let apt figure out and install/remove to satisfy deps
sudo apt-get install -f           # older spelling of the same thing
sudo apt-get install --fix-missing <pkg>   # ignore packages that cannot be fetched and continue
```
`dpkg --configure -a` first, always — a package stuck mid-`postinst` from an
interrupted install blocks apt from doing anything else until it's finished
or explicitly fixed.

## 5. Pinning — making apt prefer a specific version/repo
```
# /etc/apt/preferences.d/pin-nginx
Package: nginx*
Pin: release a=stable
Pin-Priority: 900
```
A priority above 1000 allows downgrades; apt's defaults are 500 for
ordinary sources, 990 for the target release and 100 for installed versions;
a negative priority prevents the version from being installed. Useful for
pinning a package to a specific suite when multiple repos (backports,
third-party PPAs) all offer different versions of the same name and apt's
default (newest wins) isn't what you want.

## 6. Other solvers
For the dnf side see the companion skill
`computing-software.systems-network-administration.linux.dnf-yum-dependency-resolution`.
Read apt's proposed removal list before accepting it; installing a specific
version (`apt install <pkg>=<version>`) can avoid a removal apt proposed.

## Gotchas
- `apt remove` keeps config files (`~c` state in `dpkg -l`); `apt purge`
  removes them too — a reinstall after `remove` can silently reuse stale
  config that `purge` would have cleared.
- A lock error means another apt or dpkg process is running; find it with `ps aux | grep -i apt`
  and wait rather than deleting lock files by hand.
- Removing a package with many reverse dependencies (`apt-cache rdepends`)
  via `apt remove` cascades — always read apt's proposed removal list in
  full before confirming, especially on a server where `apt autoremove`
  after a big uninstall can take more with it than expected.

## Verify
- [ ] `dpkg -l | grep -v ^ii` is empty (or only expected `rc` entries) — no package stuck half-configured.
- [ ] `apt-cache policy <pkg>` shows the installed version matching the intended pin/priority, not an unexpected candidate.
- [ ] `apt-mark showhold` matches the intentional hold list, not leftover holds from a past incident.
- [ ] After `apt --fix-broken install`, `apt update && apt upgrade --dry-run` shows no further unmet dependencies.

## Checked

Checked against Debian Policy ch-relationships (current Debian policy site, 2026-10-25), the apt source docs (Debian/apt doc/, last commit 2025-11-10) and dpkg(1).
Confirmed: field semantics for Depends, Recommends, Suggests, Breaks, Conflicts and Provides; `--no-install-recommends`, `--install-suggests`, `-f/--fix-broken`, `--fix-missing` (an apt-get option) and apt-mark `hold/unhold/showhold`; pin priorities (990 target release, 500, 100 installed, above 1000 allows downgrade, negative prevents install); remove keeps and purge deletes configuration files; `dpkg --configure -a`.
Fixed: `apt update --fix-missing` is not a valid use, replaced by `apt-get install --fix-missing`. Removed as unconfirmed: lock-frontend and PPA 404 remarks and the apt-versus-dnf solver comparison.

Method: documentation only; no commands were run.
