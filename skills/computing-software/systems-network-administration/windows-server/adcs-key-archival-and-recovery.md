---
id: computing-software.systems-network-administration.windows-server.adcs-key-archival-and-recovery
name: adcs-key-archival-and-recovery
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-cs, key-recovery-agent, key-archival, certutil, encryption-certificates]
level: advanced
status: docs-checked
description: "Configure AD CS key archival with key recovery agents for encryption certificates (EFS, S/MIME), and recover an archived private key with certutil."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/configure-key-archival-recover-private-keys
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key archival and key recovery agents

For encryption certificates (EFS, S/MIME), losing the private key means losing the data. The CA can archive the
private key at issuance, encrypted to Key Recovery Agent (KRA) certificates.

## Set up
1. **KRA template**: issue the "Key Recovery Agent" template to a small, trusted group (pending CA manager approval).
2. KRA users enrol and the CA manager approves. Back up the KRA certificate + private key offline (PFX in a vault).
3. In the CA properties, configure the Recovery Agents page with the number of KRA certificates to use and add the
   KRA certificates (Microsoft does not publish a detailed current procedure for this page; follow your CA's version
   guidance). Each archived key is encrypted once to every KRA public key in use.
4. On the encryption template (for example a copy of User for S/MIME), enable private-key archival.

## Recover a key
```cmd
REM find the archived certificate by user or serial
certutil -getkey <serial_number> recover.blob
REM a KRA (holding the KRA private key) decrypts:
certutil -recoverkey recover.blob user-recovered.pfx
```
The `-getkey` search token can be a common name, serial number, thumbprint, key identifier, requester name (domain\user)
or UPN; with several matches it writes a script instead. `-getkey <token> recover <BaseName>` retrieves and recovers in one
step (needs the KRA certificate and key) and writes a `.p12` file.
Give the PFX to the user over a secure channel; import with the password.

## Role separation
Certificate managers retrieve the blob (`-getkey`), KRAs decrypt (`-recoverkey`); assign the roles to different
people. Use dual authorization as an operational control.

## Gotchas
- Enrol a test subject only after the CA has a valid KRA configuration; keys issued before archival was configured are not covered.
- The KRA private key is required to decrypt: protect and back up KRA certificates and keys, and keep KRA enrolment manual and individually approved (no autoenrollment).
- Do not archive signing keys; non-repudiation requires they exist only with the user.

## Verify
- [ ] Test user's S/MIME key recovered to a PFX that decrypts a test message.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs main branch, last commit 2026-10-23. Confirmed: the Key Recovery Agent template and manual approval of KRA enrolment, separation of the certificate manager (retrieve) and KRA (decrypt) roles, encryption of the archived key to each KRA public key, the advice not to archive signing keys, and the certutil -getkey (blob, script, retrieve, recover and search tokens) and -recoverkey syntax. Removed as unconfirmed: the Restart CertSvc step, the exact Request Handling checkbox label, the CA-side exportability sentence, the KeyRecoveryHashes column in the -view example, and the role separation switch. The CA Recovery Agents page procedure is not documented in detail on the current page; the skill says so.

Method: documentation only; no commands were run.
