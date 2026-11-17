---
id: computing-software.software-engineering.python.safe-xml-parsing-with-elementtree
name: safe-xml-parsing-with-elementtree
category: computing-software
field: software-engineering
product: python
tags: [python, py-data-formats, xml-etree-safe-parsing, elementtree, xml-security, billion-laughs, iterparse, xpath]
level: practitioner
status: docs-checked
description: "Parse and query XML with xml.etree.ElementTree, keep memory low with iterparse, and know the entity-expansion and Expat limits that apply to untrusted XML."
sources: ["https://docs.python.org/3/library/xml.etree.elementtree.html", "https://docs.python.org/3/library/xml.html#xml-vulnerabilities"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe XML parsing with ElementTree

```python
import xml.etree.ElementTree as ET

root = ET.fromstring(xml_text)                       # or ET.parse(path).getroot()
ns = {"a": "http://www.w3.org/2005/Atom"}
for entry in root.findall("a:entry", ns):            # limited XPath subset
    title = entry.findtext("a:title", default="", namespaces=ns)
    link = entry.find("a:link", ns).get("href")
root.find(".//item[@id='7']")                        # predicates on attributes

# Memory-flat streaming of a huge file
for event, elem in ET.iterparse("big.xml", events=("end",)):
    if elem.tag == "record":
        handle(elem)
        elem.clear()                                  # empties the element; it stays in the tree until the document ends

# Build and write
el = ET.Element("user", id="1"); ET.SubElement(el, "name").text = "Ada"
ET.indent(el); ET.ElementTree(el).write("u.xml", encoding="utf-8", xml_declaration=True)
```

## Security (untrusted XML)
The ElementTree docs point untrusted or unauthenticated data to the "XML security" section of the `xml` docs, which says:
- Python's built-in parsers rely on Expat. By default Expat itself does not access local files or create network connections.
- **Billion laughs / quadratic blowup** (entity expansion) and **large tokens** attacks: Expat versions lower than 2.7.2 may be vulnerable to billion laughs, quadratic blowup and large tokens, or to disproportionate memory use. Python bundles Expat, but may use a system Expat depending on how it was configured; check `pyexpat.EXPAT_VERSION`.
- **Decompression bombs** apply to any library parsing compressed XML streams (gzipped HTTP, LZMA files); `xmlrpc` is vulnerable.
- The pages name no third-party hardening library, so cap input size and decompressed size yourself before parsing.

## Gotchas
- Namespaces appear as `{uri}tag` in `.tag`; use the `namespaces` dict with prefixes in `find*`.
- `ET.tostring()` returns bytes (US-ASCII by default) unless `encoding="unicode"`.
- `Element.findtext(match, default=None, namespaces=None)` returns the first match's text; pass `default=""` to get a string when nothing matches.
- An element with no subelements tests as `False` (and testing truth emits `DeprecationWarning` since 3.12); use `elem is not None` or `len(elem)`.
- Comments are preserved only with a `TreeBuilder(insert_comments=True)` (new in 3.8).
- The `[@attrib='value']` predicate cannot contain quotes in the value.
- `iterparse` builds the tree incrementally but does not free it incrementally: clear processed elements, or remove processed children from a parent, as the docs show.

## Verify
- [ ] `pyexpat.EXPAT_VERSION` is 2.7.2 or newer on the deployed interpreter.
- [ ] Peak memory of the `iterparse` loop stays flat on a very large file.

## Checked

- 2026-11-03: checked against the CPython docs `library/xml.etree.elementtree.rst` (iterparse memory guidance, `indent` 3.9, `tostring`, `findtext`, `TreeBuilder` insert_comments 3.8, attribute predicates, truth-value caution) and `library/xml.rst` (XML security section: Expat versions, billion laughs, quadratic blowup, decompression bomb, large tokens).
- Removed: defusedxml and lxml advice and exception names, the Expat 2.4.1 claim, the xml.sax/minidom external-entity claim, the "escaped automatically" comment.

Method: documentation only; no commands were run.
