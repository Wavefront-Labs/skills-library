---
id: computing-software.cryptography-implementation.secure-implementation.exception-messages-that-leak-crypto-state
name: exception-messages-that-leak-crypto-state
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, aeadbadtagexception, exception-handling, error-oracles, information-leak]
level: practitioner
status: docs-checked
description: "Stop exception types and messages leaking crypto state: Java AEADBadTagException hierarchy, generic external errors with internal logging, and what CWE-209 warns about."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/crypto/AEADBadTagException.html", "https://cwe.mitre.org/data/definitions/209.html", "https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception messages that leak crypto state

## The leak

Error messages and exception types give attackers information. CWE-209 describes a product that
generates an error message including sensitive information about its environment, users or
associated data, and warns that attackers use detailed information to refine their attack. OWASP
adds that error-handling issues can reveal a lot about the target and identify injection points.

In Java, `AEADBadTagException` is thrown when a `Cipher` in an AEAD mode (such as GCM or CCM)
cannot verify the authentication tag. It extends `BadPaddingException`, which extends
`GeneralSecurityException`, so one catch clause can cover tag, padding and other security
failures. Code that reports these (or later parse failures) differently to the caller exposes
which step failed.

## Uniform handling

OWASP's pattern: when an unexpected error occurs, return a generic response and log the error
details server side, not to the user. Applied to decryption:

```java
try {
    byte[] pt = cipher.doFinal(ct);
    return parse(pt);
} catch (GeneralSecurityException | ParseException e) {
    log.debug("decrypt failure id={}", requestId, e);   // internal only
    throw new DecryptionFailed();                        // one type, one message
}
```

- Map decrypt, verify and parse failures to one external error and one status code.
- CWE-209 mitigation: error messages should contain only the minimal details useful to the
  intended audience, and should not reveal the methods used to determine the error.
- Do not include keys, plaintext or full ciphertext in logged messages.

## Verify

- [ ] Tampered tag, tampered body and wrong-length input yield the same external response.
- [ ] Stack traces and exception text never reach the client.

## Checked

Method: docs-checked 2026-11-09 against the Java 21 AEADBadTagException API page, CWE-209 (description, consequences, mitigation), OWASP Error Handling Cheat Sheet (introduction and generic-response sections). Removed: specific padding-oracle and Bleichenbacher claims, "equalise work" timing advice, per-language exception names for Python, Node and .NET, rate-limiting and alerting advice, and the latency check from the verify step, none of which the read sources state.
