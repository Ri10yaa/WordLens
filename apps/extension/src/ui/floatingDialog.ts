import type { ContextualMeaningResponse } from "../../../../packages/shared/ts/context";

type DisplayPayload = ContextualMeaningResponse;

const AGENT_TITLE = "WORD LENS";

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
        <header class="ai-dict-header">
          <div>
            <p class="ai-dict-label">${AGENT_TITLE}</p>
            <p class="ai-dict-sub">Contextual Meaning Agent</p>
          </div>
          <div class="ai-header-actions">
            <button id="ai-dict-minimize" class="ai-circle-btn" aria-label="Minimize">–</button>
            <button id="ai-dict-close" class="ai-circle-btn" aria-label="Close">✕</button>
          </div>
        </header>
        <div id="ai-dict-messages" class="ai-messages"></div>
        <div class="ai-input-container">
          <input id="ai-input" type="text" placeholder="Type a word to analyze" />
          <button id="ai-search" class="ai-primary-btn">Go</button>
        </div>
        <div id="ai-loading" class="ai-loading" style="display:none;">running inference…</div>
      </div>
      <button id="ai-minimized" class="ai-minimized" style="display:none;" aria-label="Restore panel">
        <span>Word</span>
        <span>Lens</span>
      </button>
    `;

    const style = document.createElement("style");
    style.innerHTML = `
      .ai-dict-dialog {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 400px;
        max-width: 90vw;
        max-height: calc(100vh - 48px);
        min-height: 220px;
        background: #070509;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 4px;
        display: flex;
        flex-direction: column;
        font-family: 'Space Grotesk', 'Sora', sans-serif;
        font-size: 16px;
        z-index: 2147483647;
        box-shadow: 0 34px 80px rgba(5, 6, 9, 0.75);
      }
      .ai-dict-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 20px 8px;
        color: #f6f7fb;
        letter-spacing: 0.12em;
      }
      .ai-dict-label {
        margin: 0;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }
      .ai-dict-sub {
        margin: 6px 0 0;
        font-size: 13px;
        color: rgba(239, 245, 255, 0.6);
        letter-spacing: 0.1em;
      }
      .ai-header-actions {
        display: flex;
        gap: 6px;
      }
      .ai-circle-btn {
        width: 32px;
        height: 32px;
        border-radius: 4px;
        border: none;
        background: rgba(255, 255, 255, 0.12);
        color: #eff5ff;
        font-size: 16px;
        cursor: pointer;
        transition: background 0.2s ease;
      }
      .ai-circle-btn:hover {
        background: rgba(255, 255, 255, 0.2);
      }
      .ai-messages {
        padding: 10px 20px 18px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 18px;
        max-height: calc(70vh - 140px);
      }
      .ai-messages::-webkit-scrollbar {
        width: 6px;
      }
      .ai-messages::-webkit-scrollbar-track {
        background: transparent;
      }
      .ai-messages::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 8px;
      }
      .ai-messages::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.4);
      }
      .ai-card {
        background: #080911;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 4px;
        padding: 14px 16px;
        color: #f7f7f9;
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
      }
      .ai-card-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 10px;
      }
      .ai-word {
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.4em;
      }
      .ai-confidence {
        font-size: 11px;
        color: rgba(255, 255, 255, 0.6);
      }
      .ai-definition {
        min-height: 60px;
        margin: 0;
        font-size: 12px;
        line-height: 1.55;
      }
      .ai-meta {
        margin-top: 10px;
        font-size: 11px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.55);
      }
      .ai-input-container {
        display: flex;
        gap: 10px;
        padding: 16px 20px 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        margin-top: auto;
      }
      #ai-input {
        flex: 1;
        background: #020204;
        border: 1px solid rgba(255, 255, 255, 0.24);
        color: #f5f6fb;
        padding: 11px 14px;
        border-radius: 4px;
        font-size: 15px;
        letter-spacing: 0.05em;
      }
      .ai-primary-btn {
        background: linear-gradient(110deg, #f7fbff, #cfd8f0);
        color: #050505;
        border: none;
        border-radius: 4px;
        padding: 11px 20px;
        font-weight: 600;
        cursor: pointer;
        letter-spacing: 0.1em;
      }
      .ai-primary-btn:hover {
        opacity: 0.85;
      }
      .ai-loading {
        text-align: center;
        padding: 8px 0 16px;
        color: #969ab1;
        font-size: 11px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }
      .ai-minimized {
        position: fixed;
        bottom: 24px;
        right: 24px;
        min-width: 46px;
        min-height: 46px;
        padding: 0 14px;
        border-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        background: #050507;
        color: #f5f6fb;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 2147483647;
        box-shadow: 0 14px 34px rgba(5, 7, 9, 0.55);
      }
      .ai-minimized:hover {
        background: #090a0f;
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

    const card = document.createElement("section");
    card.className = "ai-card";

    const header = document.createElement("div");
    header.className = "ai-card-header";
    const wordEl = document.createElement("span");
    wordEl.className = "ai-word";
    wordEl.textContent = data.word.toUpperCase();
    const confEl = document.createElement("span");
    confEl.className = "ai-confidence";
    confEl.textContent = data.confidence
      ? `confidence ${Math.round(data.confidence * 100)}%`
      : "confidence —";
    header.append(wordEl, confEl);

    const definitionEl = document.createElement("p");
    definitionEl.className = "ai-definition";
    definitionEl.textContent = "";

    const meta = document.createElement("div");
    meta.className = "ai-meta";
    const senseLabel = data.sense_id ? data.sense_id.replace(/\./g, " · ") : "unranked sense";
    meta.textContent = `signal ${senseLabel}`;

    card.append(header, definitionEl, meta);
    this.messages.appendChild(card);
    this.messages.scrollTop = this.messages.scrollHeight;

    this.streamDefinition(definitionEl, data.definition ?? "No definition available");
  }

  private streamDefinition(target: HTMLElement, text: string) {
    const words = text.split(/\s+/).filter(Boolean);
    if (!words.length) {
      target.textContent = "No definition available";
      return;
    }

    target.textContent = "";
    let index = 0;
    const interval = window.setInterval(() => {
      target.textContent = `${target.textContent ?? ""}${index === 0 ? "" : " "}${words[index]}`;
      index += 1;
      if (index >= words.length) {
        window.clearInterval(interval);
      }
    }, 70);
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
