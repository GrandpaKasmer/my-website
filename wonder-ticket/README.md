# The Wonder Ticket
### By Grandpa Kasmer · version 0.1.0

A small, self-contained reflection arcade. Choose a door, a feeling, and a charm; pull the lever; keep a ticket and try a ten-minute adventure.

**This is scripted entertainment and reflection, not AI inference, a forecast, or professional advice.** Four doors × four feelings × four charms produce 64 combinations of authored passages. There is no accuracy claim or secret personal-data lookup. The name is a working title; trademark and store-name availability have not been cleared.

## Start here

Use Node.js 22 or newer. No npm dependencies, package installation, API keys, database, login, or paid services are needed to run the project.

```sh
npm run dev
```

Open http://localhost:4173. Stop the server with Control-C.

```sh
npm test            # 12 automated tests
npm run build       # build deployable dist/ with generated icons
npm run preview     # serve an existing dist/
npm run ios:sync    # build web resources and copy into the native iOS project
npm run ios:open    # open the project on a Mac with Xcode installed
```

The downloadable release includes prebuilt `dist/`, native bundled web files, and app icons. The source repository omits generated files: run `npm run ios:sync` after cloning before opening Xcode.

## Included

- Mobile-first, keyboard-accessible choice flow and animated ticket reveal.
- Ticket text sharing/copy fallback and generated PNG export.
- Explicitly saved tickets, up to 20, kept on the device/browser, with deletion.
- Optional sound, reduced-motion support, and clear entertainment labeling.
- Web app manifest and versioned offline cache implementation.
- Bundled SwiftUI/WKWebView iPhone/iPad project with share sheet and light haptics.
- Privacy and terms pages describing this implementation.

No accounts, analytics SDKs, ads, checkout, push notifications, or backend. Web hosting can still generate ordinary access logs. Saved tickets are not a secure vault and do not sync between devices. Native and browser storage behavior must be verified on real devices before inviting testers.

## Repository layout

```text
web/                         editable self-contained app + web resources
scripts/                     dependency-free build and local server
 tests/                      Node logic tests and optional Playwright tests
 ios/WonderTicket.xcodeproj/  native Xcode project
 ios/WonderTicket/            native source, assets, bundled web output
 docs/                       deployment, TestFlight, test results, session handoff
 dist/                       generated web deployment output
```

The website source is intentionally one HTML file with inline CSS/JavaScript so it is easy to inspect, move, and preview without a build framework. The build generates original PNG icons using Node built-ins; it downloads no assets. The iOS app runs the same bundled experience, not a remote website.

## Status and next actions

Read `docs/TEST_RESULTS.md` for exact testing limits. The logic/build tests and in-memory browser interaction checks passed. The iOS sources passed syntax and project-file checks, **not an Apple SDK compilation**. Native signing, device testing, TestFlight upload, and domain deployment remain owner actions.

- Web launch: `docs/DEPLOYMENT.md`
- Xcode/TestFlight: `docs/TESTFLIGHT.md`
- Bounded-session handoff: `docs/SESSION_HANDOFF.md`

Keep this release small. Verify one complete reading on a phone and the website deployment before considering any new features. FixOps and other Kasmer One applications are outside this project's scope.

Copyright © 2026 Kasmer One LLC. All rights reserved. No open-source license is granted by this package.
