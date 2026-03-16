console.log("AI Dictionary content script loaded");

chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
  if (request.action === "getSelection") {
    const selectedText = window.getSelection()?.toString().trim() ?? "";
    sendResponse({ selectedText });
  }
});
