---
id: computing-software.firmware-embedded-development.bare-metal-programming.misra-control-flow-rules
name: misra-control-flow-rules
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [misra-control-flow, misra-c, rule-15, switch-statements, single-exit, firmware-embedded-development]
level: advanced
status: draft
description: "Write firmware that satisfies MISRA C:2012 control-flow rules (14.x loops, 15.x goto/single exit/else, 16.x switch) without contorting the code."
sources:
  - https://misra.org.uk/product/misra-c2012-third-edition-first-revision/
  - https://barrgroup.com/embedded-systems/books/embedded-c-coding-standard
  - https://cppcheck.sourceforge.io/misra.php
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control flow rules (Rules 14-16)

## Key rules
| Rule | Cat. | Requirement |
|---|---|---|
| 14.2 | Req | `for` loops well-formed: one loop counter, not modified in the body, no float counter |
| 14.3 | Req | controlling expressions not invariant (except `while (1)`/`for (;;)` per exception for infinite loops) |
| 14.4 | Req | controlling expression essentially Boolean: `if (count != 0U)` not `if (count)` |
| 15.1 | Adv | no `goto` |
| 15.4 | Adv | at most one `break`/`goto` terminating a loop |
| 15.5 | Adv | single point of exit at the end of a function |
| 15.6 | Req | bodies of `if`/`else`/loops/`switch` are compound statements (braces always) |
| 15.7 | Req | `if ... else if` chains end with `else` |
| 16.1-16.7 | Req | switch well-formed: every clause ends in `break`, `default` present and first or last, at least two clauses, no Boolean switch |

## Compliant firmware patterns
```c
/* 14.4: compare explicitly */
while ((USART1->ISR & USART_ISR_TXE) == 0U) { }

/* 15.6/15.7 */
if (state == ST_IDLE) {
    start();
} else if (state == ST_RUN) {
    step();
} else {
    /* no action: state ST_ERROR handled elsewhere */
}

/* 16.x: every case breaks, default last */
switch (cmd) {
    case CMD_START: start(); break;
    case CMD_STOP:  stop();  break;
    default:        err = ERR_BAD_CMD; break;
}
```

## Single exit (15.5, advisory)
Strict single exit makes error handling nested and harder to read. Common resolution in
firmware projects: **adopt 15.5 as advisory and deviate for early-return parameter checks**, or
use the `status` accumulation style:
```c
status_t init(dev_t *d) {
    status_t st = STATUS_OK;
    if (d == NULL) { st = STATUS_EINVAL; }
    if (st == STATUS_OK) { st = clock_on(d); }
    if (st == STATUS_OK) { st = reset_chip(d); }
    return st;
}
```
`goto cleanup` (15.1, advisory) is also commonly deviated in drivers that release resources; MISRA
15.2/15.3 then require jumping forward only and within the same block.

## Fall-through
MISRA forbids switch fall-through (16.3). If behaviour is shared, call a helper or combine labels
(`case A: case B: ...; break;` is allowed: empty clauses may fall through).

## Verify
- [ ] cppcheck MISRA addon (`cppcheck --addon=misra --enable=style src/`) reports no 14.x-16.x findings, or each has a deviation ID.
- [ ] Code review checklist: braces everywhere, explicit comparisons, final `else`, `default` last.
