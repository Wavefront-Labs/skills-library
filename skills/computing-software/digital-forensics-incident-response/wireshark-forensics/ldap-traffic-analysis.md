---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.ldap-traffic-analysis
name: ldap-traffic-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [ldap-traffic, protocol-forensics, active-directory, kerberos-traffic, dfir]
level: advanced
status: draft
description: "Analyse LDAP/LDAPS/GC traffic for AD reconnaissance (BloodHound, AdFind), LDAP relay and modifications: filters, search scope, signing and decryption limits."
sources: ["https://datatracker.ietf.org/doc/html/rfc4511", "https://wiki.wireshark.org/LDAP", "https://attack.mitre.org/techniques/T1087/002/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LDAP traffic analysis

**Goal:** Active Directory reconnaissance and many AD attacks travel over LDAP (389), LDAPS (636)
and Global Catalog (3268/3269). Recognise enumeration and malicious modifications on the wire.

## Visibility
- Plain LDAP on 389 is cleartext unless **sealed** by SASL (Kerberos/NTLM with signing+sealing - the default for Windows clients, which encrypts payloads). Many tools (ldapsearch simple bind, some Python tools) send cleartext.
- Wireshark can decrypt Kerberos-sealed LDAP if given a keytab with the relevant keys (Preferences > Protocols > KRB5 > keytab), in lab or with authorised key material.
- LDAPS (636) is TLS: metadata only unless keys are available.

## Display filters
```text
ldap.protocolOp == 3                         # searchRequest
ldap.filter contains "servicePrincipalName"  # Kerberoasting target enumeration
ldap.filter contains "userAccountControl:1.2.840.113556.1.4.803:=4194304"   # AS-REP roastable (DONT_REQ_PREAUTH)
ldap.filter contains "admincount=1"
ldap.protocolOp == 6                         # modifyRequest
ldap.bindRequest_element and ldap.simple    # simple binds (cleartext passwords!)
```

## Recon signatures
- **BloodHound/SharpHound**: bursts of searchRequests with filters like `(objectClass=*)`, `(samAccountType=805306368)`, attributes including `nTSecurityDescriptor`, `msDS-AllowedToActOnBehalfOfOtherIdentity`, paged results control, from a workstation (not a server or DC).
- **AdFind**: many sequential queries for trusts (`trustedDomain`), computers, OUs.
- Volume per source: thousands of results in seconds from a non-admin host.

## Attack signatures
- modifyRequests writing `msDS-KeyCredentialLink` (shadow credentials), `msDS-AllowedToActOnBehalfOfOtherIdentity` (RBCD), group membership (`member`).
- NTLM-authenticated LDAP binds as a machine account from a different IP (relay).

## Host-side correlation
- DC Directory Service event 1644 (expensive/inefficient searches, when enabled) records the filter and client IP; 5136 for modifications.

## Gotchas
- Sealed LDAP hides filters: rely on volume/timing metadata and DC logs.
- Monitoring tools and management servers query LDAP heavily; baseline by source.

## Verify
Recon or modification claims are matched to DC logs (1644/5136) or decrypted payloads.
