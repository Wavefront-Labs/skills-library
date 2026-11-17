---
id: computing-software.web-development.node-express.xxe-and-insecure-deserialization
name: xxe-and-insecure-deserialization
category: computing-software
field: web-development
product: node-express
tags: [xxe, insecure-deserialization, xml-parsing, yaml-load, pickle, security]
level: practitioner
status: verified
description: "Preventing XML external entity attacks and unsafe deserialization: parser settings in Node/Python/Java/Ruby, XML inside uploads, YAML/pickle/Marshal pitfalls and safe formats."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html
  - https://github.com/tiran/defusedxml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XXE and insecure deserialization

## 1. XXE
```xml
<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]>
<r>&x;</r>
```
A parser that resolves external entities reads local files, makes SSRF requests, or exhausts memory ("billion laughs" nested entities).
Safe settings:
| Stack | Do |
|---|---|
| Node | `fast-xml-parser` (v5.11 throws `External entities are not supported` for a `SYSTEM` entity and does not expand nested internal entities; keep `processEntities` defaults); with `libxmljs2` never pass `noent: true` (not run) |
| Python | `defusedxml.ElementTree.fromstring`; lxml `XMLParser(resolve_entities=False, no_network=True)` (lxml 6.1 resolves a local `file:` entity only with `resolve_entities=True`; its default no longer does, and it caps entity amplification). The stdlib `xml.etree` does not resolve external entities and its expat limits amplification, but `defusedxml` rejects any entity declaration outright (`EntitiesForbidden`) |
| Java | `factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)` |
| Ruby | Nokogiri default is safe; never pass `Nokogiri::XML::ParseOptions::NOENT` / `DTDLOAD` |
| .NET | `DtdProcessing = DtdProcessing.Prohibit` |
XML hides in uploads: SVG, DOCX/XLSX/PPTX (zip of XML), SAML responses, SOAP, RSS imports. Parse them with the same hardened settings.

## 2. Insecure deserialization
Formats that can encode objects/code execute attacker logic on load:
- Python `pickle.loads` (a `__reduce__` returning `(print, (...))` ran on load), `yaml.load` without `SafeLoader` (PyYAML 6 requires a `Loader`; `UnsafeLoader` executed `!!python/object/apply`, `FullLoader` and `safe_load` refused it) -> use JSON or `yaml.safe_load`.
- Ruby `Marshal.load`, `YAML.load` on old Psych -> `YAML.safe_load`, JSON; Rails cookies: `cookies_serializer = :json`.
- Java `ObjectInputStream`, PHP `unserialize` -> avoid on untrusted data; use allowlist filters (`ObjectInputFilter`).
- Node: `node-serialize`/`serialize-to-js` `unserialize` (IIFE RCE); `js-yaml` v3 `load` (v3.15 builds a callable function from `!!js/function`; `safeLoad` and v4 `load` reject it with `unknown tag`); `eval`/`new Function` on JSON-like strings.
Rule: untrusted input only through data-only formats (JSON, protobuf, plain YAML via safe loaders), then validate with a schema (zod, pydantic, JSON Schema).

## 3. Signed is not safe
Signing a serialized blob (cookie, cache entry) protects integrity only while the key stays secret; a leaked `SECRET_KEY_BASE` or Django `SECRET_KEY` with pickle-based sessions = RCE. Prefer JSON serializers even for signed data.

## Verify
- [ ] Uploading the XXE payload (and an SVG with it) returns a parse error, not file contents; Semgrep rules for `pickle.loads`, `yaml.load(`, `Marshal.load` pass.

## Checked
Run on Windows with Python 3.14.0 (lxml 6.1.3, defusedxml, PyYAML 6.0.3) and Node 20.20.2 (fast-xml-parser 5.11.2, node-serialize 0.0.4, js-yaml 3.15.2 and 4.x): a `file:` external entity pointing at a local secret read through lxml with `resolve_entities=True` (and `load_dtd`) but not through the lxml default, `resolve_entities=False`, stdlib ElementTree, defusedxml or fast-xml-parser; billion-laughs rejected by lxml, expat and defusedxml; pickle and PyYAML behaviours above; `node-serialize` `unserialize` executed an IIFE (`_$$ND_FUNC$$_function(){...}()`) with a harmless payload and without the trailing `()` it only created the function. Not run: Java, Ruby, .NET, libxmljs2, SVG, DOCX or SAML uploads, Marshal, PHP, `ObjectInputFilter`, the signed-cookie claim (reasoning only). Python and Node parsers are not OS-specific; `file:` URI syntax differs on Windows (drive-letter paths after `file:///`).
