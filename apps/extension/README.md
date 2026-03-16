# Chrome Extension

Always-on Chrome overlay that surfaces context-aware definitions powered by the backend API.

## Scripts

```bash
cd apps/extension
npm install
npm run build
```

Load the generated `dist` directory as an unpacked extension at `chrome://extensions`.

Set `BACKEND_URL` when building to target other environments:

```bash
BACKEND_URL=https://api.example.com npm run build
```

## Manual QA Checklist

- Highlight a word and use the context menu entry; verify floating dialog displays results.
- Open the dialog manually, type a word, and ensure contextual definition + confidence appear.
- Reload pages to confirm dialog state persistence (minimized/visible) across navigations.
