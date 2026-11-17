---
id: computing-software.cybersecurity-defensive.zeek.packet-analysis-framework
name: packet-analysis-framework
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, packet-analysis, packet-analyzer, register-packet-analyzer, link-layer]
level: advanced
status: docs-checked
description: "Zeek packet analysis plugins below session analysis: packet flow from IOSource through layered analyzers, register_packet_analyzer mappings, default_analyzer and module naming."
sources: ["https://docs.zeek.org/en/current/frameworks/packet-analysis.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# packet analysis framework

The packet analysis architecture parses headers below session analysis, so new link and network layer protocols can be added.

Flow: an IOSource (by default libpcap, reading pcap files or sniffing an interface) acquires packets, which are processed layer by layer. Each analyzer parses its header, picks the analyzer for the encapsulated protocol using a numeric ID in the header, and passes the payload on. At the IP layer packet analysis ends and Zeek builds a session; after TCP and UDP session analysis, application analyzers take over with Dynamic Protocol Detection.

Configuration example for Ethernet:

```
module PacketAnalyzer::ETHERNET;
export {
    const default_analyzer: PacketAnalyzer::Tag = PacketAnalyzer::ANALYZER_IP &redef;
}
event zeek_init() &priority=20
    {
    PacketAnalyzer::register_packet_analyzer(PacketAnalyzer::ANALYZER_ETHERNET, 0x8864, PacketAnalyzer::ANALYZER_PPPOE);
    }
```

`PacketAnalyzer::register_packet_analyzer(parent, identifier, child)` maps an identifier such as an EtherType to a child analyzer. `default_analyzer` is used when nothing matches. Ethernet adds `snap_analyzer`, `novell_raw_analyzer` and `llc_analyzer` for frame types identified by the first payload bytes.

Conventions: the module is `PacketAnalyzer::<canonical name>` and the fallback is named `default_analyzer`. The root analyzer dispatches by link type, for example `register_packet_analyzer(PacketAnalyzer::ANALYZER_ROOT, DLT_EN10MB, PacketAnalyzer::ANALYZER_ETHERNET)`.

Plugins implement an analyzer by inheriting `zeek::packet_analysis::Analyzer` and overriding `AnalyzePacket()`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
