---
id: computing-software.systems-network-administration.samba.provision-ad-dc
name: provision-ad-dc
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, provision-ad-dc, provision, domain-provision, active-directory, samba-tool]
level: practitioner
status: docs-checked
description: "Provision the first Samba Active Directory domain controller with samba-tool domain provision, interactive or non-interactive, and add the optional reverse zone."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_an_Active_Directory_Domain_Controller
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# provision ad dc
Before provisioning, move the default config aside and clear old databases:
`mv /etc/samba/smb.conf /etc/samba/smb.conf.initial`. Find leftover `*.tdb` and `*.ldb` locations with `smbd -b | egrep "LOCKDIR|STATEDIR|CACHEDIR|PRIVATE_DIR"`.

Interactive:
`samba-tool domain provision --use-rfc2307 --interactive`
Answers used on the wiki: realm `SAMDOM.EXAMPLE.COM`, domain `SAMDOM`, role `dc`, DNS backend `SAMBA_INTERNAL`, forwarder `8.8.8.8` (or `none`).

Non-interactive:
`samba-tool domain provision --server-role=dc --use-rfc2307 --dns-backend=SAMBA_INTERNAL --realm=SAMDOM.EXAMPLE.COM --domain=SAMDOM --adminpass=Passw0rd`

Notes:
- `--use-rfc2307` enables the Unix Attributes tab; recommended for new domains.
- `--adminpass` must meet complexity rules or provisioning fails.
- Do not use `NONE` or `BIND9_FLATFILE` as the DNS backend.
- Bind to chosen NICs with `--option="interfaces=lo eth0" --option="bind interfaces only=yes"`.
- Never re-provision further DCs in the same domain; join them instead.
- Interactive provisioning does not enable Group Policy; edit smb.conf for that.
- Realm and DNS zone cannot be renamed later; avoid `.local`.

Optional reverse zone and PTR for the DC (start Samba first; `<DNS-IP>` is the AD DNS server IP or hostname):
`samba-tool dns zonecreate <DNS-IP> 0.99.10.in-addr.arpa -U Administrator`
`samba-tool dns add <DNS-IP> 0.99.10.in-addr.arpa 1 PTR dc1.samdom.example.com -U Administrator`

Verify: `smbclient -L localhost -N` lists netlogon and sysvol.

## Checked

2026-11-04. Confirmed against the Samba wiki page Setting up Samba as an AD DC: smb.conf.initial step, the smbd -b path lookup, interactive and non-interactive commands and answers, --use-rfc2307, --adminpass complexity, unsupported NONE and BIND9_FLATFILE backends, interfaces options, do-not-reprovision rule, Group Policy note, no renaming and .local warning, zonecreate and PTR commands, smbclient verification. Removed the claim that PTRs are never created automatically.
Method: documentation only; no commands were run.
