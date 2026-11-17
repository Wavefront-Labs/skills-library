---
id: computing-software.data-engineering.apache-hadoop.mapreduce-encrypted-shuffle
name: mapreduce-encrypted-shuffle
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, mapreduce, shuffle, ssl, tls, keystore]
level: advanced
status: docs-checked
description: "MapReduce encrypted shuffle: core-site hadoop.ssl.* settings, mapreduce.shuffle.ssl.enabled, ssl-server.xml and ssl-client.xml keys, truststore reload and caveats."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/EncryptedShuffle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted shuffle

Encrypted shuffle runs the MapReduce shuffle over HTTPS, with optional client authentication. Steps: set the core-site.xml properties on all nodes and mark them `final`; set `mapreduce.shuffle.ssl.enabled` = true (default false) in mapred-site.xml, also `final`; configure ssl-server.xml and ssl-client.xml; set the Linux container executor so job tasks cannot read the server keystore (the page defers to the Hadoop Kerberos configuration docs); restart all NodeManagers to activate.

core-site.xml defaults:
- `hadoop.ssl.require.client.cert`: false (the page says to keep it false for now)
- `hadoop.ssl.hostname.verifier`: DEFAULT (also STRICT, STRICT_IE6, DEFAULT_AND_LOCALHOST, ALLOW_ALL)
- `hadoop.ssl.keystores.factory.class`: `org.apache.hadoop.security.ssl.FileBasedKeyStoresFactory` (the only implementation)
- `hadoop.ssl.server.conf`: `ssl-server.xml`; `hadoop.ssl.client.conf`: `ssl-client.xml` (looked up on the classpath, typically the conf directory)
- `hadoop.ssl.enabled.protocols`: TLSv1.2 (used only by DatanodeHttpServer)

ssl-server.xml (mapred user owns it with exclusive read; keystore and truststore files likewise): `ssl.server.keystore.type` jks, `.location`, `.password`, `ssl.server.truststore.type/.location/.password`, `ssl.server.truststore.reload.interval` 10000 ms. ssl-client.xml mirrors this with `ssl.client.*`; mapred owns it with default permissions.

Truststores reload every 10 seconds by default; copying a new truststore over the old one is picked up without restarting NodeManagers (useful when adding or removing nodes or trusted clients). Other changes need NodeManager restarts.

Caveats from the page:
- Significant performance impact; profile it and consider reserving one or more cores.
- Client certificate keystores must currently be readable by all users submitting jobs, so a rogue job could use them, but without a valid JobToken it cannot fetch shuffle data; a job can only fetch its own.
- Debugging: `-Djavax.net.debug=all` (reducer child opts, or `YARN_NODEMANAGER_OPTS` in yarn-env.sh) is very verbose and slows jobs by orders of magnitude; use only on small jobs.
- Separate feature: `mapreduce.job.encrypted-intermediate-data` (default false) encrypts spill files, with `-key-size-bits` and `.buffer.kb` companions; enabling it restricts the job to one attempt.

## Checked

Method: 2026-11-08, read the project's EncryptedShuffle markdown source in full against this skill. Removed an unsupported "Verify" step (HTTPS fetcher log lines and plain-HTTP rejection are not stated); added the container-executor and ownership details from the page; the property defaults were unchanged.
