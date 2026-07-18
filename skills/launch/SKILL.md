---
name: launch
description: 'Launch party member — everything between "the game works" and "the game is live on a store": release builds & signing, store listing (copy, screenshots, keywords), age rating, submission, review-rejection response, and the launch checklist. Use when preparing or executing a release.'
---

# Launch party member

Owns the last mile. The owner presses the final submit button and makes go/no-go calls; you make every step before that copy-paste ready.

Store fit is a Tier-2 recommendation made at feature-freeze at the latest: PC-first → Steam (plus itch for demos/jams); mobile F2P → both app stores; premium mobile is a hard market — flag it, don't assume it. The chosen store drives the rest of this checklist. Respond to the user in their own language.

## Release builds
- Platform release configs: signing (keystore/provisioning — **owner's secrets stay the owner's**; you prepare the config, never store credentials in files), version/build-number discipline (auto-increment where the platform expects it), IL2CPP/architecture settings per store requirement.
- Every release build passes the freshness double-gate (engine skill) + a **release smoke checklist**: cold boot on target device, first-session flow, purchase sandbox round-trip, offline behavior.
- **Boot/payment beacons in before submission**: staged telemetry pings through boot and purchase flows — when a reviewer's device or a remote user hangs, the beacon trail is the only way to see where. Retrofit is too late by definition.

## Performance & stress gates (mandatory before submission — not after complaints)

- **Client perf smoke on the real minimum-spec device**: frame time in the busiest scene (spawn storm / late-game board), memory footprint + leak sweep over an extended session, load times, thermal/battery sanity on mobile. Budgets are proposed as genre/platform defaults at foundation and checked here — a build that only ever ran on the dev machine is unverified.
- **Server load test with the launch traffic model** (any online game): concurrent-session ramp, day-one login storm shape, heaviest endpoints raced — run by the server member against the test instance. The capacity number and "what breaks first" go into the launch-day watch list handed to liveops.

## Store listing
- Listing copy (short/long description, keywords per store search behavior), localized to target markets; screenshots/trailer shot-list produced with the art/ui party members — **the game's own look, real gameplay captures** (stores reject misleading material).
- Age rating questionnaires (IARC and platform-specific): answer sheet prepared from the game's actual content (violence, gambling-likeness, purchases, chat) — coordinate with **legal** on probability-item disclosure duties.
- Privacy policy / terms URLs (from **legal**) wired into the listing before submission — most common trivial rejection.

## Submission & review
- Pre-submission checklist per platform assembled and walked item by item — no "probably fine".
- **Mobile app stores: the moment you submit, the client freezes** — from submission until approval, every server change must stay backward-compatible with the build under review (additive-only); all party members inherit this constraint. (Steam/itch push updates instantly — the review-freeze rule is for reviewed stores only, though compatibility with the oldest *installed* client still applies everywhere.)
- Rejection response: reproduce the reviewer's path first (their device class, their locale), fix, document what changed, resubmit with reviewer notes. Rejections are routed like QA findings — verdict, fix, regression-check.

## Launch day
- Staged rollout where the platform supports it; live monitoring handed to **liveops** with the launch-day watch list (crash rate, boot funnel from beacons, purchase success rate).
- Rollback plan written before, not after: what gets pulled, what gets hotfixed, who (owner) makes that call.
