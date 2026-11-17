---
id: computing-software.cybersecurity-defensive.endpoint-security.self-encrypting-drives
name: self-encrypting-drives
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [self-encrypting-drives, sed, opal, edrive, hardware-encryption, tcg-opal, disk-encryption]
level: advanced
status: draft
description: "Evaluate self-encrypting drives (TCG Opal/eDrive): why BitLocker defaults to software encryption, firmware flaws, pre-boot authentication, crypto-erase use and policy settings."
sources: ["https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/configure", "https://msrc.microsoft.com/update-guide/vulnerability/ADV180028", "https://trustedcomputinggroup.org/resource/storage-work-group-storage-security-subsystem-class-opal/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Self-encrypting drives

SEDs encrypt in drive firmware (TCG Opal 2.0). The data is always encrypted with the media key; security
depends on how the key is protected and on the firmware being correct.

## Key facts
- 2018 research (Meijer & van Gastel) showed several SSDs with broken hardware encryption (password not cryptographically tied to the key). Microsoft advisory ADV180028 led to BitLocker **defaulting to software encryption** (since KB4516071, 2019) even when the drive supports eDrive.
- To keep using hardware encryption you must explicitly allow it via policy ("Configure use of hardware-based encryption for fixed data/OS drives") with an allow-list of approved drives/algorithms - generally not recommended unless the drive is validated (e.g. FIPS 140-3 / Common Criteria certified for the configuration).
- Opal without pre-boot authentication only locks on power loss; a running or sleeping machine is unlocked.

## Where SEDs are useful
- **Crypto-erase / sanitise:** instant secure erase by changing the media encryption key (NIST SP 800-88 purge) - excellent for decommissioning, even if you also run software encryption.
- Performance on old CPUs (irrelevant with AES-NI).
- Arrays and servers with validated SED + external key manager (KMIP) for drive-removal protection.

## Configuration choices
- Laptops: BitLocker software XTS-AES with TPM (+PIN where needed), regardless of drive type.
- Check what is in use: `manage-bde -status` shows "Encryption Method: Hardware Encryption" vs XTS-AES.
- Data-centre SEDs: manage keys via the array or KMIP server; test drive-removal (drive unreadable outside the array).

## Verify
- [ ] No laptops using hardware encryption unless on the approved list.
- [ ] Decommissioning process uses crypto-erase plus verification record.
