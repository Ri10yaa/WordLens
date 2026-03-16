# Extension QA

1. Build assets: `cd apps/extension && npm install && npm run build`.
2. Load the `dist` directory via `chrome://extensions` → "Load unpacked".
3. Visit any webpage, highlight a word, right-click → "Define with AI Dictionary". A floating dialog should appear with a definition + confidence.
4. Test manual search: click the floating widget, type a word, confirm backend results stream back.
5. Refresh the tab and ensure minimized/visible state persists (stored via `chrome.storage.local`).
