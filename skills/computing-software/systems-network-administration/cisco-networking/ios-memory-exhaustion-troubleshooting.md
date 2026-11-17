---
id: computing-software.systems-network-administration.cisco-networking.ios-memory-exhaustion-troubleshooting
name: ios-memory-exhaustion-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, memory-leak, memory-exhaustion, show-memory, malloc-fail, process-memory, show-processes-memory]
level: practitioner
status: draft
description: "Find IOS/IOS XE memory leaks and exhaustion: free memory trends, per-process holders, MALLOCFAIL messages, IOSd vs Linux memory, and what to give TAC."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-software-releases-121-mainline/6507-mallocfail.html
  - https://www.cisco.com/c/en/us/support/docs/routers/asr-1000-series-aggregation-services-routers/116777-technote-product-00.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Memory exhaustion troubleshooting

## Symptoms
- `%SYS-2-MALLOCFAIL: Memory allocation of N bytes failed from 0x..., alignment 0, pool Processor`
- `%PLATFORM-4-ELEMENT_WARNING: ... Used Memory value 92% exceeds warning level 90%`
- New SSH sessions fail, BGP drops, `show` commands refuse to run, eventually a crash/reload.

## Classic IOS
```
show memory statistics                  ! Processor and I/O pools: Total, Used, Free, Lowest, Largest
show processes memory sorted            ! Holding column per process
show processes memory sorted holding | exclude 0 0 0
show memory dead                        ! memory held by dead processes
```
Take samples hours apart. A process whose **Holding** grows steadily without load change = leak.
"Largest" free block much smaller than "Free" = fragmentation.

## IOS XE (Linux-based)
Two layers: IOSd process heap and Linux/QFP memory.
```
show platform resources                         ! control-plane memory and CPU health
show platform software status control-processor brief
show processes memory platform sorted           ! Linux processes (smd, fman, iosd...)
show memory platform
show processes memory sorted                    ! inside IOSd
show platform software memory iosd switch active R0 brief
show platform hardware qfp active infrastructure exmem statistics   ! ASR/ISR data plane memory
```

## Common causes
- Known bug (check release notes, Bug Search by the leaking process name).
- Huge tables: full BGP table on a router sized for defaults, NetFlow cache sizing, ARP/MAC storms.
- Many SSH/automation sessions not closing (`show users`, `show tcp brief`).
- Debugs left running into the buffer; big `logging buffered`.
- Embedded packet capture buffers left allocated.

## Actions
1. Capture evidence before reload: the commands above, `show tech-support memory`, `show logging`.
2. Mitigate: clear the offending feature (e.g. reduce NetFlow cache, `clear ip bgp` soft), kill stuck VTYs (`clear line`).
3. Plan a reload in a window; upgrade to a fixed release.
4. Monitor free memory via SNMP (CISCO-MEMORY-POOL-MIB / CISCO-PROCESS-MIB) with a trend alert.

## Verify
- [ ] Post-fix samples show stable Holding for the suspect process over 24-72 h.
