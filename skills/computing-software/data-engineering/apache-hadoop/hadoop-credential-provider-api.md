---
id: computing-software.data-engineering.apache-hadoop.hadoop-credential-provider-api
name: hadoop-credential-provider-api
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, security, credential-provider, jceks, secrets, keystore]
level: advanced
status: docs-checked
description: "Storing Hadoop secrets in credential providers: provider URI types, hadoop credential create, the provider path property, keystore password options and clear-text fallback."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/CredentialProviderAPI.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credential provider API

Keep passwords out of config XML. Create an entry (alias matches the config property name):

```
hadoop credential create ssl.server.keystore.password -value 123 -provider localjceks://file/path/to/aws.jceks
```

Other subcommands are in the Commands Manual.

Provider URIs:
- `user:///`: the user's Credentials file
- `jceks://SCHEME/path`: Java keystore on a Hadoop filesystem, e.g. `hdfs://nn:9001/user/alice/secret.jceks` becomes `jceks://hdfs@nn:9001/user/alice/secret.jceks`
- `localjceks://file/path`: local only, avoids a recursive HDFS dependency
- `bcfks://` and `localbcfks://`: Bouncy Castle FIPS equivalents

Configuration:
- `hadoop.security.credential.provider.path`: comma-separated providers, checked in order; if unset, `getPassword()` skips providers
- `hadoop.security.credstore.java-keystore-provider.password-file`
- `hadoop.security.credential.clear-text-fallback`: default true; false forces provider lookups

Keystore password: default is the hardcoded "none" (relies on file permissions); or env `HADOOP_CREDSTORE_PASSWORD`; or a clear-text password file with strict permissions. Every reading process needs the same password.

Consumers include HDFS SSL via `DFSUtil`, KMS and HttpFS SSL, YARN WebAppUtils, LDAP groups mapping, S3A, WASB and ADLS. They resolve secrets via `Configuration.getPassword()`, using the same property names as clear-text passwords, so migration stays backward compatible. The whole provider path is checked before falling back to clear text.

Notes from the page: the keystore password is not the primary protection (OS file permissions are), and keystore files cannot be read by standard tools such as cat or editors, though code using the API can. Local providers (`localjceks`, `localbcfks`) are loaded by the process reading the config, so for YARN the files must be visible on every host. Filesystems such as s3a, abfs, adls and wasb refuse keystores on their own scheme, to avoid infinite recursion. With `hadoop.security.credential.clear-text-fallback` set to false, all `getPassword()` lookups must be served by a provider.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (CredentialProviderAPI.md in the apache/hadoop repo). Claims were accurate; added caveats and removed an unsupported "Verify" step.
