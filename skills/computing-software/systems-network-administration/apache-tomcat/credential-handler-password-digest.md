---
id: computing-software.systems-network-administration.apache-tomcat.credential-handler-password-digest
name: credential-handler-password-digest
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, credentialhandler, messagedigestcredentialhandler, secretkeycredentialhandler, nestedcredentialhandler, password-hashing, pbkdf2, salt, iterations]
level: advanced
status: docs-checked
description: "Store Tomcat 10.1 Realm passwords hashed: MessageDigestCredentialHandler, SecretKeyCredentialHandler (PBKDF2) and NestedCredentialHandler attributes, defaults and an example."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/credentialhandler.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CredentialHandler

A Realm nests at most one `<CredentialHandler className="...">`; the class must implement `org.apache.catalina.CredentialHandler`. With none specified, a MessageDigestCredentialHandler is used with no algorithm, so stored passwords are treated as clear text.

Implementations named on the page: MessageDigestCredentialHandler, SecretKeyCredentialHandler and NestedCredentialHandler (the page gives no package names; use the fully qualified class name from the Javadoc in `className`).

MessageDigestCredentialHandler:
- `algorithm`: a `java.security.MessageDigest` name; unset = clear text.
- `encoding` UTF-8; `iterations` and `saltLength` apply when creating new credentials.
- `digestInRfc3112Order` false (default changes in Tomcat 12).

SecretKeyCredentialHandler:
- `algorithm` `PBKDF2WithHmacSHA1`, `keyLength` 160, `iterations`, `saltLength`.

If a stored value has no iteration count, 1 is assumed; no salt, none is used.

Stored forms MessageDigestCredentialHandler accepts: plain text (no algorithm), hex digest, `{MD5}` or `{SHA}` Base64 digest, `{SSHA}` salted SHA1 (digest plus salt, Base64), and `salt$iterationCount$encodedCredential` (hex). SecretKeyCredentialHandler accepts the `salt$iterationCount$encodedCredential` form.

NestedCredentialHandler delegates to sub-handlers defined by nesting `<CredentialHandler>` elements inside it. Credentials are matched against each in the listed order, and a match against any one is enough (useful when migrating hash formats).

## Checked

2026-11-04. Read the Tomcat 10.1 CredentialHandler page (config/credentialhandler.html) and the Realm page (config/realm.html): confirmed the default MessageDigestCredentialHandler, the MessageDigest, SecretKey and Nested attributes and defaults, the stored password forms, the iteration count 1 and no-salt fallbacks, the nested ordering rule and the at-most-one nesting rule in a Realm. Removed the package-qualified class names and the XML example built on them, the bin/digest script instructions and the verify step, none of which the pages show.

Method: documentation only; no commands were run.
