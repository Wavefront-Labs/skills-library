---
id: computing-software.software-engineering.perl.yaml-xml-csv-parsing
name: yaml-xml-csv-parsing
category: computing-software
field: software-engineering
product: perl
tags: [perl, yaml-pp, xml-libxml, text-csv, csv-xs, xpath, yaml-xml-csv-parsing]
level: practitioner
status: draft
description: "Parse CSV with Text::CSV, XML with XML::LibXML and XPath, and YAML with YAML::PP; avoid regex parsing of these formats."
sources: ["https://metacpan.org/pod/Text::CSV", "https://metacpan.org/pod/XML::LibXML", "https://metacpan.org/pod/YAML::PP"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# YAML, XML and CSV parsing

**Goal:** use real parsers.

## CSV
```perl
use Text::CSV;                                   # uses Text::CSV_XS when installed (faster)
my $csv = Text::CSV->new({ binary => 1, auto_diag => 1, sep_char => ',' });
open(my $fh, '<:encoding(UTF-8)', $file) or die $!;
my @hdr = @{ $csv->getline($fh) }; $csv->column_names(@hdr);
while (my $row = $csv->getline_hr($fh)) { print $row->{name} }
$csv->eof or $csv->error_diag;
$csv->say($out_fh, \@fields);                    # writes a quoted record
```
`binary => 1` is needed for embedded newlines and non-ASCII. Never `split /,/` quoted CSV.

## XML
```perl
use XML::LibXML;
my $doc = XML::LibXML->load_xml(location => $file);          # or string => $xml
for my $n ($doc->findnodes('//item[@type="a"]')) { say $n->findvalue('./name'), ' ', $n->getAttribute('id') }
my $xpc = XML::LibXML::XPathContext->new($doc);
$xpc->registerNs(a => 'http://example.com/ns'); my @n = $xpc->findnodes('//a:item');
my $new = $doc->createElement('x'); $doc->documentElement->appendChild($new); print $doc->toString(1);
```
Untrusted XML: disable entity expansion and network access (`load_ext_dtd => 0, expand_entities => 0, no_network => 1`) to prevent XXE; check the XML::LibXML docs for current defaults.

## YAML
```perl
use YAML::PP; my $yp = YAML::PP->new; my $cfg = $yp->load_file('config.yaml'); $yp->dump_file('out.yaml', $cfg);
```
Alternatives: YAML::XS (libyaml binding, faster), YAML::Tiny (simple subset). Do not load untrusted YAML with a loader that instantiates objects (`YAML::Load` in old YAML.pm blessed objects); prefer safe options in YAML::PP/YAML::XS (`$YAML::XS::LoadBlessed = 0`).

## Failure modes
- CSV files from Excel may start with a BOM: open with `<:encoding(UTF-8)` and strip a leading `\x{FEFF}` from the first header, or use `File::BOM` (CPAN).
- Namespaced XML needs `registerNs`; plain `//item` finds nothing.

## Self-check
- [ ] A quoted field with an embedded comma and newline round-trips through Text::CSV.
