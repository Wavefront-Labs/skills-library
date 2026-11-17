---
id: computing-software.cryptography-implementation.key-management.java-sunpkcs11-provider-configuration
name: java-sunpkcs11-provider-configuration
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, sunpkcs11, pkcs11, java, hsm, keystore, jca]
level: advanced
status: docs-checked
description: "Configure the Java SunPKCS11 provider for HSMs and tokens: config file, Security.addProvider at runtime, KeyStore PKCS11 login, slot selection and attribute templates."
sources: ["https://docs.oracle.com/en/java/javase/21/security/pkcs11-reference-guide1.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/Provider.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java SunPKCS11 provider configuration

## Config file
```
name = HSM
library = /opt/vendor/lib/libpkcs11.so
slotListIndex = 0
attributes(generate, CKO_PRIVATE_KEY, *) = {
  CKA_TOKEN = true
  CKA_SENSITIVE = true
  CKA_EXTRACTABLE = false
}
```
Select the slot with `slot` (the slot ID) or `slotListIndex` (index into the `C_GetSlotList` list); at most one
of them may be given and the default is index 0.

## Load
```java
Provider p = Security.getProvider("SunPKCS11").configure("/etc/pkcs11/hsm.cfg");
Security.addProvider(p);
KeyStore ks = KeyStore.getInstance("PKCS11", p);
ks.load(null, pin);                         // C_Login as user
PrivateKey k = (PrivateKey) ks.getKey("signing-key", null);
Signature s = Signature.getInstance("SHA256withECDSA", p);
```
Or statically in `java.security`: `security.provider.13=SunPKCS11 /etc/pkcs11/hsm.cfg`.

## Gotchas
- Pass the provider object explicitly to `getInstance` so the operation uses the token.
- Each provider instance is tied to one slot; use a distinct `name` per instance (the provider is named
  `SunPKCS11-<name>`).
- `keytool -storetype PKCS11 -providerClass sun.security.pkcs11.SunPKCS11 -providerArg hsm.cfg -list`.
- Disable mechanisms the token implements badly with `disabledMechanisms = { CKM_... }`.

## Verify
- [ ] `keytool -list` shows token entries; signing test runs with the token provider, key not extractable.

## Checked

2026-11-01. Confirmed in the Java SE 21 PKCS#11 Reference Guide: `slot`/`slotListIndex` semantics and default,
`name`, `attributes(...)` templates, `disabledMechanisms`, `Provider.configure`, `security.provider.N` form,
keytool `-providerClass sun.security.pkcs11.SunPKCS11 -providerArg`. Removed: `tokenLabel` and `pkcs11-tool` slot
lookup claims, Java version gate, software-provider fallback reason, session tuning line.
Method: documentation only; no commands were run.
