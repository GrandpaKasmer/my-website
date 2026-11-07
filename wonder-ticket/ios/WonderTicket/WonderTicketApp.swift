import SwiftUI

@main
struct WonderTicketApp: App {
    var body: some Scene {
        WindowGroup {
            ArcadeWebView()
                .ignoresSafeArea()
                .preferredColorScheme(.dark)
        }
    }
}
