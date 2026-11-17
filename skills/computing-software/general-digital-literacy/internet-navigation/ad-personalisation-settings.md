---
id: computing-software.general-digital-literacy.internet-navigation.ad-personalisation-settings
name: ad-personalisation-settings
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, in-privacy, ad-personalisation, targeted-ads, ad-settings, advertising-id]
level: intro
status: docs-checked
description: "Turn off or tune personalised ads in Google My Ad Center, Meta, Apple, Microsoft and Amazon, reset the phone advertising ID, and understand what still gets collected."
sources:
  - https://myadcenter.google.com/
  - https://support.google.com/My-Ad-Center-Help/answer/12156161
  - https://support.apple.com/en-us/105131
  - https://support.apple.com/en-us/102420
  - https://support.google.com/chrome/answer/13355898
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ad personalisation settings

Turning off personalisation doesn't remove ads; you get generic ones, and less of your activity is used to target you.

## Accounts
- **Google:** myadcenter.google.com › **Personalised ads** Off, (this deletes your saved topic and brand preferences and also turns off personalisation on partner sites and apps), or keep it on and customise. The option can be missing if the account shows the user is under 18. Other ad networks are not affected.
- **Meta, Microsoft, Amazon, X, TikTok, LinkedIn:** each has ad preferences in its own account privacy or ads settings; use that service's help centre for the current menu path.

## Phones
- **iPhone:** apps must ask before tracking you. Settings › Privacy & Security › **Tracking** › *Allow Apps to Request to Track* off (each app that asks is then treated as if you tapped Ask App Not to Track). Settings › Privacy & Security › **Apple Advertising** › Personalized Ads off; Apple says this covers only the App Store, Apple News and Stocks, and may not reduce how many ads you see.
- **Android:** Settings › Google › All services › Ads (older versions: Settings › Privacy › Ads) › **Reset** or **Delete advertising ID**. Delete removes the ID without assigning a new one; apps can still show ads.

## Browser
- Chrome: More › Settings › Privacy and security › **Ad privacy** (Ad topics, Site-suggested ads, Ad measurement). Blocking a topic or site does not stop related ads entirely. Managed devices may have these locked by an administrator.

## Gotchas
- Google and Apple settings are per account; repeat for each profile and family member. Signed-out Google ad settings are saved to the browser or device.
- Ads based on the page you're reading (contextual) and on location continue.

## Verify
- [ ] Each account's ad settings show personalisation off or limited; iPhone Tracking request toggle off.

## Checked

Checked 2026-10-27 against Google My Ad Center Help (12156161), Apple Support 105131 and 102420, Chrome Help 13355898 and Android Help ad settings. Confirmed: My Ad Center off deletes preferences and covers partner sites, Apple Advertising covers only App Store, News and Stocks, Tracking toggle behaviour, Chrome Ad privacy path, Android advertising ID reset and delete paths.

Method: documentation only; no commands were run.
