---
id: computing-software.systems-network-administration.dns-dhcp.bind-version-upgrades
name: bind-version-upgrades
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, bind-upgrade, esv, named-checkconf, change-management]
level: practitioner
status: docs-checked
description: "Plan and execute BIND 9 upgrades: ESV vs stable branches, removed options, named-checkconf against the new version, cache/journal handling and rollback."
sources:
  - https://bind9.readthedocs.io/en/latest/notes.html
  - https://kb.isc.org/docs/supported-platforms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIND version upgrades

## Choosing a branch
The upstream repository keeps stable branches `bind-9.18` and `bind-9.20`; `main` currently produces 9.21.x development tags. Check ISC's supported-versions and support-lifetime pages for which branches get fixes, and prefer a supported ISC build (ISC packages or ISC Docker images) over an old distribution build when you need fixes.

## Before the upgrade
1. Read the release notes for every version you skip: removed and changed options. For example, the 9.20.0 notes say `auto-dnssec` was removed in favour of `dnssec-policy` (or manual signing), and `dnssec-enable` is marked ancient in the 9.20 parser. `masters` is a legacy name for `primaries`.
2. Test the config with the new binary:
```
named-checkconf -z /etc/bind/named.conf        # new version, on a test host or in a container
```
3. Back up config, zone files, journals (`.jnl`), DNSSEC keys and `managed-keys.bind`.

## Execution
- Upgrade secondaries/resolvers one at a time behind anycast or with resolver lists, watching
  query success.
- Dynamic and inline-signed zones: keep journals and keys backed up before the first start of the new version, and do not assume you can downgrade afterwards.
- Check logs after start for configuration warnings and key-state messages.

## Rollback
Keep the previous package version available. Rolling back after a dnssec-policy migration requires restoring the backed-up key and journal state.

## Verify
- [ ] `named -V` shows the new version, `rndc status` is clean, zones load with expected serials and validation still works (`dig +dnssec`).

## Checked

Date: 2026-10-26. BIND 9 ARM sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus bind-9.20 branch notes and grammar), read on 2026-10-26. Confirmed: notes-9.20.0 removal of auto-dnssec, ancient status of dnssec-enable and auto-dnssec in lib/isccfg/namedconf.c, named-checkconf -z loading primary zones, existence of bind-9.18 and bind-9.20 branches. Removed unconfirmed claims about ESV lifetimes, odd/even numbering, journal conversion and the version of dnssec-enable removal.

Method: documentation only; no commands were run.
