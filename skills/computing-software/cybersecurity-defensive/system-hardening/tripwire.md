---
id: computing-software.cybersecurity-defensive.system-hardening.tripwire
name: tripwire
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [tripwire, file-integrity-monitoring, open-source-tripwire, twpol, integrity-check, fim]
level: practitioner
status: docs-checked
description: "Run Open Source Tripwire for file integrity monitoring: site and local keys, policy file rules, database init, integrity checks, updating after approved changes, and reporting."
sources: ["https://github.com/Tripwire/tripwire-open-source", "https://github.com/Tripwire/tripwire-open-source/blob/master/man/man4/twpolicy.4", "https://github.com/Tripwire/tripwire-open-source/blob/master/man/man8/tripwire.8", "https://github.com/Tripwire/tripwire-open-source/blob/master/man/man8/twadmin.8", "https://github.com/Tripwire/tripwire-open-source/blob/master/man/man8/twprint.8"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tripwire (open source)

Open Source Tripwire is the original host-based integrity checker: it records file attributes and hashes in a
signed database and reports differences.

## Keys
- **Site key** signs the configuration and policy files (shared across hosts in a site).
- **Local key** signs the database and reports on each host.
Keys are protected by passphrases (change them with `twadmin --change-passphrases`); store the passphrases in a vault. Generate keys with
`twadmin --generate-keys --site-keyfile site.key` and `twadmin --generate-keys --local-keyfile <host>-local.key`.

## Policy (twpol.txt)
```
@@section FS
SEC_CRIT = $(IgnoreNone)-a ;       # critical files: every property except access time
SEC_BIN  = $(ReadOnly) ;           # binaries: should never change
SEC_CONFIG = $(Dynamic) ;          # configs: content changes expected occasionally
(rulename = "Critical system binaries", severity = 100)
{
  /usr/bin   -> $(SEC_BIN) ;
  /usr/sbin  -> $(SEC_BIN) ;
}
(rulename = "Config files", severity = 80)
{
  /etc       -> $(SEC_CONFIG) ;
  !/etc/mtab ;                      # exclusion
}
```
Property masks: `p` permissions, `i` inode, `n` links, `u`/`g` owner, `s` size, `m` mtime, `c` ctime, hashes
`M` MD5, `S` SHA, `H` Haval, `C` CRC32. Predefined variables: `ReadOnly`, `Dynamic`, `Growing`, `IgnoreNone`,
`IgnoreAll`, `Device`.
Only one rule may apply to any given object; a file with more than one rule makes Tripwire exit with an error without scanning.

Sign it: `twadmin --create-polfile -S site.key /etc/tripwire/twpol.txt`, then delete or secure the plaintext.

## Database and checks
```bash
tripwire --init                         # baseline database (signed with local key)
tripwire --check --email-report         # or schedule via cron daily
twprint --print-report --twrfile <report>.twr
```

## After approved changes
`tripwire --update --twrfile <latest report>` opens the report in an editor where you select the changes to accept
into the database. Policy edits: `tripwire --update-policy twpol.txt` (policy and database files are binary and signed, so you are prompted for the site and local passphrases).

## Protect Tripwire itself
Keep a copy of the database, policy, config and binaries off-host or on read-only media; an attacker with root
can otherwise re-init the database.

## Verify
Modify a test binary under `/usr/local/bin` and the next check reports it under the binaries rule with severity
100; after `--update` the next check is clean.

## Checked
Checked 2026-10-25 against the Open Source Tripwire manual pages twpolicy(4), tripwire(8), twadmin(8) and twprint(8) (Tripwire/tripwire-open-source; the repository's last commit is 2019-03-16, so the pages describe a stable but old release). Confirmed: property mask letters and the predefined variables (ReadOnly, Dynamic, Growing, Device, IgnoreAll, IgnoreNone), `rulename` and `severity` attributes, stop points (`!path ;`), `@@section`, `tripwire --init`, `--check --email-report`, `--update --twrfile`, `--update-policy`, `twadmin --create-polfile -S`, `--generate-keys` with `--site-keyfile`/`--local-keyfile`, `--change-passphrases`, and `twprint --print-report --twrfile`. Corrected: the sample `$(IgnoreNone)-SHa` also removed the SHA and Haval hashes, not just access time; the example now uses `-a`. Removed unconfirmed: Debian package prompts, distribution policy defects and report directory path.

Method: documentation only; no commands were run.
