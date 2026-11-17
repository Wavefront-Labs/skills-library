---
id: computing-software.systems-network-administration.linux.package-repositories-keys-and-mirrors
name: package-repositories-keys-and-mirrors
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, repository, repositories, package-repository, local-mirror, package-mirror, gpg-key, signed-by, apt-sources, deb822, sources-list, yum-repos-d, dnf-config-manager, epel, createrepo, reposync, debmirror, apt-mirror, aptly, apt-cacher-ng, nexus, air-gapped, offline-install, lpic-1, sysadmin, ppa, dnf-makecache]
level: practitioner
status: gated
description: "Add apt/dnf repositories with scoped GPG keys (signed-by, gpgkey), fix key/metadata errors, and build local mirrors or caches (reposync, aptly, apt-cacher-ng) for fleets."
sources:
  - https://manpages.debian.org/bookworm/apt/sources.list.5.en.html
  - https://wiki.debian.org/DebianRepository/UseThirdParty
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_software_with_the_dnf_tool/assembly_managing-custom-software-repositories_managing-software-with-the-dnf-tool
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Package repositories, GPG keys and local mirrors

**Goal:** add a repository so that only *that* repository is trusted with *its* key,
diagnose signature/metadata failures, and serve packages from your own mirror when
hosts are many or offline.

## 1. apt (Debian/Ubuntu): deb822 + `Signed-By`
`apt-key` is deprecated; a key in
`/etc/apt/trusted.gpg.d/` is trusted for **every** repository, which is how one (gated: unconfirmed, source is paywalled or blocked)
compromised vendor key signs your base system. Scope keys per repo:
```bash
curl -fsSL https://vendor.example/key.asc \
  | sudo gpg --dearmor -o /etc/apt/keyrings/vendor.gpg     # binary keyring
# or keep the ASCII-armored key as /etc/apt/keyrings/vendor.asc (Debian wiki: ASCII-armored keys use the .asc extension)
sudo tee /etc/apt/sources.list.d/vendor.sources <<'EOF'
Types: deb
URIs: https://vendor.example/apt
Suites: bookworm
Components: main
Architectures: amd64
Signed-By: /etc/apt/keyrings/vendor.gpg
EOF
sudo apt update
```
One-line form still works: `deb [arch=amd64 signed-by=/etc/apt/keyrings/vendor.gpg] https://vendor.example/apt bookworm main`
in a `.list` file. `/etc/apt/keyrings` is the conventional dir (create it `0755`);
`/usr/share/keyrings` is for keys shipped by packages.

Check the key before trusting it: `gpg --show-keys /etc/apt/keyrings/vendor.gpg`
and compare the fingerprint with the vendor's published one. Keys expire: a
`EXPKEYSIG` error means fetch the vendor's refreshed key, not disable checks.

Common errors:
- `NO_PUBKEY ABC123…` — key missing or not in the `Signed-By` path; fix the path,
  never `apt-get --allow-unauthenticated`.
- `does not have a Release file` — wrong suite/codename (`lsb_release -cs`) or the
  vendor does not ship your release; do not point `noble` at `jammy` blindly.
- `Conflicting values set for option Signed-By` — the same repo listed twice with
  different keys (an old `.list` plus a new `.sources`). Remove one.
- Prevent a third-party repo from replacing base packages with a pin
  (`/etc/apt/preferences.d/vendor`, `Pin-Priority: 100` for everything from it except the
  package you want) — see `apt-dependency-resolution` in this product.

PPAs (`add-apt-repository ppa:user/name`) write the same files; inspect them after.

## 2. dnf/yum (RHEL/Fedora): `.repo` files and `gpgkey`
```ini
# /etc/yum.repos.d/vendor.repo
[vendor]
name=Vendor packages for EL$releasever
baseurl=https://vendor.example/el/$releasever/$basearch/
enabled=1
gpgcheck=1
repo_gpgcheck=1          # also verify the repo metadata signature if the vendor signs it
gpgkey=https://vendor.example/RPM-GPG-KEY-vendor
module_hotfixes=1        # only if the repo must override a modular stream (rare)
priority=90              # lower value wins; the default is 99
```
Helpers: `dnf config-manager --add-repo URL` (writes a `.repo` from a URL, no key),
`dnf config-manager --set-disabled vendor`, `dnf repolist --all`, `dnf repoinfo vendor`,
`dnf --disablerepo='*' --enablerepo=vendor list available`.
EPEL on RHEL 9: `dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm`
plus enable CRB: `subscription-manager repos --enable codeready-builder-for-rhel-9-$(arch)-rpms`
(`dnf config-manager --set-enabled crb` on Rocky/Alma).

Keys are imported on first use (dnf prompts; `-y` accepts) and stored in the rpm db:
`rpm -q gpg-pubkey --qf '%{NAME}-%{VERSION}-%{RELEASE}\t%{SUMMARY}\n'`,
remove with `rpm -e gpg-pubkey-<ver>-<rel>`. Pre-import for unattended hosts:
`rpm --import /path/key`. Error `GPG check FAILED` with a changed key: compare
fingerprints (`gpg --show-keys key`), then remove the old pubkey and re-import.
Stale metadata (`404 repodata/...`): `dnf clean metadata && dnf makecache`;
`metadata_expire=1h` in the `.repo` controls caching.

Variables: `$releasever` (override with `--releasever=9`), `$basearch`, custom
`/etc/dnf/vars/<name>` files — handy for `baseurl=https://mirror/$site/el/...`.

## 3. Local mirror vs cache — pick the smaller tool
| Need | Tool |
|---|---|
| Save bandwidth, hosts online | **apt-cacher-ng** (proxy, works for apt and yum; `Acquire::http::Proxy "http://cache:3142";`) or Squid |
| Full offline copy, RHEL-family | `reposync` + `createrepo_c` |
| Full offline copy, Debian | `apt-mirror` or `debmirror`; `aptly` when you need snapshots/promotion |
| Many repo types, promotion workflow | Nexus / Artifactory / Pulp (heavier) |

### RHEL-family mirror
```bash
dnf install dnf-plugins-core createrepo_c
reposync --repoid=baseos --repoid=appstream --download-metadata --newest-only \
         --delete -p /srv/mirror/el9         # --newest-only keeps one version per package
# packages land in /srv/mirror/el9/<repoid>/; --download-metadata copies repodata (incl. modules & groups)
createrepo_c --update /srv/mirror/el9/custom   # only for your OWN dir of rpms; reposync'd repos already carry repodata
```
Serve `/srv/mirror` with nginx/httpd (`autoindex on`), then on clients:
```ini
[baseos-local]
name=BaseOS local
baseurl=http://mirror.internal/el9/baseos/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rockyofficial
```
Modular repos (AppStream): without `--download-metadata` you lose `modules.yaml` and
`dnf module` streams break. Re-run `reposync` on a timer; `--delete` removes packages
no longer upstream, which is what you want for a mirror and not what you want for an
archive.

### Debian/Ubuntu mirror with aptly (snapshot-able)
```bash
aptly mirror create -architectures=amd64 -filter-with-deps bookworm http://deb.debian.org/debian bookworm main
aptly mirror update bookworm
aptly snapshot create bookworm-$(date +%F) from mirror bookworm
aptly publish snapshot -distribution=bookworm bookworm-$(date +%F)   # signs with your GPG key
aptly serve                                                           # or serve ~/.aptly/public via nginx
```
Clients get `Signed-By` = your signing key. Promoting a tested snapshot to prod is
`aptly publish switch bookworm <snapshot>`; that is the whole reason to choose aptly
over a dumb `apt-mirror` copy. `apt-mirror` (config `/etc/apt/mirror.list`) is fine
when "latest only" is acceptable; mirrors keep upstream signatures so no re-signing.

### Air-gapped transfer
Sync on an internet host, `rsync -a --delete` the tree to removable media, serve on the
inside. Keys travel as files (`gpgkey=file:///...`, `Signed-By: /etc/apt/keyrings/...`).
Test on one client with `dnf --disablerepo='*' --enablerepo='*-local' update --assumeno`
or `apt-get -s dist-upgrade`.

## 4. Hygiene
- One file per repository, named after the vendor; comments with the date and why.
- Disable, don't delete, repos you may need for `dnf history undo`/downgrades.
- `apt-get update` warnings about `i386` for a 64-bit-only repo: add `Architectures:`
  (deb822) or `[arch=amd64]`.
- Audit what is trusted: `apt-key list` (deprecated but shows leftovers in
  `trusted.gpg`), `ls /etc/apt/trusted.gpg.d /etc/apt/keyrings`,
  `rpm -qa gpg-pubkey*`. Move anything in `trusted.gpg.d` that is not the distro's own
  to `keyrings` with `Signed-By`.

## Verify
- [ ] `apt-get update` / `dnf makecache` completes with no `NO_PUBKEY`, `EXPKEYSIG` or
      `GPG check FAILED` lines.
- [ ] `apt-cache policy <pkg>` / `dnf repoquery --location <pkg>` shows the package
      comes from the intended repo (or the local mirror URL).
- [ ] Removing the vendor key file makes `apt update` fail for that repo only, not for
      the base repos (proves `Signed-By` scoping).
- [ ] On a mirror client with the upstream repo disabled, `dnf update`/`apt
      dist-upgrade` resolves fully from the mirror.

## Checked

2026-11-02

- Confirmed: sources.list(5) from manpages.debian.org, the Debian UseThirdParty wiki page and the DNF configuration reference were fetched.
- Removed or gated: dnf reposync/createrepo_c flags, apt-mirror style filters and key-handling commands are not all stated on the fetched pages; gated, confirm in the current man pages.

Method: documentation only; no commands were run.
