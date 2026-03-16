import type { ContextualMeaningResponse } from "../../../../packages/shared/ts/context";

type DisplayPayload = ContextualMeaningResponse;

class FloatingDialog {
  private dialog!: HTMLElement;
  private messages!: HTMLElement;
  private loading!: HTMLElement;
  private minimized!: HTMLElement;
  private input!: HTMLInputElement;
  private searchBtn!: HTMLButtonElement;
  private closeBtn!: HTMLButtonElement;
  private minBtn!: HTMLButtonElement;

  constructor() {
    if ((window as any).aiDictInstance) return;

    this.createDialog();
    this.setupEventListeners();
    this.listenForMessages();
    this.restoreVisibilityState();

    (window as any).aiDictInstance = this;
  }

  private createDialog() {
    if (document.getElementById("ai-dict-floating-container")) return;

    const container = document.createElement("div");
    container.id = "ai-dict-floating-container";
    container.innerHTML = `
      <div id="ai-dict-dialog" class="ai-dict-dialog">
        <div class="ai-dict-header">
          <div class="ai-dict-title">AI DICTIONARY</div>
          <div>
            <button id="ai-dict-minimize" class="ai-btn">−</button>
            <button id="ai-dict-close" class="ai-btn">✕</button>
          </div>
        </div>
        <div id="ai-dict-messages" class="ai-messages"></div>
        <div class="ai-input-container">
          <input id="ai-input" type="text" placeholder="Enter word or sentence..." />
          <button id="ai-search" class="ai-btn">SEARCH</button>
        </div>
        <div id="ai-loading" class="ai-loading" style="display:none;">ANALYZING...</div>
      </div>
      <div id="ai-minimized" class="ai-minimized" style="display:none;">DICT</div>
    `;

    const style = document.createElement("style");
    style.innerHTML = `
      .ai-dict-dialog {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 360px;
        background: #050505;
        border: 1px solid #2c2c2c;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        font-family: 'Space Grotesk', Arial, sans-serif;
        z-index: 2147483647;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
      }
      .ai-dict-header {
        display: flex;
        justify-content: space-between;
        padding: 12px 14px;
        border-bottom: 1px solid #1a1a1a;
        color: #f7f7f7;
        letter-spacing: 0.08em;
        font-size: 13px;
      }
      .ai-btn {
        background: transparent;
        border: 1px solid #2f2f2f;
        color: #f7f7f7;
        padding: 4px 8px;
        cursor: pointer;
        border-radius: 4px;
        font-size: 12px;
      }
      .ai-btn:hover {
        background: #f7f7f7;
        color: #050505;
      }
      .ai-messages {
        padding: 14px;
        max-height: 240px;
        overflow-y: auto;
        color: #f7f7f7;
        font-size: 13px;
      }
      .ai-input-container {
        display: flex;
        gap: 8px;
        padding: 12px 14px;
        border-top: 1px solid #1a1a1a;
      }
      #ai-input {
        flex: 1;
        background: #0d0d0d;
        border: 1px solid #2c2c2c;
        color: #f7f7f7;
        padding: 6px 10px;
        border-radius: 4px;
      }
      .ai-loading {
        text-align: center;
        padding: 10px;
        color: #9c9c9c;
        font-size: 12px;
      }
      .ai-minimized {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #f7f7f7, #dcdcdc);
        color: #050505;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        cursor: pointer;
        border-radius: 24px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      }
    `;

    document.head.appendChild(style);
    document.body.appendChild(container);

    this.dialog = document.getElementById("ai-dict-dialog")!;
    this.messages = document.getElementById("ai-dict-messages")!;
    this.loading = document.getElementById("ai-loading")!;
    this.minimized = document.getElementById("ai-minimized")!;
    this.input = document.getElementById("ai-input") as HTMLInputElement;
    this.searchBtn = document.getElementById("ai-search") as HTMLButtonElement;
    this.closeBtn = document.getElementById("ai-dict-close") as HTMLButtonElement;
    this.minBtn = document.getElementById("ai-dict-minimize") as HTMLButtonElement;
  }

  private setupEventListeners() {
    this.searchBtn.addEventListener("click", () => this.manualSearch());
    this.input.addEventListener("keydown", (event) => {
      if (event.key === "Enter") this.manualSearch();
    });
    this.closeBtn.addEventListener("click", () => this.hide());
    this.minBtn.addEventListener("click", () => this.minimize());
    this.minimized.addEventListener("click", () => this.restore());
  }

  private manualSearch() {
    const text = this.input.value.trim();
    if (!text) return;

    this.setLoading(true);
    chrome.runtime.sendMessage({ action: "manualSearch", text });
  }

  private listenForMessages() {
    chrome.runtime.onMessage.addListener((request) => {
      if (request.action === "displayResult") {
        this.displayResult(request.data);
      }
      if (request.action === "showDialog") {
        this.show();
      }
    });
  }

  private displayResult(data: DisplayPayload) {
    this.setLoading(false);
    this.show();

    const div = document.createElement("div");
    const confidence = data.confidence ? `${Math.round(data.confidence * 100)}%` : "—";
    div.innerHTML = `
      <strong>${data.word}</strong><br />
      ${data.definition ?? "No definition available"}<br />
      <small>Confidence: ${confidence}</small>
      <hr />
    `;

    this.messages.appendChild(div);
    this.messages.scrollTop = this.messages.scrollHeight;
  }

  private setLoading(state: boolean) {
    this.loading.style.display = state ? "block" : "none";
  }

  private show() {
    this.dialog.style.display = "flex";
    this.minimized.style.display = "none";
    chrome.storage.local.set({ visible: true, minimized: false });
  }

  private hide() {
    this.dialog.style.display = "none";
    this.minimized.style.display = "none";
    chrome.storage.local.set({ visible: false });
  }

  private minimize() {
    this.dialog.style.display = "none";
    this.minimized.style.display = "flex";
    chrome.storage.local.set({ visible: true, minimized: true });
  }

  private restore() {
    this.show();
  }

  private restoreVisibilityState() {
    chrome.storage.local.get(["visible", "minimized"], (res) => {
      if (res.visible) {
        if (res.minimized) this.minimize();
        else this.show();
      } else {
        this.show();
      }
    });
  }
}

(() => new FloatingDialog())();
