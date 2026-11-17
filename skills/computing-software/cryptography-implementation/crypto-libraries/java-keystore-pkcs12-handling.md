---
id: computing-software.cryptography-implementation.crypto-libraries.java-keystore-pkcs12-handling
name: java-keystore-pkcs12-handling
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, jca, jce, java-keystore, pkcs12, keystore-api, secret-key-entry]
level: practitioner
status: docs-checked
description: "Load and write Java KeyStores in code: PKCS12 type, getKey and certificate chains, SecretKeyEntry, password handling and the default keystore type."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/KeyStore.html", "https://docs.oracle.com/en/java/javase/21/security/java-cryptography-architecture-jca-reference-guide.html", "https://docs.oracle.com/en/java/javase/21/security/sunmscapi-provider.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KeyStore PKCS12 handling (Java)

## Load and read
```java
char[] pw = System.getenv("KEYSTORE_PASSWORD").toCharArray();
KeyStore ks = KeyStore.getInstance("PKCS12");
try (InputStream in = Files.newInputStream(Path.of("api.p12"))) {
    ks.load(in, pw);
}
PrivateKey key = (PrivateKey) ks.getKey("api", pw);
Certificate[] chain = ks.getCertificateChain("api");
Arrays.fill(pw, '\0');
```
- `KeyStore.getInstance(File, char[])` returns a loaded keystore of the appropriate type for the file.
- `KeyStore.getDefaultType()` returns the `keystore.type` Security property, or `"jks"` if unset, so name
  `"PKCS12"` explicitly instead of relying on the default.
- `getKey` returns null if the alias does not exist or is not a key entry; `getCertificateChain` returns the
  user's certificate first, then CAs, or null. List aliases with `Collections.list(ks.aliases())` when unsure.

## Write
```java
KeyStore ks = KeyStore.getInstance("PKCS12");
ks.load(null, null);
ks.setEntry("api", new KeyStore.PrivateKeyEntry(key, chain),
            new KeyStore.PasswordProtection(pw));
ks.setEntry("data-kek", new KeyStore.SecretKeyEntry(aesKey),
            new KeyStore.PasswordProtection(pw));
try (OutputStream out = Files.newOutputStream(Path.of("app.p12"))) { ks.store(out, pw); }
```
`SecretKeyEntry` stores a secret key (the KeyStore API page's sample saves one). Which PKCS12 key and MAC
protection algorithms your JDK writes, and OS or HSM keystore types, depend on the JDK version and providers:
look them up in your JDK's documentation (the Windows and macOS keystore types were not checked here).

## Rules
- Passwords as `char[]` from env/secret store, zeroed after use. Never hardcode them in properties
  files committed to git.
- The API allows different passwords for the store and for entries; if tools such as keytool will open the
  store, test with the passwords you plan to use.
- Reload on change for rotated certificates (watch the file, or reload on a timer) instead of
  restarting.
- Don't put many unrelated keys in one store; one store per service limits blast radius.

## Verify
- [ ] Startup fails clearly if the alias is missing or the chain is empty.
- [ ] `keytool -list -v -keystore app.p12` shows the expected entries and algorithms.
- [ ] No keystore password appears in source, logs or `ps` output.

## Checked
2026-10-28. Confirmed against the JDK 21 KeyStore API page: `getInstance(File, char[])`, default type from
`keystore.type` else "jks", `getKey` and `getCertificateChain` null/ordering behaviour, `SecretKeyEntry`,
separate passwords allowed. Removed: JKS cannot store secrets (the page's own JKS sample saves a secret key),
PKCS12 protection algorithms and property names, JDK version gates, lower-cased aliases, wrong-password exception
chain, Windows, macOS and PKCS11 keystore types (the SunMSCAPI page fetched was a stub). The Java code was not
compiled or run.
Method: documentation only; no commands were run.
