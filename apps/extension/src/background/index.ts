const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "define-word",
    title: "Define with AI Dictionary",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== "define-word" || !tab?.id) return;

  chrome.tabs.sendMessage(tab.id, { action: "showDialog" });

  try {
    const response = await fetch(`${BACKEND_URL}/define/${info.selectionText}`);
    if (!response.ok) throw new Error(`Backend error: ${response.status}`);
    const data = await response.json();

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
    const response = await fetch(`${BACKEND_URL}/tools/define_contextual`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ word: request.text, sentence: "" }),
    });

    if (!response.ok) throw new Error(`Backend error: ${response.status}`);
    const data = await response.json();

    chrome.tabs.sendMessage(sender.tab.id, {
      action: "displayResult",
      data,
    });
  } catch (error) {
    console.error("Manual search failed", error);
  }
});
