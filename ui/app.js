const dropzone = document.getElementById("dropzone");
const browseBtn = document.getElementById("browseBtn");
const statusBox = document.getElementById("status");
const resultBox = document.getElementById("resultBox");
const resultFilename = document.getElementById("resultFilename");
const resultText = document.getElementById("resultText");
const copyBtn = document.getElementById("copyBtn");
const historyEl = document.getElementById("history");

function setStatus(message, isError) {
  statusBox.textContent = message;
  statusBox.classList.remove("hidden");
  statusBox.classList.toggle("error", !!isError);
}

function clearStatus() {
  statusBox.classList.add("hidden");
}

function showResult(filename, text) {
  resultFilename.textContent = filename;
  resultText.value = text;
  resultBox.classList.remove("hidden");
}

const SUPPORTED_EXTENSIONS = [".ogg", ".mp3", ".aiff", ".aif"];

async function transcribePath(path) {
  const lowerPath = path.toLowerCase();
  if (!SUPPORTED_EXTENSIONS.some((ext) => lowerPath.endsWith(ext))) {
    setStatus(
      `Formato não suportado. Formatos aceitos: ${SUPPORTED_EXTENSIONS.join(", ")}`,
      true
    );
    return;
  }
  setStatus("Transcrevendo... isso pode levar alguns instantes.");
  resultBox.classList.add("hidden");

  const result = await window.pywebview.api.transcribe_file(path);

  if (!result.ok) {
    setStatus("Erro: " + result.error, true);
    return;
  }

  clearStatus();
  const filename = path.split(/[\\/]/).pop();
  showResult(filename, result.text);
  await loadHistory();
}

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("dragover");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragover");
});

dropzone.addEventListener("drop", (e) => {
  // O caminho completo do arquivo é resolvido no lado Python (webview.dom) e
  // entregue via window.transcribePath(); aqui só cuidamos do feedback visual.
  e.preventDefault();
  dropzone.classList.remove("dragover");
});

browseBtn.addEventListener("click", async () => {
  const path = await window.pywebview.api.open_file_dialog();
  if (path) {
    await transcribePath(path);
  }
});

copyBtn.addEventListener("click", () => {
  resultText.select();
  document.execCommand("copy");
});

function formatDayLabel(dateStr) {
  const today = new Date();
  const todayStr = today.toISOString().slice(0, 10);
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  const yesterdayStr = yesterday.toISOString().slice(0, 10);

  if (dateStr === todayStr) return "Hoje";
  if (dateStr === yesterdayStr) return "Ontem";

  const [y, m, d] = dateStr.split("-");
  return `${d}/${m}/${y}`;
}

function formatTime(isoDateTime) {
  const timePart = isoDateTime.split("T")[1] || "";
  return timePart.slice(0, 5);
}

async function loadHistory() {
  const groups = await window.pywebview.api.get_history();
  historyEl.innerHTML = "";

  if (!groups || groups.length === 0) {
    historyEl.innerHTML = '<p class="muted">Nenhuma transcrição ainda.</p>';
    return;
  }

  for (const group of groups) {
    const groupEl = document.createElement("div");
    groupEl.className = "day-group";

    const title = document.createElement("div");
    title.className = "day-title";
    title.textContent = formatDayLabel(group.date);
    groupEl.appendChild(title);

    for (const item of group.items) {
      const itemEl = document.createElement("div");
      itemEl.className = "history-item";
      itemEl.innerHTML = `
        <div class="fname">${item.filename}</div>
        <div class="time">${formatTime(item.created_at)}</div>
      `;
      itemEl.addEventListener("click", () => {
        showResult(item.filename, item.transcript_text);
        clearStatus();
      });
      groupEl.appendChild(itemEl);
    }

    historyEl.appendChild(groupEl);
  }
}

window.addEventListener("pywebviewready", () => {
  loadHistory();
});
