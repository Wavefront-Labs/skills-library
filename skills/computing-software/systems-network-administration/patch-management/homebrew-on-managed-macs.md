---
id: computing-software.systems-network-administration.patch-management.homebrew-on-managed-macs
name: homebrew-on-managed-macs
category: computing-software
field: systems-network-administration
product: patch-management
tags: [homebrew, macos, brew-upgrade, third-party-patching, patch-management]
level: practitioner
status: docs-checked
description: "Handle Homebrew on managed Macs: who owns the prefix, running brew upgrade safely from MDM as the user, auditing outdated formulae and casks, and when to block it."
sources:
  - https://docs.brew.sh/Installation
  - https://docs.brew.sh/Manpage
  - https://docs.brew.sh/FAQ
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Homebrew on managed Macs

Developers install tools via Homebrew; those packages (openssl, node, python, casks like browsers) are invisible to most MDM patch tools and go stale.

## Facts that matter
- Prefix: `/opt/homebrew` on Apple silicon (Intel Macs are a Tier 3 configuration). Homebrew is designed for one owning account, which can be a dedicated account, and the prefix owner must not be root. The macOS .pkg installer supports only Apple silicon and takes its install user from the console user or an override file; the Homebrew docs also have a "Homebrew for Mac Admins" page for MDM deployment.
- Homebrew gives no security guarantees where users with write access to the prefix are untrusted.
- `brew update` refreshes formula definitions; `brew upgrade` upgrades installed formulae and casks; `brew outdated --greedy` includes casks that self-update.
- Homebrew auto-updates itself; set `HOMEBREW_NO_AUTO_UPDATE=1` to disable it, or `HOMEBREW_AUTO_UPDATE_SECS` to change the frequency.

## Audit from MDM (script run as root)
```sh
#!/bin/zsh
user=$(stat -f %Su /dev/console)
brew=/opt/homebrew/bin/brew
[ -x $brew ] || { echo "no-brew"; exit 0; }
sudo -u "$user" -H $brew outdated --quiet | /usr/bin/wc -l      # one name per outdated formula or cask
```
Report the count as an extension attribute (Jamf) or custom attribute (Intune) to find stale machines.

## Upgrade
```sh
sudo -u "$user" -H env HOMEBREW_NO_ENV_HINTS=1 $brew update
sudo -u "$user" -H $brew upgrade --formula
sudo -u "$user" -H $brew upgrade --cask        # GUI apps
sudo -u "$user" -H $brew cleanup --prune=30
```
Run at login or off-hours with user notification; developers may have pinned formulae or casks (`brew pin <name>`) for reasons.

## Policy choices
- Allow with weekly upgrade script + reporting (common for developers).
- Provide a managed multi-user setup owned by a service account (more work).
- Block unmanaged package managers on non-developer Macs (restrict via app allowlisting).

## Gotchas
- Casks for apps that self-update are skipped by an ordinary `brew upgrade`; `--greedy` (or `HOMEBREW_UPGRADE_GREEDY=1`) includes them, so use it only if you want brew to manage them.
- Upgrading language runtimes (python, node) can affect environments built on them; communicate before bulk upgrades.

## Verify
Extension attribute of outdated count trending to near zero; scanner findings in `/opt/homebrew/Cellar` paths decrease.

## Checked
2026-10-28. Confirmed against docs.brew.sh Installation (prefix, Tier 3 Intel, pkg installer, root not allowed as owner, security note), FAQ (`HOMEBREW_NO_AUTO_UPDATE`, `HOMEBREW_AUTO_UPDATE_SECS`, `brew pin`, `--greedy`, `HOMEBREW_UPGRADE_GREEDY`, one owning account) and the Manpage (`outdated --quiet` and `--json=v2`, `cleanup --prune`, `pin`). Removed: the `/usr/local` Intel prefix, `brew autoupdate`, the python JSON count, `node@20` pin example, the Santa name, and the claim that upgrading python or node breaks virtualenvs.
Method: documentation only; no commands were run.
