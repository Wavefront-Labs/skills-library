---
id: computing-software.cybersecurity-defensive.application-security.xxe-prevention
name: xxe-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [owasp-top-10, xxe, xml-external-entities, xml-parser-hardening, dtd, billion-laughs, cwe-611]
level: practitioner
status: docs-checked
description: "Prevent XML external entity attacks: disable DTDs and external entities per parser (Java, .NET, Python, PHP, libxml2), find risky parsers in code, and test with safe payloads."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html", "https://cwe.mitre.org/data/definitions/611.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XXE prevention

XML parsers that process DTDs can be made to read local files (`file:///etc/passwd`), make server-side
requests (SSRF), or exhaust memory (billion laughs). Inputs include SOAP, SAML, SVG, DOCX/XLSX (zip of
XML), RSS, and any "upload XML" feature.

## Fix: reject DTDs (best), else block external entities
Per the OWASP cheat sheet: reject DOCTYPE declarations wherever the parser supports it; if DTDs are needed, disable
external entities and external DTD loading and limit entity expansion. Keep XInclude disabled unless required, and
restrict external access during schema validation and style sheet processing too. Treat an unsupported security
setting as a configuration failure; do not carry on parsing untrusted XML with partial hardening.

**Java** (JAXP built-ins, Java 9+; pass streams, not untrusted filenames or URLs):
```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newDefaultInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
DocumentBuilder builder = dbf.newDocumentBuilder();
Document doc = builder.parse(untrustedStream);
```
`setExpandEntityReferences(false)` only changes how entity references appear in the tree; it does not replace
blocking external resources. SAXParserFactory takes the same two features.
StAX (`XMLInputFactory.newDefaultFactory()`): set `XMLInputFactory.SUPPORT_DTD` and
`XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES` to false; StAX does not support `FEATURE_SECURE_PROCESSING`.
TransformerFactory: set `FEATURE_SECURE_PROCESSING` plus `ACCESS_EXTERNAL_DTD` and `ACCESS_EXTERNAL_STYLESHEET`
to `""` before compiling the style sheet.
**.NET**: in .NET Framework 4.5.2 and later `XmlDocument`, `XmlTextReader` and `XPathNavigator` are safe by
default (their `XmlResolver` is null); below 4.5.2 set `XmlResolver = null`. For `XmlReader`/`XmlTextReader`,
`DtdProcessing = DtdProcessing.Prohibit` throws on any DOCTYPE. ASP.NET apps must also set `httpRuntime
targetFramework` to 4.5.2 or later.
**Python**: for untrusted XML use the `defusedxml` parsing interfaces in place of the standard-library ones, and
set `forbid_dtd=True` where offered. They reject prohibited constructs; they do not sanitise XML or cap resources.
**PHP / libxml2** (2.9.0 and later): entity substitution is off by default; never enable `LIBXML_NOENT`,
`LIBXML_DTDLOAD` or `LIBXML_DTDVALID` for untrusted XML without blocking external resources.
**libxml2 (C)**: do not pass `XML_PARSE_NOENT` or `XML_PARSE_DTDLOAD` to `xmlReadMemory`, `xmlReadFile`,
`xmlCtxtReadMemory` and the related read functions.

## Find risky code
- SAST rules (Semgrep XXE rules).
- Grep for parser factories without the settings above; check libraries that parse XML internally
  (SAML libraries, document converters, SVG renderers).

## Test (in test environments)
Send a harmless external entity pointing to a canary URL you control:
```xml
<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY x SYSTEM "http://canary.example.test/xxe">]>
<r>&x;</r>
```
A hit on the canary or an error revealing entity resolution means vulnerable. DAST tools (ZAP, Burp)
include XXE checks.

## Gotchas
- Switching to JSON does not help if a second endpoint still accepts XML (content-type confusion).
- Office documents and SVG uploads are XML parsers in disguise.
- Preventing XXE does not prevent every XML denial-of-service attack; see the OWASP XML Security Cheat Sheet.

## Verify
Unit test that feeds the parser the canary payload and asserts an exception or no network call, for every
parser instantiation point.

## Checked
2026-10-31. Confirmed against the OWASP XML External Entity Prevention Cheat Sheet: Java JAXP settings, StAX
properties, TransformerFactory attributes, .NET 4.5.2 defaults and DtdProcessing, libxml2 2.9 default and the
NOENT/DTDLOAD options, defusedxml and forbid_dtd, Semgrep rules. Removed unconfirmed: lxml parser arguments, the
CodeQL rule id, the setXIncludeAware/legacy feature lines, ".NET Core" default claim, named SVG renderers and the
parameter-entity gotcha. The DOCTYPE canary payload is a test pattern, not a sourced claim.
Method: documentation only; no commands were run.
