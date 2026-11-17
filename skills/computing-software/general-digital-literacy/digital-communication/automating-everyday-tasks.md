---
id: computing-software.general-digital-literacy.digital-communication.automating-everyday-tasks
name: automating-everyday-tasks
category: computing-software
field: general-digital-literacy
product: digital-communication
tags: [digital-communication, dc-content-creation, power-automate, apple-shortcuts, automation]
level: intro
status: draft
description: "Automate repetitive tasks with Apple Shortcuts, Power Automate, IFTTT or Zapier: save attachments, send reminders, resize photos, trigger by time or place."
sources:
  - https://support.apple.com/guide/shortcuts/welcome/ios
  - https://learn.microsoft.com/en-us/power-automate/
  - https://help.ifttt.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Automate everyday tasks

## Apple Shortcuts (iPhone, iPad, Mac)
- **Shortcuts** app > + : chain actions (e.g. *Get latest photos > Resize > Save to Files*). Gallery has ready-made ones.
- **Automation** tab: trigger by time, arriving/leaving a place, connecting CarPlay, opening an app, low battery, NFC tag. Example: when I leave work, text home "On my way" with ETA.
- Run from Siri, the Home Screen, the Action button, or the share sheet.

## Microsoft Power Automate
- **Power Automate** (cloud, make.powerautomate.com) with Microsoft 365: templates like *Save Outlook attachments to OneDrive*, *Get a Teams notification when a file is added*, approvals.
- **Power Automate Desktop** (free on Windows 11): records clicks and keystrokes to automate desktop apps and files (rename, move, fill forms).

## Other options
- **Google Home/Assistant routines**: "Good morning" reads calendar and weather, turns on lights.
- **IFTTT** and **Zapier**: connect web services (new form response > add row to Google Sheet > email me). Free tiers are limited.
- Built-in rules: email rules/filters, calendar recurring tasks, phone Focus schedules.

## Doing it well
- Automate something you do weekly that has clear steps; start small and test with sample data.
- Name automations clearly and note what they do; check run history for failures.
- Be careful with automations that send messages, delete files or move money; add a confirmation step.
- Automations connected to accounts hold access tokens; remove ones you no longer use (account > connected apps).

## Verify
- [ ] The automation runs from its trigger, its history shows success, and the result is correct.
