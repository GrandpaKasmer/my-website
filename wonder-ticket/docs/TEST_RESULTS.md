# Verification report — November 7, 2026

## Passed

- `npm test`: all 12 Node tests passed. Coverage includes all 64 combinations, deterministic ticket creation, invalid input/date rejection, schema validation, escaping, corrupt/unavailable storage handling, explicit saving/deduplication/20-ticket limit, deletion, disclaimer inclusion, script syntax, and no remote script dependency.
- `npm run ios:sync`: dependency-free production build and native resource/icon generation succeeded.
- `python tests/sandbox_checks.py`: Chromium in-memory rendering checks passed at 1440, 768, 390, and 320 CSS pixels. Tested choice flow, back navigation, disabled controls, ticket reveal, save/reopen/deduplicate/delete using a test storage adapter, canvas PNG export, manual text-copy fallback, escaped malicious saved text, and no horizontal overflow or page errors.
- Swift source syntax-only parse: `swiftc -frontend -parse ios/WonderTicket/WonderTicketApp.swift ios/WonderTicket/ArcadeWebView.swift` passed.
- `plutil -lint` passed for project.pbxproj, Info.plist, and PrivacyInfo.xcprivacy.
- Desktop and narrow phone screenshots were visually inspected. An initial narrow-screen horizontal overflow was corrected and the interaction checks rerun.

## Environment limits — NOT verified

The container's Chromium policy blocks navigation to HTTP and file URLs, including localhost. `tests/browser_checks.py` could therefore not complete a real-origin test. The in-memory suite uses a test storage adapter and does not validate persistent browser storage, service workers, cache installation, HTTPS, or offline reload. These still require normal browser tests on the deployed site or the owner's Mac. Browser share sheets and actual clipboard permission behavior also need device testing.

No Apple SDK, signing identity, or Apple account was available here. Swift parsing is not type-checking or compiling with SwiftUI/WebKit/UIKit. The Xcode project, native sharing/haptics, bundled offline operation, iOS storage, safe areas, and App Store/TestFlight eligibility need a real Mac/device check.

No GitHub Actions CI run, live hosted deployment, DNS verification, payment test, accessibility certification, security audit, or real-user validation is claimed.

## Reproducing tests

```sh
npm test
npm run ios:sync
```

The optional browser tests require Python and Playwright/Chromium installed separately. They are development checks, not app runtime dependencies. The regular browser suite expects the local server at port 4173. The sandbox suite uses in-memory rendering for restricted environments and should not be mistaken for end-to-end hosting validation.

For owner acceptance steps see DEPLOYMENT.md and TESTFLIGHT.md.
