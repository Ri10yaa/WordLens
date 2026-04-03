const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

async function fetchContextualMeaning(word: string, sentence = "") {
  const response = await fetch(`${BACKEND_URL}/tools/define_contextual`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ word, sentence }),
  });

  if (!response.ok) throw new Error(`Backend error: ${response.status}`);
  return response.json();
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "define-word",
    title: "Define with AI Dictionary",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== "define-word" || !tab?.id) return;

  const selection = info.selectionText?.trim();
  if (!selection) return;

  chrome.tabs.sendMessage(tab.id, { action: "showDialog" });

  try {
    const data = await fetchContextualMeaning(selection, "");

    chrome.tabs.sendMessage(tab.id, {
      action: "displayResult",
      data,
    });
  } catch (error) {
    console.error("Backend error", error);
  }
});

chrome.runtime.onMessage.addListener(async (request, sender) => {
  if (request.action !== "manualSearch" || !sender.tab?.id) return;

  try {
    const data = await fetchContextualMeaning(request.text, "");

    chrome.tabs.sendMessage(sender.tab.id, {
      action: "displayResult",
      data,
    });
  } catch (error) {
    console.error("Manual search failed", error);
  }
});
