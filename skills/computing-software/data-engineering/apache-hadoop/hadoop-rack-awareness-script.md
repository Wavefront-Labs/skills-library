---
id: computing-software.data-engineering.apache-hadoop.hadoop-rack-awareness-script
name: hadoop-rack-awareness-script
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, rack-awareness, topology, net-topology, hdfs]
level: practitioner
status: docs-checked
description: "Configuring Hadoop rack awareness: net.topology.script.file.name, number.args default 100, a DNSToSwitchMapping class, output format, and the /default-rack trap."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/RackAwareness.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rack awareness

Master daemons learn each worker's rack id by invoking either an external script or a Java class named in configuration. Either must follow the `org.apache.hadoop.net.DNSToSwitchMapping` interface, with a one-to-one mapping between input and output.

- `net.topology.node.switch.mapping.impl`: the Java class. An example, `NetworkTopology.java`, ships with Hadoop and can be customised. A class is faster than a script because no external process is forked when a worker registers.
- `net.topology.script.file.name`: path to an external script. Unlike the class, no script ships with Hadoop; the administrator provides it.
- `net.topology.script.number.args`: how many IPs Hadoop passes in ARGV per fork, default 100. Set to 1 and the script is forked for every IP submitted by DataNodes and/or NodeManagers.

If neither the script nor the class is set, every IP maps to `/default-rack`. The page warns this causes trouble for HDFS replication: the default writes one replica off-rack, and there is only one rack.

## Output format

Topology is `/myrack/myhost`, where `/` is the delimiter, `myrack` the rack id and `myhost` the host. With one /24 subnet per rack, `/192.168.100.0/192.168.100.5` is a valid unique mapping.

The page's Python example discards argv[0], masks each IP with 255.255.255.0 using netaddr, prints `/<network address>`, and prints `/rack-unknown` on failure. Its bash example fakes one rack per host on a flat network: `echo $@ | xargs -n 1 | awk -F '.' '{print "/rack-"$NF}'`, so HDFS can still create an off-rack copy.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (RackAwareness.md in the apache/hadoop repo). Removed a "Verify" step that cited another page not in sources; corrected the claim that neither a script nor class ships (the Java class example does).
