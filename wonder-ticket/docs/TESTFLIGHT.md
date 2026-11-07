# Xcode and TestFlight handoff

## Exact status

A native SwiftUI + WKWebView Xcode project is included. It bundles the web app and implements native text/image sharing and light haptics. It has NOT been built against an Apple SDK, signed, archived, uploaded to App Store Connect, or tested on an iPhone in this session. Source syntax and plist/project syntax checks passed; those are not substitutes for an Xcode build.

## On your Mac

1. Install a currently supported Xcode/macOS combination and sign in to your Apple developer account locally. TestFlight distribution requires the appropriate Apple Developer Program membership and account permissions. Never paste signing passwords, certificates, or private keys into chat or commit them to GitHub.
2. From this app directory run:

```sh
npm run ios:sync
npm run ios:open
```

Or open `ios/WonderTicket.xcodeproj` directly after syncing. There are no CocoaPods or third-party Swift packages.

3. Select the WonderTicket app target → Signing & Capabilities. Select YOUR team and keep automatic signing enabled. The proposed bundle ID is `com.grandpakasmer.wonderticket`; check its availability in your account and change it if necessary. No team ID was guessed or embedded.
4. Select an iPhone simulator and build/run. Resolve any current SDK errors before proceeding. Then run on your physical iPhone, and test iPad layout/share-sheet behavior if retaining iPad support.

Current project settings: display name Wonder Ticket; version 0.1.0, build 1; deployment target iOS 16.0; iPhone and iPad. Source uses Swift 5 language mode. These are project settings, not a claim of successful compatibility testing.

## Device acceptance test

- Complete a reading; try back navigation and changing all choices.
- Save a ticket; fully close/reopen the app; confirm it persists; delete it.
- Turn off connectivity and repeat the full reading.
- Share text and image, including cancel and repeated opening; verify image text fits.
- Toggle chime; check mute/audio behavior and haptics.
- Test VoiceOver, larger text, reduced motion, safe areas, and landscape.
- Open privacy and terms and return to the app.
- Verify no unexpected permissions or network requests.

PrivacyInfo.xcprivacy is included for this implementation with no tracking, collected-data, or required-reason API declarations. Review it and App Store privacy answers against the FINAL SDK/build and any future dependencies. Local storage is not a promise that every hosting or Apple diagnostic process collects nothing.

## Upload only after successful device testing

Create the matching app record in App Store Connect with your selected bundle ID. Confirm the display name is available, provide beta description/contact/test instructions, and answer age-rating, privacy, and encryption questions truthfully. The project currently declares no non-exempt encryption because it implements no custom cryptography; confirm this remains appropriate before upload.

In Xcode, select a generic iOS device/archive destination, then Product → Archive. In Organizer choose Distribute App and the App Store Connect/TestFlight upload path offered by the current Xcode version. Validate and upload. After processing, choose the build in App Store Connect → TestFlight, resolve any compliance warnings, and add it to an internal testing group for eligible account users. For external testers, submit the required beta review information and wait for Apple's review where required.

No TestFlight invitation URL exists until Apple has processed the uploaded build and its tester configuration.

## Approval is not promised

Apple's guideline 4.2 requires sufficient app functionality beyond a repackaged website; guideline 4.3(b) specifically treats fortune-telling as a well-established category and requires a meaningfully different or improved experience. Bundling this app and adding native sharing do not guarantee acceptance. Present it accurately as an authored reflection/creative-action experience, not as accurate prediction technology, and do not disguise its functionality to evade review.

TestFlight builds expire, so it is a beta-testing route, not a permanent customer distribution plan. Keep web launch as the small first release while you evaluate native testing.

Official references checked November 7, 2026:
- https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/
- https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/
- https://developer.apple.com/app-store/review/guidelines/
