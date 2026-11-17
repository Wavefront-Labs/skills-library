---
id: computing-software.cryptography-implementation.applied-cryptography.verify-then-parse-and-signature-stripping
name: verify-then-parse-and-signature-stripping
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, digital-signatures, signature-stripping, verify-then-parse, signature-wrapping, xml-dsig, saml, optional-signatures, fail-closed]
level: advanced
status: docs-checked
description: "Prevent signature stripping and wrapping: mandatory signatures, verify before parsing, use only verified content; SAML/XML-DSig and optional-signature failures."
sources: ["https://www.usenix.org/system/files/conference/usenixsecurity12/sec12-final91.pdf", "https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verify-then-parse and signature stripping

Three related bug classes defeat correct signature algorithms:

1. **Stripping**: the attacker removes the signature and the verifier, finding
   none, proceeds (signature treated as optional, or "unsigned = legacy").
2. **Wrapping**: the verifier checks a signature over one part of a document
   but the application reads a different part (XML Signature Wrapping attacks on SAML
   implementations were described in 2012; see OWASP's SAML cheat sheet).
3. **Parse-before-verify**: the application parses and acts on fields (or
   parser bugs trigger) before verification completes.

## Rules

- **Signatures are mandatory** for a message type. Configuration, not the
  message, decides whether a signature is required. No "if signature present,
  verify" branches.
- **Verify first, over raw bytes**, then parse only those bytes (see signing
  canonical data). For envelope formats, use the library function that returns
  the verified payload and use only that return value.
- **One source of truth**: never look up data by ID elsewhere in the document
  after verification. In SAML, check that the signature `Reference URI` resolves to the signed
  Assertion or Response, use only that assertion, and reject assertions outside
  the validated signed content (OWASP SAML Security Cheat Sheet).
- **Fail closed**: exceptions, unknown algorithms, missing keys and malformed
  signatures all reject.
- **Downgrade**: a "version 1 unsigned" format must be retired, not accepted
  as fallback; otherwise attackers send v1.

## Patterns to grep for

```text
if (msg.signature != null) verify(...)          // optional signature
parse(json) ... then verify(sig, serialize(obj)) // parse before verify, re-serialize
getElementsByTagName("Assertion")[0]             // reads first assertion, not the signed one
catch (SignatureException e) { log; continue; }  // fail open
```

## Testing

- Remove the signature: rejected.
- Duplicate the signed element and modify the unsigned copy (XSW tests): rejected.
- Signature valid but over different content (signature from another
  message): rejected.

## Verify

- [ ] Signature requirement enforced by configuration for each message type.
- [ ] Application uses only the payload returned by the verify call.
- [ ] Stripping and wrapping tests in the test suite.

## Checked

- 2026-11-01. Confirmed (OWASP SAML Security Cheat Sheet): XML Signature Wrapping attacks on SAML were described in 2012; the signature Reference URI must resolve to the signed Assertion or Response and the assertion used must be covered by the validated signature.
- Removed as unconfirmed: library function names, SAML Raider, the Duo source (page unreadable), and the claim about most implementations.
- The grep patterns and rules are design guidance, not cited figures.

Method: documentation only; no commands were run.
