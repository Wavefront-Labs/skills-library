---
id: computing-software.data-science-and-analytics.jupyter-notebooks.ipython-line-cell-magics
name: ipython-line-cell-magics
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [ipython-magics, timeit-magic, jn-magics-productivity]
level: practitioner
status: docs-checked
description: "Use %time, %timeit, %run, %pip, %env and %matplotlib line and cell magics to time code, install packages and set the plotting backend inside the notebook."
sources:
  - https://ipython.readthedocs.io/en/stable/interactive/magics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Magics
```python
%timeit -n 100 -r 5 f(x)      # line mode: time one statement
%time sum(range(n))           # CPU and wall time, returns the value
%pip install pkg              # runs pip within the current kernel
%env VAR=value                # set an environment variable
%matplotlib inline            # activate a plotting backend; %matplotlib --list shows options
%who_ls int                   # names of variables, optionally filtered by type
%run -m example               # run a module instead of a script path
%load_ext name                # load an IPython extension
```
Cell mode (first line of the cell):
```python
%%timeit -r 5 setup_code
body_to_time
```
## Gotchas
- `%timeit` default repeats R is 7; without `-n`, N is chosen automatically for accuracy. Time is the average of the repeats.
- In `%%timeit` cell mode the first-line statement is setup (run, not timed) and the cell body is timed; the body can use variables from the setup.
- `%time` is also a cell magic; there, a statement directly after the magic line raises an error. On Windows system time is always reported as 0. It is "very basic"; use `%timeit` for more control.
- `%time` reports Python compile time when it exceeds 0.1 s.
- Magics are IPython-only; code moved to a plain script must drop them.
## Verify
- [ ] Timing cell reports the expected repeats and loops for the options given.

## Checked

2026-11-09. Confirmed against the IPython built-in magics page (searched by magic name and options): %time line and cell modes, %timeit usage and options, %pip, %env, %matplotlib, %who_ls, %run -m, %load_ext. Removed: %autoreload and the autoreload gotcha and Verify item (not on this page), tag autoreload-magic; `%%time` as the first line of a cell now shown only through the confirmed cell-mode description.
Method: docs-checked 2026-11-09 against the IPython built-in magics page.
