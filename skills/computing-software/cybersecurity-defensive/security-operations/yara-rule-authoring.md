---
id: computing-software.cybersecurity-defensive.security-operations.yara-rule-authoring
name: yara-rule-authoring
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [malware-analysis, yara-rule-authoring, yara, yara-x, hunting-rules, retrohunt, false-positive-testing, pe-module]
level: advanced
status: gated
description: "Write YARA rules that detect malware families without false positives: string choice, conditions, modules, performance and testing against goodware."
sources: ["https://yara.readthedocs.io/en/stable/commandline.html", "https://virustotal.github.io/yara-x/docs/", "https://github.com/Neo23x0/YARA-Style-Guide", "https://github.com/Neo23x0/YARA-Performance-Guidelines"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# YARA rule authoring

**Goal:** rules that find a malware family or tool across files, memory and retrohunts,
survive minor variants, and do not fire on legitimate software.

## Anatomy
```
rule MAL_Loader_Example_Oct26 {
  meta:
    author = "SOC DE"  date = "2026-10-16"  reference = "CASE-123"
    description = "Loader seen in CASE-123, string decryption routine and C2 path"
    hash = "<sha256 of a sample>"
  strings:
    $s1 = "/gate.php?id=" ascii
    $s2 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101" ascii
    $op_decrypt = { 8A 04 0E 34 ?? 88 04 0F 41 3B CA 72 F3 }
    $pdb = "\\Release\\loaderx.pdb" ascii nocase
  condition:
    uint16(0) == 0x5A4D and filesize < 2MB and
    ( ( $op_decrypt and 1 of ($s*) ) or $pdb )
}
```

Checked with the YARA-X engine (python `yara-x` 1.22.0; classic libyara and the `yara` CLI were not available here, so libyara-specific behaviour is gated: unconfirmed). The rule above compiles with no errors; a buffer with `MZ`, the hex bytes and `/gate.php?id=` matches; the hex pattern plus a string matches; the hex pattern alone does not; the `$pdb` string matches case-insensitively when the `MZ` header is present and does not when it is missing.

## Choosing strings
- Prefer things the author must keep: decryption loops (byte patterns with wildcards `??`),
  unique protocol strings, configuration markers, mutex names, misspellings.
- Avoid library code, common API names, compiler strings, and anything a packer would change.
- Use `wide` for UTF-16 strings, `xor` / `base64` modifiers for simple encodings. `xor` and `base64` cannot be combined on one string (YARA-X: `E019 invalid modifier combination`); `wide xor` and `base64wide` are fine.
- Combine weak strings with counts (`3 of ($s*)`) rather than trusting one.

## Conditions and performance
- Start with cheap checks: `uint16(0) == 0x5A4D`, `filesize`, so the scanner skips most files.
- Avoid short atoms (under 4 bytes) and leading wildcards in hex strings; they slow scans a lot.
- Modules: `pe.imphash() == "..."`, `pe.number_of_signatures == 0`, `pe.sections[i].name`, `math.entropy(...)` (all compiled in YARA-X after `import "pe"` / `import "math"`).
- YARA-X (the Rust rewrite) is largely compatible and has `slow_pattern`, `potentially_slow_loop` and `too_many_iterations` warnings (its docs list them; they did not fire on my small examples such as `"ab"` or `{ ?? ?? 41 42 }`, so do not rely on them as a performance proof); test both if you deploy to mixed engines.

## Testing
1. True positives: all known samples of the family match (`yara -r rule.yar samples/`; `-r` is recursive).
2. False positives: run against a goodware corpus (e.g. clean Windows system directory copies,
   common installers) and your own software repository.
3. Retrohunt (VirusTotal or your EDR) over 90 days; review every unexpected hit.
4. Time it: `yara -p 4 -r rule.yar corpus/` (`-p` is the thread count and applies to directory scans) before and after; flag rules that dominate scan time.

## Deployment
EDR custom rules, Velociraptor `Windows.Detection.Yara.Process` (memory; artifact exists in the Velociraptor repo), mail gateway,
`windows.vadyarascan` in Volatility 3 (plugin exists in the repo). Version rules in Git with tests.

## Gotchas
- Rules on unpacked memory strings will not match the packed file on disk; label which form a rule targets.
- `nocase` and many `wide` strings multiply atoms; use only where needed.
- Naming convention (`MAL_`, `HKTL_`, `SUSP_`) helps triage hits.

## Verify
- [ ] 100% of reference samples match, zero hits on the goodware set.
- [ ] Rule compiles in every engine version deployed.
