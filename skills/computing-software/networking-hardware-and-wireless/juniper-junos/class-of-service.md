---
id: computing-software.networking-hardware-and-wireless.juniper-junos.class-of-service
name: class-of-service
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, class-of-service, cos, forwarding-class, scheduler]
level: practitioner
status: draft
description: "Configure Junos CoS classification, forwarding classes, schedulers and rewrite rules."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Class of service basics
Goal: prioritise traffic through the router.

```
set class-of-service forwarding-classes class voice queue-num 5
set class-of-service classifiers dscp CLS forwarding-class voice loss-priority low code-points ef
set class-of-service interfaces xe-0/0/3 unit 0 classifiers dscp CLS
set class-of-service schedulers VOICE-S priority strict-high
set class-of-service schedulers BE-S transmit-rate percent 60
set class-of-service scheduler-maps SM forwarding-class voice scheduler VOICE-S
set class-of-service interfaces xe-0/0/3 scheduler-map SM
set class-of-service rewrite-rules dscp RW forwarding-class voice loss-priority low code-point ef
```

- Pipeline: classify (behaviour aggregate, multifield), queue by forwarding class, schedule (rate, priority, buffer), shape, rewrite.
- Default forwarding classes: best-effort, expedited-forwarding, assured-forwarding, network-control (platform dependent: confirm).

Gotcha: CoS features and queue counts vary a lot between platforms (MX, EX, QFX, SRX). A config valid on one may be rejected or ignored on another; check the platform CoS guide.

Operational tip: classify as close to the edge as possible and trust DSCP only on interfaces you control; remark traffic arriving from untrusted peers with a multifield classifier.

## Verify
- `show interfaces queue xe-0/0/3` shows packets per queue; `show class-of-service interface xe-0/0/3`.
