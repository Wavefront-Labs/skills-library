---
id: computing-software.cryptography-implementation.key-management.ca-key-compromise-recovery
name: ca-key-compromise-recovery
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, ca-compromise, private-ca, pki, certificate-revocation, root-ca, intermediate-ca, incident-response, trust-anchor]
level: sme
status: draft
description: "Recover from a CA private key compromise: revoke and re-issue, distribute new trust anchors, CRL/OCSP actions, relying-party communication and prevention."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://www.rfc-editor.org/rfc/rfc5280#section-5.3.1", "https://cabforum.org/working-groups/server/baseline-requirements/documents/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CA key compromise recovery

SP 800-57 calls CA key compromise the worst case: every certificate the CA signed, and every certificate an attacker
can now sign, is suspect.

## Immediate actions
1. **Contain:** take the CA offline; preserve logs and HSM audit records; determine how the key was exposed
   (HSM credential theft, exported backup, software key file).
2. **Intermediate compromised (root intact):**
   - Root signs a CRL revoking the intermediate with reason `cACompromise` (2) and publishes it at the CDP; update
     OCSP for the intermediate.
   - Stand up a new intermediate with a new key (and a new name or at least new SKI), re-issue all leaf certificates.
3. **Root compromised:**
   - Revocation of a root is not meaningful (it is self-signed); you must **remove it from every trust store**.
   - Pre-distributed backup root (generated and deployed in advance) saves weeks; otherwise push a new root via MDM,
     GPO, config management, container base images and device firmware.

## Re-issuance at scale
- Automated issuance (ACME, cert-manager, SPIFFE) turns re-issuance into a restart; manual certificates are the long
  tail. Inventory decides how fast you recover.
- Rotate subscriber private keys too if the attacker may have obtained them (e.g. CA also held escrowed keys).

## Communication
- Notify relying parties and subscribers with the revocation time, affected serial ranges, and new trust anchor.
- For a publicly trusted CA, Baseline Requirements and root program policies impose notification and revocation
  deadlines (24 hours to 5 days by reason).

## Prevention for next time
- CA keys in HSMs with M-of-N activation; offline root; short-lived intermediates.
- Name constraints on intermediates to limit blast radius.
- Certificate Transparency or internal issuance logs so you can enumerate everything the CA signed.

## Verify
- [ ] Runbook drill: replace an intermediate and re-issue all leaves in a staging PKI within target time.
- [ ] Backup root is present in all trust stores before it is needed.
