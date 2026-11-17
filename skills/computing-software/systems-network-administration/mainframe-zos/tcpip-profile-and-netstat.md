---
id: computing-software.systems-network-administration.mainframe-zos.tcpip-profile-and-netstat
name: tcpip-profile-and-netstat
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, tcpip-profile, netstat, ports-reserved, tcpip-zos, vtam, netstat-zos, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Network setup"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TCP/IP profile and NETSTAT

Goal: configure and diagnose z/OS networking.
- The TCPIP profile defines devices, home addresses, ports (`PORT 22 TCP SSHD`), and routing (VIPA for stability).
- `NETSTAT CONN`, `NETSTAT DEVLINKS`, `NETSTAT GATE`, `PING`, `TRACERTE` via TSO/Omvs.
- Dynamic VIPA with sysplex distribution for HA.
Verify: connections shown in ESTABLISHED to correct ports.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
