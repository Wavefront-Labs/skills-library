---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.stationarity-decomposition
name: stationarity-decomposition
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [stationarity-adf, seasonal-decompose, acf-pacf, st-timeseries]
level: practitioner
status: draft
description: "Inspect trend and seasonality with decomposition, test stationarity with ADF and read ACF and PACF plots."
sources:
  - https://www.statsmodels.org/stable/tsa.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stationarity
```python
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
adfuller(y.dropna())            # p small -> reject unit root
seasonal_decompose(y, period=12, model="additive").plot()
plot_acf(y.diff().dropna())
```
## Gotchas
- ADF null is a unit root (non-stationary); read it the right way round.
- Differencing removes trend; seasonal differencing removes seasonality.
## Verify
- [ ] Differenced series ACF decays quickly.
