---
id: computing-software.systems-network-administration.linux.sosreport-collection
name: sosreport-collection
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sos, sosreport, sos-report, sos-clean, sos-collect, support-case, diagnostics, obfuscation, rhel, ubuntu, troubleshooting, sysadmin]
level: practitioner
status: docs-checked
description: "Gather support diagnostics with sos: running sos report with the right plugins, obfuscating with sos clean, multi-node sos collect, uploading to a case, and reading a sosreport yourself."
sources:
  - https://github.com/sosreport/sos
  - https://github.com/sosreport/sos/blob/main/man/en/sos-report.1
  - https://github.com/sosreport/sos/blob/main/man/en/sos-clean.1
  - https://github.com/sosreport/sos/blob/main/man/en/sos-collect.1
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# sos report collection

**Goal:** hand a vendor (or yourself) a complete, sanitised snapshot of a host's config,
logs and state in one archive — the first thing every Linux support case asks for.

## 1. Run it
```bash
# install the sos package from your distribution
sos report --batch --case-id 01234567  # non-interactive; --case-id labels the archive
sos report --batch --all-logs          # include rotated/compressed logs, not just current
sos report -o networking,logs,systemd --batch        # only some plugins (faster)
sos report -e podman,kdump -k logs.all_logs=on      # enable extra plugins / plugin options
sos report -l                          # list plugins and options
```
Runs as root. `--all-logs` can drastically increase the archive size; check free space in the temporary directory (`--tmp-dir` changes it).

## 2. Sanitise before sending
```bash
sos report --batch --clean                    # obfuscate during collection
sos clean /var/tmp/sosreport-*.tar.xz         # or afterwards
```
`sos clean` replaces hostnames, IPs, MACs, usernames and keywords (`--keywords secretproject`) consistently and
writes a mapping file in the same location as the archive (keep it private) so you can translate references back. It doesn't
catch everything — skim `etc/` for credentials in custom files.

## 3. Many nodes
```bash
sos collect --nodes web01,web02,db01 --batch --case-id 01234567    # over SSH, one tarball per node + wrapper
sos collect --cluster-type pacemaker --batch                        # discover nodes from the cluster
```

## 4. Upload
`sos report --upload` with the `--upload-*` options (see sos-report(1); with `--batch`, credentials must come from
options or environment variables) or attach the tarball to the case manually.

## 5. Reading one yourself
```bash
tar xf sosreport-*.tar.xz && cd sosreport-*/
ls; ls sos_commands/                    # command outputs are grouped per plugin
```

## Gotchas
- The archive contains sensitive data even after cleaning; transfer and store it like a backup, delete when the case closes.
- On a hung or overloaded host, use `-o` with a narrow plugin set and `--plugin-timeout`, or the run may never finish.

## Verify
- [ ] The tarball exists and `tar tf` lists the expected logs.
- [ ] If cleaned, `grep -r <real-hostname>` in the extracted archive finds nothing; the mapping file stays local.

## Checked

Checked 2026-10-27 against sos man pages sos-report(1), sos-clean(1), sos-collect(1) from sosreport/sos main, 2026-10-27. Confirmed: sos report options --batch, --case-id, --all-logs, -o/-e/-k/-l, --plugin-timeout, --tmp-dir, --clean, --upload and --upload-* options, sos clean mapping file location and --keywords, sos collect --nodes and --cluster-type. Removed or softened: default archive file name and path, run-time and size figures, the .sha256 file, the Red Hat portal upload remark, archive layout details, xsos and legacy sosreport wrapper remarks.

Method: documentation only; no commands were run.
