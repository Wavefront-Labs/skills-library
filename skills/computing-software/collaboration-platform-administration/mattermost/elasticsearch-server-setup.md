---
id: computing-software.collaboration-platform-administration.mattermost.elasticsearch-server-setup
name: elasticsearch-server-setup
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [elasticsearch, search-indexing, analysis-icu, cjk-analyzers]
level: advanced
status: docs-checked
description: "Install Elasticsearch for Mattermost search: dedicated server, network and destructive-requires-name settings, mandatory analysis-icu plugin and CJK plugins."
sources: ["https://docs.mattermost.com/administration-guide/scale/elasticsearch-setup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Elasticsearch server setup

Elasticsearch indexes post data for fast, near real-time search, managed from the System Console once connected. Run it on a dedicated machine separate from the Mattermost server. Two stages: set up Elasticsearch, then configure Mattermost.

Server steps (Elasticsearch v9 or v8):
1. Install, then enable and start under systemd (daemon-reload, enable elasticsearch.service, start).
2. Check with curl localhost:9200.
3. Find the network interface name with ip addr, edit /etc/elasticsearch/elasticsearch.yml, and replace the network.host value _eth0_ with it.
4. Set action.destructive_requires_name to false so wildcard operations work.
5. Restart and confirm with netstat -plnt that ports 9200 and 9300 listen on the server's IP.
6. Install the analysis-icu plugin with elasticsearch-plugin install analysis-icu on every node; it is required because Mattermost's post and file index templates depend on it. Restart each node (one at a time in production) and verify with the _cat/plugins request, which should list analysis-icu once per node.
7. Optionally install analysis-nori (Korean), analysis-kuromoji (Japanese) or analysis-smartcn (Chinese), restart, then enable the EnableCJKAnalyzers setting. On a server with indexed content, purge and rebuild the index in System Console > Environment > Elasticsearch for the analyzers to apply to existing posts.
8. Test reachability from the Mattermost host with curl against port 9200.

Mattermost side: System Console > Environment > Elasticsearch, set Enable Elasticsearch Indexing to true (new posts are then indexed automatically after saving) and make sure Backend type is elasticsearch. Connection details and the initial index build follow on that page.

## Checked

2026-11-09. Confirmed against the Mattermost Elasticsearch server setup source: dedicated machine advice, v9 or v8, systemd steps, network.host, action.destructive_requires_name, ports 9200 and 9300, the required analysis-icu plugin on every node with rolling restart, the CJK plugins and EnableCJKAnalyzers, and the System Console steps. Nothing removed.

Method: docs-checked 2026-11-09 against the mattermost/docs source administration-guide/scale/elasticsearch-setup.rst (whole file).
