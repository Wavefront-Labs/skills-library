---
id: computing-software.networking-hardware-and-wireless.asterisk.cdr-fields-dispositions-and-variables
name: cdr-fields-dispositions-and-variables
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, cdr, cdr-function, disposition, billsec, duration, userfield, accountcode, cdr-custom]
level: practitioner
status: docs-checked
description: "Read and set CDR fields with the CDR function, know standard fields (src, dst, billsec, disposition, linkedid), dispositions, and custom CDR variables for cdr_custom."
sources:
  - https://docs.asterisk.org/Configuration/Reporting/Call-Detail-Records-CDR/CDR-Specification/
  - https://docs.asterisk.org/Configuration/Reporting/Call-Detail-Records-CDR/CDR-Variables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDR fields, dispositions and variables
Access fields with `${CDR(field)}`; read/write fields can be changed with `Set(CDR(field)=value)` until the CDR is finalized.

Times: `start` (CDR created), `answer`, `end`. `duration` = end minus start; `billsec` = end minus answer (whether to bill it is up to you).

Standard fields: `accountcode` (r/w), `src` (caller ID number), `dst`, `dcontext`, `clid`, `channel`, `dstchannel`, `lastapp`, `lastdata`, `start`, `answer`, `end`, `duration`, `billsec`, `disposition`, `amaflags` (r/w), `userfield` (r/w, 255 chars; if set on both parties they are joined with `;`), `uniqueid`, `linkedid`, `peeraccount` (r/w), `sequence` (with uniqueid and linkedid identifies one record).

Dispositions (Party A's view): `NO ANSWER` (default for unanswered), `CONGESTION`, `FAILED`, `BUSY`, `ANSWERED` (once answered, hangup cause no longer changes it). The `congestion` setting in `cdr.conf` can map congestion to FAILED.

Custom variables: `Set(CDR(name)=value)`. Output them to a text-format CDR with the `cdr_custom` driver, as shown in `cdr_custom.conf.sample`.

## Checked
2026-11-04: read the cited Asterisk documentation pages (CDR-Specification, CDR-Variables) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
