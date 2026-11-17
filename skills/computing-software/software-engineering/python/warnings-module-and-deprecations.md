---
id: computing-software.software-engineering.python.warnings-module-and-deprecations
name: warnings-module-and-deprecations
category: computing-software
field: software-engineering
product: python
tags: [python, py-exceptions, warnings-module, deprecationwarning, warnings-filter, stacklevel, pytest-warns]
level: practitioner
status: docs-checked
description: "Emit, filter and test warnings: warnings.warn with stacklevel, category choice, -W flags and filterwarnings, the 3.13 @deprecated decorator and turning warnings into errors in CI."
sources: ["https://docs.python.org/3/library/warnings.html", "https://docs.python.org/3/library/warnings.html#warnings.deprecated"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# warnings module and deprecations

```python
import warnings

def old(x):
    warnings.warn("old() is deprecated, use new()", DeprecationWarning, stacklevel=2)
    return new(x)               # stacklevel=2 attributes the warning to the CALLER

# Python 3.13+: also visible to type checkers
from warnings import deprecated
@deprecated("Use new() instead")
def old2(x): ...
```

## Categories
`DeprecationWarning` (for other Python developers; ignored by default unless triggered by code in `__main__`), `FutureWarning` (for end users of applications), `PendingDeprecationWarning` (ignored by default), `UserWarning` (the default for `warn`), `RuntimeWarning`, `ResourceWarning` (ignored by default). Test runners are advised to show all warnings for the code under test.

## Filtering
```
python -W error::DeprecationWarning script.py      # make them fatal
python -W default script.py                        # show warnings that are ignored by default
PYTHONWARNINGS="error::FutureWarning"
```
In code: `warnings.simplefilter("error")` or `with warnings.catch_warnings(): warnings.simplefilter("ignore", RuntimeWarning); ...`.
A `-W` filter has the form `action:message:category:module:lineno`, e.g. `ignore::DeprecationWarning:somemodule`.

## Testing
```python
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    old(1)
assert w[0].category is DeprecationWarning
```
The docs show `catch_warnings(record=True)` for testing; a test framework may offer its own helper.

## Gotchas
- Without `stacklevel=2` the warning points at your library and users cannot find their call site.
- The `"default"` action prints the first occurrence for each (message, category, module, lineno); tests that expect repeats need `simplefilter("always")`.
- `catch_warnings` modifies global state and is not concurrency-safe unless `-X context_aware_warnings=1` (3.14+, defaults to on for free-threaded builds, off otherwise).
- The docs address application developers for blanket filters (`if not sys.warnoptions: warnings.simplefilter("ignore")`); a library changing global filters affects its users.

## Verify
- [ ] CI runs the test suite with `-W error` so deprecations are noticed before upgrades.
- [ ] Your own deprecation has a test that checks the warning and a removal version in the message.

## Checked

- 2026-11-03: checked against the CPython docs `library/warnings.rst` and `using/cmdline.rst`: category table and default filters, `warn(stacklevel)`, `-W` forms, `catch_warnings(record=True)`, `deprecated` decorator (3.13), `context_aware_warnings` flag (3.14).
- Removed: pytest.warns and pytest.ini filterwarnings (third party, not in these docs) and `-X dev` as a way to show ResourceWarning.

Method: documentation only; no commands were run.
