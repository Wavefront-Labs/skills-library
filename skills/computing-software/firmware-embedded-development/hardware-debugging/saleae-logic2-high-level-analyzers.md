---
id: computing-software.firmware-embedded-development.hardware-debugging.saleae-logic2-high-level-analyzers
name: saleae-logic2-high-level-analyzers
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [saleae-hla, saleae, logic2, high-level-analyzer, protocol-decoding, logic2-automation, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write Saleae Logic 2 High Level Analyzers in Python on top of another analyzer's frames, and know what the logic2-automation interface offers."
sources:
  - https://support.saleae.com/saleae-api-and-sdk/extensions/high-level-analyzer-extensions
  - https://support.saleae.com/saleae-api-and-sdk/extensions/api-documentation
  - https://saleae.github.io/logic2-automation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saleae Logic 2 High Level Analyzers (HLA)

An HLA is a Python class that consumes the frames of another analyzer (for example Async Serial)
and emits your own frames, shown as a row in the capture.

## Files
A new HLA extension folder holds `README.md` (shown in Logic 2 and on the Marketplace),
`extension.json` (required in the extension root; lists the HLAs and measurement scripts) and
`HighLevelAnalyzer.py`. If your class is not named `Hla` (the default), the class name must be
referenced in the json file.

## Skeleton
```python
from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting

class MyHla(HighLevelAnalyzer):
    search_for = StringSetting()          # shown in the Logic 2 settings UI
    result_types = {'match': {'format': 'Found: {{data.char}}'}}

    def __init__(self):
        pass                              # settings are available as attributes here

    def decode(self, frame: AnalyzerFrame):
        try:
            ch = frame.data['data'].decode('ascii')
        except Exception:
            return                        # not an ASCII character
        if ch in self.search_for:
            return AnalyzerFrame('match', frame.start_time, frame.end_time, {'char': ch})
```
- Subclass `HighLevelAnalyzer` and implement `decode()`; it is called for every frame from the
  input analyzer and returns None, one `AnalyzerFrame` or a list of them.
- `AnalyzerFrame(type, start_time, end_time, data)` carries a type string, GraphTime start and end
  and a data dict. Output times can span a different range, for example to fill the gaps
  between matches with a 'nomatch' frame.
- Setting classes: `StringSetting`, `NumberSetting(min_value, max_value)`, `ChoicesSetting(choices)`.
- `result_types` maps each output frame type to a `format` string using `{{type}}` and
  `{{data.field}}` placeholders; add an entry for every type you emit.
- Async Serial emits one frame type, `data`, with fields `data` (a bytes object), `error` and
  `address`. Check Saleae's Analyzer Frame Types page for any other analyzer before relying on its
  fields.

## Debugging
There is no debugger attach for Python extensions. Use `print()` (goes to the in-app terminal),
the wall clock format and timing markers to find the frame named in an error, and the reload source
button or menu item (Reload Source Files) to re-run after editing.

## Automation interface
The Logic 2 Automation Interface is a gRPC API (the proto is published, so other languages can use it
directly); the Python library `saleae.automation` wraps it. Its documented classes include Manager,
LogicDeviceConfiguration, CaptureConfiguration, ManualCaptureMode, TimedCaptureMode,
DigitalTriggerCaptureMode, GlitchFilterEntry and DataTableExportConfiguration. It needs Logic 2
launched with the socket interface enabled: follow the "Launching the Logic 2 Software and Starting
the Socket Interface" section of the automation docs for the flags and port, and the Getting Started
section for installing the package.

## Verify
- [ ] HLA rows line up with the underlying frames and your firmware logs.
- [ ] After editing, reloading the source reproduces the expected rows.

## Checked
Confirmed from the Saleae HLA guide: file layout, imports, setting classes, result_types format,
decode contract, Async Serial frame fields, debugging tips and the reload action; from the API
documentation page: AnalyzerFrame signature and setting classes; from the automation docs index:
the class list, gRPC basis and section names. Removed as unconfirmed: the I2C and SPI frame type
lists and the register-decoding example, the port 10430 number, the Manager.connect, start_capture,
add_analyzer and export_data_table call shapes, and the claim about HLAs via automation.

Method: docs-checked 2026-11-09 against the Saleae HLA extension guide, the Saleae API documentation page and the logic2-automation documentation index, all read in full.
