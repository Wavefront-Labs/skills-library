---
id: computing-software.search-and-information-retrieval.apache-solr.update-processor-chains
name: update-processor-chains
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [update-processors, update-request-processor, urp-chain, updateprocessor, indexing-pipeline]
level: advanced
status: docs-checked
description: "Customize Solr indexing with update request processor chains: default chain order, named top-level processors, SolrCloud behaviour before and after DistributedUpdateProcessor."
sources:
  - https://solr.apache.org/guide/solr/latest/configuration-guide/update-request-processors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# update-processor-chains

Update request processors (URPs) transform documents after loading but before indexing. The default chain runs `LogUpdateProcessorFactory`, `DistributedUpdateProcessorFactory` and `RunUpdateProcessorFactory`; `RunUpdateProcessorFactory` executes the update and should be last in every custom chain; without it the updates do not affect the indexed data. If a chain omits `DistributedUpdateProcessorFactory`, Solr inserts it just before `RunUpdateProcessorFactory`.

Define processors once and reuse them:
```
<updateProcessor class="solr.RemoveBlankFieldUpdateProcessorFactory" name="remove_blanks"/>
<updateProcessorChain name="custom" processor="remove_blanks,signature">
  <processor class="solr.RunUpdateProcessorFactory"/>
</updateProcessorChain>
```
Select a chain per request with the `update.chain` parameter.

SolrCloud: processors listed before `DistributedUpdateProcessor` run only on the node that first receives the update. After forwarding, the shard leader and each replica run the processors listed after it. The documented dedupe chain puts `SignatureUpdateProcessorFactory` (which writes the uniqueKey field) before it, so the signature is computed once on the first node. The guide warns that custom post-processors (listed after it, via the `post-processor` attribute) are never invoked for buffered updates replayed on a recovering replica (SOLR-8030) and advises avoiding them.

Bundled factories include DefaultValue, TimestampUpdateProcessorFactory, UUID, CloneField, DocExpiration, AddSchemaFields, ParseDate/Numeric, Trim, Truncate and Script.

Changing a chain usually warrants reindexing.

## Checked

Checked 2026-11-09 against the full Update Request Processors page of the Solr Reference Guide (URP anatomy, default chain, custom chains, top-level updateProcessor elements, SolrCloud pre- and post-processors, update.chain parameter, processor list). Removed the claim that every chain must end with the run processor in absolute terms; added the auto-insert behaviour and the SOLR-8030 warning.

Method: docs-checked 2026-11-09 against the Update Request Processors page (raw ref-guide source); no commands were run.
