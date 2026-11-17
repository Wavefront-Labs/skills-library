---
id: computing-software.systems-network-administration.samba.testparm
name: testparm
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, testparm, config-check, smb-conf-check, parameter-name, smb-conf]
level: intro
status: docs-checked
description: "Validate smb.conf with testparm: dump effective settings, show defaults, query one parameter or section, test hosts allow, and use the exit status in scripts."
sources:
  - https://www.samba.org/samba/docs/current/man-html/testparm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# testparm
```
testparm                          # check default smb.conf, prompt, dump
testparm -s                       # no prompt; print the effective config
testparm -sv                      # also unset parameters at their defaults
testparm -s --parameter-name="security"
testparm -s --section-name=Demo
testparm --show-all-parameters    # with types and possible values
testparm -s /path/to/smb.conf     # a specific file
testparm -s /path/to/smb.conf hostname 10.0.0.5   # would this host pass hosts allow/deny?
testparm --option="log level=3"
```
Options: `-s|--suppress-prompt`, `-v|--verbose`, `--parameter-name` (global section unless a section is given; parametric options use a colon), `--section-name`, `-l|--skip-logic-checks`, `-d`, `--debug-stdout`, `--configfile`, `--option=name=value`, `-V`.

Exit status: 0 when no errors; 1 when smb.conf has an error, so scripts can gate reloads: `testparm -s >/dev/null && smbcontrol all reload-config`.

Gotchas: a clean result does not guarantee shares work; the hostname argument needs a hostIP too; run it after every edit.

## Checked

2026-11-04. Confirmed against the testparm(1) manual page: every option shown, the -s prompt behaviour, -v defaults, --parameter-name scope and colon syntax, --section-name, --show-all-parameters, -l, the hostname hostIP test, the not-a-guarantee note, and exit codes 0 and 1. The reload-config pairing is confirmed on the Samba wiki member troubleshooting page. Removed the claim about `samba-tool testparm`. The IP and paths are illustrative.
Method: documentation only; no commands were run.
