---
id: computing-software.search-and-information-retrieval.apache-solr.jvm-heap-sizing
name: jvm-heap-sizing
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [jvm, jvm-settings, heap-size, garbage-collection, xmx, mmapdirectory]
level: practitioner
status: docs-checked
description: "Size the Solr JVM heap: -Xms and -Xmx, GC log analysis, 25-50 percent headroom, and leaving RAM to the OS for MMapDirectory."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/jvm-settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jvm-heap-sizing

The key settings are `-Xms` (initial heap) and `-Xmx` (maximum). Setting both to the same value is common.

Method from the guide:
1. Run with your real data and queries.
2. Analyze the GC logs in the logs directory with a tool such as GCViewer or GCEasy, or watch with `jconsole`, to find memory in use after GC completes. That is the absolute minimum needed.
3. Add 25-50% headroom as a starting point.

Points to keep in mind:
- Too little headroom causes continual GC and heavy resource use.
- Solr uses `MMapDirectory`, so most of the Lucene index is served from RAM the JVM does not hold. Leave as much memory as possible to the operating system.
- Keep the heap as small as performance allows. 8-16 GB is common; larger heaps need extensive testing before production.

There is no one-size-fits-all value. Most modern JVMs do well with defaults when memory is not the issue. The guide also says G1GC is currently preferred, and that on hardware with hundreds of gigabytes of RAM it is often better to run several JVMs with limited heaps (for example as Docker containers).

## Checked

Checked 2026-11-09 against the full JVM Settings page of the Solr Reference Guide. Removed the `bin/solr start -m` sentence, which is not on that page.

Method: docs-checked 2026-11-09 against the JVM Settings page (raw ref-guide source); no commands were run.
