---
id: computing-software.systems-network-administration.patch-management.waf-ips-virtual-patching
name: waf-ips-virtual-patching
category: computing-software
field: systems-network-administration
product: patch-management
tags: [waf-virtual-patching, mitigation, compensating-controls, waf, ips, emergency-patching]
level: practitioner
status: docs-checked
description: "Use WAF or IPS rules as virtual patches while a real fix is pending: when it fits, the OWASP workflow, writing and testing rules, and tracking the patch."
sources:
  - https://owasp.org/www-community/Virtual_Patching_Best_Practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual patching with WAF or IPS

OWASP defines a virtual patch as a security policy enforcement layer that prevents exploitation of a known vulnerability. It analyses transactions and intercepts attacks in transit, so malicious traffic never reaches the application and the application's source code is unchanged. It is a temporary workaround, not remediation: the real patch still needs to land.

## When it fits
- The vendor fix is not yet released, patch testing and installation is slow, the system is mission-critical and cannot go offline, or the code is legacy, outsourced or too costly to fix.
- The attack has a request pattern the tool can inspect (headers, parameters, uploaded files). The tool needs a robust HTTP parser at least as flexible as the web server, or it can be evaded.
- Tools named by OWASP: an intermediary WAF or IPS, a web server plugin such as ModSecurity, or an application-layer filter such as ESAPI WAF.

## Workflow (OWASP phases)
1. **Preparation** (before an incident): subscribe to vendor alert lists; pre-authorise virtual patches through an expedited path (OWASP suggests treating them like antivirus updates or network IDS signatures); have ModSecurity deployed in advance (embedded or on an Apache reverse proxy, which can protect non-Apache back ends); turn on full audit logging, because common log format does not record POST bodies.
2. **Identification**: proactive (assessments, code review) or reactive (vendor contact, public disclosure, active security incident). Blocking the source IP is a poor fit for web attacks; a virtual patch filters on what is sent.
3. **Analysis**: CVE, impact, affected versions, configuration needed to trigger it, whether proof-of-concept code exists (use it to build and test the rule), and whether a workaround or real patch exists. If a patch exists, run patch management and create the virtual patch at the same time.
4. **Creation**: two goals, in order: no false positives (never block legitimate traffic) and no false negatives (do not miss attacks, even with evasion). Vary the PoC one element at a time to find the conditions an attack needs, then look for a characteristic that never occurs in normal traffic. A positive security (allow-list) rule gives better protection but is manual; negative (deny) rules are quicker but easier to evade. Avoid exploit-specific rules that match only one published exploit string.
5. **Implementation/testing**: test with curl, Wget or a local proxy (Burp, WebScarab), not just a browser; use the ModSecurity SecDebugLog (raise `SecDebugLogLevel`, optionally by source IP) to confirm rule processing.
6. **Recovery/follow-up**: track virtual patches in normal patch management with change tickets so their existence and function are documented.

## Gotchas
- Normalise input before matching (ModSecurity transformation functions, e.g. `t:urlDecodeUni`), and keep operator text consistent with the transform: after `t:lowercase`, a mixed-case pattern never matches.
- Rules that look for keywords like `select` or `union` without word delimiters will match ordinary words.

## Verify
The PoC is blocked and logged, legitimate traffic is unaffected, and the patch ticket stays open until the real fix is applied.

## Checked
2026-11-09. Read in full: OWASP "Virtual Patching Best Practices". Removed (not on the page): NIST SP 800-40r4 mitigation wording and source, the example ModSecurity rule, vendor managed-rule claims, nuclei, expiry dates and 48-hour soak, TLS termination and bypass-path notes, and the Log4Shell example.
Method: documentation only; no commands were run.
