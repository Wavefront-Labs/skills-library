---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.ad-cs-certificate-abuse-investigation
name: ad-cs-certificate-abuse-investigation
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [adcs-abuse, credential-theft, active-directory, golden-certificate, dfir]
level: sme
status: draft
description: "Investigate Active Directory Certificate Services abuse (ESC1-ESC8, Certifried, golden certificates): CA logs, issued certs, events 4886/4887 and remediation."
sources: ["https://posts.specterops.io/certified-pre-owned-d95910965cd2", "https://attack.mitre.org/techniques/T1649/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD CS certificate abuse investigation

**Goal:** certificate-based attacks (ATT&CK T1649; SpecterOps "Certified Pre-Owned") let attackers
authenticate as any user, often surviving password resets for the certificate lifetime.

## Common techniques
| ID | Abuse | Evidence |
|---|---|---|
| ESC1 | Template allows enrollee-supplied subject (SAN) + client auth | Issued cert with SAN UPN of a privileged user requested by a low-priv account |
| ESC2/3 | Any-purpose / enrollment agent templates | Certificates issued "on behalf of" others |
| ESC4 | Writable template ACL -> attacker makes template vulnerable | 5136 changes to `pKICertificateTemplate` objects; 4899/4900 template updates |
| ESC6 | `EDITF_ATTRIBUTESUBJECTALTNAME2` on CA | CA registry flag; any template SAN abuse |
| ESC8 | NTLM relay to HTTP enrollment (`/certsrv`) | IIS logs on CA web enrollment, relay from coerced DC authentication |
| Golden cert | CA private key stolen | CA backup/export events, `certutil -backupkey`, no issuance logs for forged certs |

## Evidence sources
- CA **Security** log (requires "Audit Certification Services" and CA auditing enabled):
  4886 request received, **4887 approved and issued** (requester, template, attributes incl. SAN),
  4888 denied, 4898 template loaded, 4899/4900 template changes.
- CA database: `certutil -view -restrict "NotBefore>=10/01/2026" -out "RequestID,RequesterName,CommonName,CertificateTemplate,RequestAttributes,SerialNumber"`
  - lists all issued certs including SAN request attributes.
- DC: **4768** TGT requests with `Certificate Information` fields (PKINIT) - Certificate Issuer/Serial/Thumbprint show which cert authenticated.
- Tooling on attacker hosts: Certify, Certipy (Linux, shows in 4768 from non-Windows), Rubeus `asktgt /certificate`.

## Remediation
- Revoke abused certificates (`certutil -revoke <serial>`), publish CRL; fix template flags/ACLs and CA flags.
- If CA key is compromised: build a new PKI, remove the old CA from NTAuth (`certutil -viewdelstore -enterprise NTAuth`), re-issue.
- Patch Certifried (CVE-2022-26923) and enable strong certificate mapping (KB5014754 enforcement).

## Gotchas
- CA auditing is off by default; database still holds issuance records.
- Revoking does not stop PKINIT unless DCs check revocation and CRL is reachable; verify.

## Verify
Every certificate issued with privileged SANs during the window is accounted for and revoked if malicious.
