---
id: computing-software.ai-ml-engineering.feature-engineering.calendar-and-holiday-features
name: calendar-and-holiday-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, time-series, holiday-features, calendar-features, holidays-library, event-windows, known-future-covariates]
level: practitioner
status: gated
description: "Build calendar and holiday features for forecasting and demand models: country/region holiday calendars, distance-to-holiday windows, moving holidays, bridges and business events."
sources:
  - https://holidays.readthedocs.io/en/latest/
  - https://facebook.github.io/prophet/docs/seasonality,_holiday_effects,_and_regressors.html
  - https://otexts.com/fpp3/useful-predictors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calendar and holiday features

**Goal:** explain demand spikes and dips tied to the calendar so the model doesn't mistake them for noise or trend.

## Holiday calendars
```python
import holidays
cal = holidays.country_holidays("US", subdiv="CA", years=range(2020, 2028))
df["is_holiday"] = df.date.dt.date.isin(cal)   # NOT df.date.isin(cal): datetime64 never matches the date keys, so it is silently all False
df["holiday_name"] = df.date.map(cal.get).fillna("none")
```
- Use the calendar for each entity's location (store region, user country); one global calendar misses regional holidays.
- Moving holidays (Easter, Ramadan, Lunar New Year, Diwali) shift every year; a "same week last year" feature misaligns them - holiday features fix that.

## Window features
Effects start before and last after the day:
```python
hdays = pd.to_datetime(sorted(cal.keys()))
idx = np.searchsorted(hdays.values, df.date.values)
df["days_to_next_holiday"] = (hdays[np.minimum(idx, len(hdays) - 1)] - df.date).dt.days.clip(upper=30)
df["days_since_prev_holiday"] = (df.date - hdays[np.maximum(idx - 1, 0)]).dt.days.clip(upper=30)
```
- Clip to a horizon (e.g. 30 days) so far-away holidays don't act as a trend proxy.
- Bridge days (a Friday between a Thursday holiday and the weekend), school vacation periods, and "first working day after" are often stronger signals than the holiday itself.
- Prophet-style: each named holiday with `lower_window`/`upper_window` gets its own effect (gated: unconfirmed, source is paywalled or blocked).

## Business calendar
Paydays (1st/15th, last Friday), promotions, product launches, sports events, tax deadlines, fiscal period ends, store openings/closures. Keep a maintained events table; these are often the largest unexplained residuals.

## Known future covariates
Calendar features are known in advance, so they are safe at forecast time for any horizon - unlike lag features. Make sure events used as features are scheduled (known before the forecast date), not "recorded after it happened"; an unplanned outage feature leaks the future.

## Verify
- [ ] Residuals around major holidays reduced after adding features.
- [ ] Calendars match entity locations.
- [ ] Every event feature is available at forecast time for the full horizon.
