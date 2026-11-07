import SwiftUI
import WebKit
import UIKit

/// Local, bundled experience. No remote app URL, API keys, account, or analytics.
struct ArcadeWebView: UIViewRepresentable {
    func makeCoordinator() -> Coordinator { Coordinator() }
    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        configuration.websiteDataStore = .default()
        configuration.preferences.javaScriptCanOpenWindowsAutomatically = false
        configuration.userContentController.add(context.coordinator, name: "wonderTicket")
        let view = WKWebView(frame: .zero, configuration: configuration)
        view.navigationDelegate = context.coordinator
        view.isOpaque = false
        view.backgroundColor = UIColor(red: 16/255, green: 39/255, blue: 36/255, alpha: 1)
        view.scrollView.backgroundColor = view.backgroundColor
        view.scrollView.contentInsetAdjustmentBehavior = .never
        context.coordinator.webView = view
        if let folder = Bundle.main.url(forResource: "Web", withExtension: nil),
           let page = Bundle.main.url(forResource: "index", withExtension: "html", subdirectory: "Web") {
            context.coordinator.allowedFolder = folder.standardizedFileURL
            view.loadFileURL(page, allowingReadAccessTo: folder)
        } else {
            view.loadHTMLString("<html><body style='background:#102724;color:#f2ebd9;font:20px -apple-system;padding:30px'><h1>The ticket machine needs its pages.</h1><p>Run npm run ios:sync in the project folder, then rebuild in Xcode.</p></body></html>", baseURL: nil)
        }
        return view
    }
    func updateUIView(_ uiView: WKWebView, context: Context) {}
    static func dismantleUIView(_ uiView: WKWebView, coordinator: Coordinator) {
        uiView.configuration.userContentController.removeScriptMessageHandler(forName: "wonderTicket")
        uiView.navigationDelegate = nil
    }
    final class Coordinator: NSObject, WKScriptMessageHandler, WKNavigationDelegate {
        weak var webView: WKWebView?
        var allowedFolder: URL?
        private func isBundled(_ url: URL) -> Bool {
            guard url.isFileURL, let folder = allowedFolder else { return false }
            return url.standardizedFileURL.path.hasPrefix(folder.path + "/")
        }
        func webView(_ webView: WKWebView, decidePolicyFor action: WKNavigationAction,
                     decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            guard let url = action.request.url else { decisionHandler(.cancel); return }
            if isBundled(url) || url.absoluteString == "about:blank" {
                decisionHandler(.allow)
                return
            }
            // Remote content is never loaded into the privileged local view.
            if action.navigationType == .linkActivated,
               (url.scheme == "mailto" || (url.scheme == "https" && url.host == "grandpakasmer.com")) {
                UIApplication.shared.open(url)
            }
            decisionHandler(.cancel)
        }
        func userContentController(_ controller: WKUserContentController, didReceive message: WKScriptMessage) {
            guard message.name == "wonderTicket", message.frameInfo.isMainFrame,
                  let source = message.frameInfo.request.url, isBundled(source),
                  let body = message.body as? [String: Any], let type = body["type"] as? String else { return }
            switch type {
            case "haptic": UIImpactFeedbackGenerator(style: .light).impactOccurred()
            case "share":
                guard let text = body["text"] as? String, !text.isEmpty, text.utf8.count <= 12_000 else { return }
                presentShare([text])
            case "image":
                guard let encoded = body["data"] as? String,
                      encoded.hasPrefix("data:image/png;base64,"), encoded.utf8.count < 6_000_000,
                      let data = Data(base64Encoded: String(encoded.dropFirst("data:image/png;base64,".count))),
                      let image = UIImage(data: data) else { return }
                presentShare([image])
            default: break
            }
        }
        private func presentShare(_ items: [Any]) {
            DispatchQueue.main.async { [weak self] in
                guard let webView = self?.webView, let root = webView.window?.rootViewController else { return }
                var presenter = root
                while let presented = presenter.presentedViewController { presenter = presented }
                guard !(presenter is UIActivityViewController) else { return }
                let activity = UIActivityViewController(activityItems: items, applicationActivities: nil)
                if let popover = activity.popoverPresentationController {
                    popover.sourceView = webView
                    popover.sourceRect = CGRect(x: webView.bounds.midX, y: webView.bounds.midY, width: 1, height: 1)
                    popover.permittedArrowDirections = []
                }
                presenter.present(activity, animated: true)
            }
        }
    }
}
