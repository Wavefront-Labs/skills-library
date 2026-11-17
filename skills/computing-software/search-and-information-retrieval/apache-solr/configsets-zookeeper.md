---
id: computing-software.search-and-information-retrieval.apache-solr.configsets-zookeeper
name: configsets-zookeeper
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [configsets, configset-api, zk-upconfig, default-configset, forbidden-file-types]
level: practitioner
status: docs-checked
description: "Manage Solr configsets: _default and sample_techproducts_configs, ZooKeeper storage in SolrCloud, uploading with bin/solr zk upconfig or the Configsets API, forbidden file types."
sources:
  - https://solr.apache.org/guide/solr/latest/configuration-guide/config-sets.html
  - https://solr.apache.org/guide/solr/latest/deployment-guide/solr-control-script-reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# configsets-zookeeper

A configset bundles `solrconfig.xml`, the schema and resources (synonyms.txt and others) under a name that collections or cores reference. Examples ship in `server/solr/configsets`: `_default` and `sample_techproducts_configs`.

SolrCloud:
- Configsets live in ZooKeeper, not the file system. `_default` is uploaded at initialization.
- Creating a collection without naming a configset copies `_default` under a unique name for that collection.
- Upload with the Configsets API or `bin/solr zk upconfig`; add one file to an existing configset with `bin/solr zk cp` or the API. Download with `bin/solr zk downconfig -z <zkHost> -n <name> -d /path/to/configset`.
- ZooKeeper's default file limit is 1 MB. Larger files need a raised limit, or must sit on every node's file system.

Forbidden upload and download types by default: class, java, jar, tgz, zip, tar, gz. Override with a comma-separated list (no dots) in `-Dsolr.configset.forbidden.file.types` or `SOLR_CONFIG_SET_FORBIDDEN_FILE_TYPES`.

## Checked

2026-11-04. Confirmed against the Configsets page and the Control Script Reference: example configsets, ZooKeeper storage, `_default` copy behaviour, `zk cp`, `zk downconfig`, the 1MB ZooKeeper file limit, forbidden file types property. Removed a generic closing tip.

Method: documentation only; no commands were run.
