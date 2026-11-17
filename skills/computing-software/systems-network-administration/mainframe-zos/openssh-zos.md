---
id: computing-software.systems-network-administration.mainframe-zos.openssh-zos
name: openssh-zos
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, sshd-zos, ssh-keys-zos, racf-keyrings, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Secure access"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenSSH on z/OS

Goal: secure shell access.
- `/etc/ssh/sshd_config`, host keys, RACF keyring option; started task `SSHD`.
- Enable key auth; disable password auth where policy allows.
- Check `BPX.DAEMON` and surrogate profiles.
Verify: key-based login works and weak ciphers are off.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
