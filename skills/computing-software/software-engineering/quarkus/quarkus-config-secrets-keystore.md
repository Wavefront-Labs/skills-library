---
id: computing-software.software-engineering.quarkus.quarkus-config-secrets-keystore
name: quarkus-config-secrets-keystore
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, secrets, encryption, keystore, smallrye-config-crypto, configuration]
level: practitioner
status: docs-checked
description: "Encrypt Quarkus config values with smallrye-config-crypto and aes-gcm-nopadding, then move secrets and the encryption key into Java KeyStores."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/config-secrets.adoc
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/config-mappings.adoc
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/config-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted secrets and KeyStores in Quarkus config

A secret is written as `${handler::value}`, where `handler` is the name of an `io.smallrye.config.SecretKeysHandler`. Of the SmallRye handlers, only `smallrye-config-crypto` is supported by Quarkus.

## Encrypt a value
Add the managed dependency `io.smallrye.config:smallrye-config-crypto`, then run:

```bash
quarkus config set --encrypt my.secret 1234
```

This writes to `application.properties` the value encrypted and Base64 encoded, wrapped in `${aes-gcm-nopadding::...}`, and generates `smallrye.config.secret-handler.aes-gcm-nopadding.encryption-key` if missing:

```properties
my.secret=${aes-gcm-nopadding::DLTb_9zxThxeT5iAQqswEl5Dn1ju4FdM9hIyVip35t5V}
smallrye.config.secret-handler.aes-gcm-nopadding.encryption-key=DDne5obnfH1RSeTg71xSZg
```

The default handler uses `AES/GCM/NoPadding`. Looking up `my.secret` decrypts automatically, provided the same encryption key is configured. In code, `config.getConfigValue("my.secret").getValue()` returns `1234`.

## Move secrets into a KeyStore
Encrypted values are still in `application.properties`. Add `io.smallrye.config:smallrye-config-source-keystore` and treat a Java KeyStore as a file-based vault. The alias is the property name:

```bash
echo DLTb_9zxThxeT5iAQqswEl5Dn1ju4FdM9hIyVip35t5V | keytool -importpass -alias my.secret -keystore properties -storepass arealpassword -storetype PKCS12 -v
```

Keep the encryption key in a separate KeyStore (alias `smallrye.config.secret-handler.aes-gcm-nopadding.encryption-key`, file `key`, own `-storepass`). Then configure:

```properties
smallrye.config.source.keystore."properties".path=properties
smallrye.config.source.keystore."properties".password=arealpassword
smallrye.config.source.keystore."properties".handler=aes-gcm-nopadding
smallrye.config.source.keystore."key".path=key
smallrye.config.source.keystore."key".password=anotherpassword
```

## Protect the KeyStore password
The KeyStore password itself is sensitive. A leak alone does not expose secrets, since the attacker also needs the keystore file. Restrict file access to a limited set of roles and run Quarkus in one of them, set the password as an environment variable, and rotate it periodically.

## Related
`@ConfigMapping` members can be typed `Secret<String>`: the name is omitted from `Config#getPropertyNames()`, name and value are omitted from the mapping `toString` output, and retrieving the value through the programmatic `Config` API throws `SecurityException`.

## Checked

2026-11-07. Read in full: config-secrets.adoc, config-mappings.adoc, config-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the claim that the value name is hidden from `toString`; the wording now follows the page (name omitted from `getPropertyNames()`, name and value omitted from the mapping `toString`, `SecurityException` on programmatic access). Added config-reference.adoc to sources.

Method: documentation only; no commands were run.
