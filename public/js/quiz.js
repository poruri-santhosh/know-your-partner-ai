// Know Your Partner AI - Interactive Quiz Engine

let questions = [];
let currentIndex = 0;
let answers = {};

// DOM Elements
const elCounter = document.getElementById("question-counter");
const elDimensionName = document.getElementById("dimension-name");
const elProgressBar = document.getElementById("progress-bar");
const elQuestionText = document.getElementById("question-text");
const elOptionsContainer = document.getElementById("options-container");
const elBtnPrev = document.getElementById("btn-prev");
const elBtnNext = document.getElementById("btn-next");
const elAnsweredIndicator = document.getElementById("answered-indicator");
const elPaletteDrawer = document.getElementById("palette-drawer");
const elQuestionsPalette = document.getElementById("questions-palette");
const elBtnTogglePalette = document.getElementById("btn-toggle-palette");

// Dimension icon map
const DIMENSION_ICONS = {
  communication: "💬",
  emotional_openness: "💖",
  social_nature: "👥",
  independence: "🧭",
  family_orientation: "🏡",
  financial_attitude: "💰",
  career_orientation: "💼",
  adventure: "✨",
  conflict_handling: "⚖️",
  lifestyle_preference: "☀️",
};

// Initialize
async function initQuiz() {
  loadSavedState();
  try {
    const res = await fetch("/api/questions");
    if (!res.ok) throw new Error("Failed to load questions from server.");
    questions = await res.json();
    
    renderPalette();
    renderQuestion(currentIndex);
    updateProgress();
  } catch (err) {
    console.error("Error loading questions:", err);
    elQuestionText.textContent = "Unable to connect to backend server. Please make sure the FastAPI backend is running.";
  }
}

function loadSavedState() {
  try {
    const saved = sessionStorage.getItem("kyp_answers");
    if (saved) {
      answers = JSON.parse(saved);
    }
  } catch (e) {
    answers = {};
  }
}

function saveState() {
  try {
    sessionStorage.setItem("kyp_answers", JSON.stringify(answers));
  } catch (e) {
    console.error("Failed to save state:", e);
  }
}

function renderQuestion(index) {
  if (!questions || questions.length === 0) return;
  const q = questions[index];
  
  elCounter.textContent = `Question ${index + 1} of ${questions.length}`;
  elDimensionName.textContent = q.dimension_name || q.dimension;
  
  const icon = DIMENSION_ICONS[q.dimension] || "📌";
  document.querySelector(".dimension-badge span:first-child").textContent = icon;
  
  elQuestionText.textContent = q.question;
  elOptionsContainer.innerHTML = "";
  
  const currentSelection = answers[q.id];
  
  q.options.forEach((opt) => {
    const btn = document.createElement("button");
    btn.className = `option-btn ${currentSelection === opt.id ? "selected" : ""}`;
    btn.innerHTML = `
      <div class="option-key">${opt.id}</div>
      <div class="option-label">${opt.text}</div>
    `;
    btn.addEventListener("click", () => selectOption(q.id, opt.id));
    elOptionsContainer.appendChild(btn);
  });
  
  elBtnPrev.disabled = index === 0;
  
  const isLast = index === questions.length - 1;
  const allAnswered = Object.keys(answers).length === questions.length;
  
  if (isLast || allAnswered) {
    elBtnNext.innerHTML = `Analyze My Profile <span>✨</span>`;
    elBtnNext.className = "btn btn-primary";
  } else {
    elBtnNext.innerHTML = `Next <span>→</span>`;
    elBtnNext.className = "btn btn-primary";
  }
  
  updateProgress();
  updatePaletteHighlights();
}

function selectOption(questionId, optionId) {
  answers[questionId] = optionId;
  saveState();
  
  // Re-render option states
  const buttons = elOptionsContainer.querySelectorAll(".option-btn");
  buttons.forEach((btn) => {
    const key = btn.querySelector(".option-key").textContent.trim();
    if (key === optionId) {
      btn.classList.add("selected");
    } else {
      btn.classList.remove("selected");
    }
  });
  
  updateProgress();
  updatePaletteHighlights();
  
  // Auto advance slightly after selection if not last question
  if (currentIndex < questions.length - 1) {
    setTimeout(() => {
      // Only auto-advance if user hasn't clicked previous or changed question
      if (answers[questionId] === optionId) {
        goToNext();
      }
    }, 280);
  }
}

function updateProgress() {
  const total = questions.length || 40;
  const answeredCount = Object.keys(answers).length;
  const pct = Math.round((answeredCount / total) * 100);
  
  elProgressBar.style.width = `${pct}%`;
  elAnsweredIndicator.textContent = `${answeredCount} / ${total} Answered`;
}

function renderPalette() {
  elQuestionsPalette.innerHTML = "";
  questions.forEach((q, idx) => {
    const item = document.createElement("div");
    item.className = `palette-item ${answers[q.id] ? "answered" : ""} ${idx === currentIndex ? "current" : ""}`;
    item.textContent = idx + 1;
    item.addEventListener("click", () => {
      currentIndex = idx;
      renderQuestion(currentIndex);
    });
    elQuestionsPalette.appendChild(item);
  });
}

function updatePaletteHighlights() {
  const items = elQuestionsPalette.querySelectorAll(".palette-item");
  items.forEach((item, idx) => {
    const q = questions[idx];
    if (!q) return;
    const isAnswered = !!answers[q.id];
    const isCurrent = idx === currentIndex;
    
    item.className = `palette-item ${isAnswered ? "answered" : ""} ${isCurrent ? "current" : ""}`;
  });
}

function goToNext() {
  if (currentIndex < questions.length - 1) {
    currentIndex++;
    renderQuestion(currentIndex);
  } else {
    finishQuiz();
  }
}

function goToPrev() {
  if (currentIndex > 0) {
    currentIndex--;
    renderQuestion(currentIndex);
  }
}

function finishQuiz() {
  const total = questions.length;
  const answeredCount = Object.keys(answers).length;
  
  if (answeredCount < total) {
    // Find first unanswered
    const firstUnanswered = questions.findIndex(q => !answers[q.id]);
    if (firstUnanswered !== -1) {
      const confirmSubmit = confirm(`You have answered ${answeredCount} of ${total} questions. Would you like to finish the remaining questions for highest ML accuracy, or submit now? Click Cancel to complete question ${firstUnanswered + 1}.`);
      if (!confirmSubmit) {
        currentIndex = firstUnanswered;
        renderQuestion(currentIndex);
        return;
      }
    }
  }
  
  // Proceed to analysis
  saveState();
  window.location.href = "analysis.html";
}

// Event Listeners
elBtnPrev.addEventListener("click", goToPrev);
elBtnNext.addEventListener("click", () => {
  if (currentIndex === questions.length - 1 || Object.keys(answers).length === questions.length) {
    finishQuiz();
  } else {
    goToNext();
  }
});

elBtnTogglePalette.addEventListener("click", () => {
  const isHidden = elPaletteDrawer.style.display === "none";
  elPaletteDrawer.style.display = isHidden ? "block" : "none";
  elBtnTogglePalette.innerHTML = isHidden ? "Overview (40) ▴" : "Overview (40) ▾";
});

// Keyboard navigation
window.addEventListener("keydown", (e) => {
  // Ignore when inputs have focus
  if (["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) return;
  
  const key = e.key.toUpperCase();
  const q = questions[currentIndex];
  if (!q) return;
  
  const optionKeys = ["A", "B", "C", "D"];
  const numberKeys = ["1", "2", "3", "4"];
  
  if (optionKeys.includes(key)) {
    selectOption(q.id, key);
  } else if (numberKeys.includes(key)) {
    const optIndex = parseInt(key, 10) - 1;
    if (q.options[optIndex]) {
      selectOption(q.id, q.options[optIndex].id);
    }
  } else if (e.key === "Enter" || e.key === "ArrowRight") {
    goToNext();
  } else if (e.key === "ArrowLeft") {
    goToPrev();
  }
});

// Start
document.addEventListener("DOMContentLoaded", initQuiz);
