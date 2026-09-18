// Know Your Partner AI - Interactive Results Dashboard & Simulator

let resultData = null;
let currentPartnerProfile = null;
let currentPartnerName = "Ideal Complementary Profile";

const DIMENSION_META = {
  communication: { name: "Communication", icon: "💬" },
  emotional_openness: { name: "Emotional Openness", icon: "💖" },
  social_nature: { name: "Social Nature", icon: "👥" },
  independence: { name: "Independence", icon: "🧭" },
  family_orientation: { name: "Family Orientation", icon: "🏡" },
  financial_attitude: { name: "Financial Attitude", icon: "💰" },
  career_orientation: { name: "Career Orientation", icon: "💼" },
  adventure: { name: "Adventure & Spontaneity", icon: "✨" },
  conflict_handling: { name: "Conflict Handling", icon: "⚖️" },
  lifestyle_preference: { name: "Lifestyle & Routine", icon: "☀️" },
};

function initResults() {
  const raw = sessionStorage.getItem("kyp_result");
  if (!raw) {
    window.location.href = "quiz.html";
    return;
  }
  
  try {
    resultData = JSON.parse(raw);
  } catch (e) {
    console.error("Failed to parse result data:", e);
    window.location.href = "quiz.html";
    return;
  }
  
  currentPartnerProfile = resultData.ideal_partner_profile;
  
  renderHeader();
  renderComparisonMatrix();
  renderPsychologicalBreakdown();
  renderNarrative();
  renderCandidates();
  renderSimulator();
}

function animateScore(targetValue) {
  const elScore = document.getElementById("overall-score");
  let current = 0;
  const target = Math.round(targetValue);
  const step = Math.max(1, Math.floor(target / 40));
  
  const timer = setInterval(() => {
    current += step;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    elScore.textContent = `${current}%`;
  }, 20);
}

function renderHeader() {
  const arch = resultData.archetype || {};
  document.getElementById("archetype-name").textContent = arch.name || "Balanced Partner";
  document.getElementById("archetype-tagline").textContent = arch.tagline || "Navigates relationships with thoughtful alignment.";
  document.getElementById("archetype-badge").textContent = arch.badge ? `Archetype: ${arch.badge}` : "Behavioral Archetype";
  
  animateScore(resultData.overall_compatibility || 85);
  
  document.getElementById("model-name").textContent = resultData.model_used || "Trained Regression Model";
  document.getElementById("compare-target-name").textContent = `Target: ${currentPartnerName}`;
  
  // Render dominant tags
  const tagsContainer = document.getElementById("dominant-tags");
  tagsContainer.innerHTML = "";
  if (resultData.dominant_traits) {
    resultData.dominant_traits.forEach((t) => {
      const tag = document.createElement("span");
      tag.className = "badge-pill";
      tag.style.margin = "0";
      tag.style.fontSize = "0.8rem";
      tag.textContent = `${t.name}: ${Math.round(t.score)}% (${t.level})`;
      tagsContainer.appendChild(tag);
    });
  }
}

function renderComparisonMatrix() {
  const matrix = document.getElementById("dimensions-matrix");
  matrix.innerHTML = "";
  
  const userProf = resultData.user_profile || {};
  const partnerProf = currentPartnerProfile || {};
  
  Object.keys(DIMENSION_META).forEach((dim) => {
    const meta = DIMENSION_META[dim];
    const uScore = Math.round(userProf[dim] || 50);
    const pScore = Math.round(partnerProf[dim] || 50);
    const diff = Math.abs(uScore - pScore);
    const matchPct = Math.max(0, 100 - diff);
    
    const row = document.createElement("div");
    row.className = "dimension-row";
    row.innerHTML = `
      <div class="dimension-label-row">
        <span style="font-weight: 600; display: flex; align-items: center; gap: 6px;">
          <span>${meta.icon}</span> ${meta.name}
        </span>
        <span style="color: var(--text-muted); font-size: 0.8rem;">
          Diff: ${diff} pts | <strong style="color: #34d399;">${matchPct}% Match</strong>
        </span>
      </div>
      <div class="bar-dual-container">
        <!-- User Bar -->
        <div style="display: flex; align-items: center; gap: 10px;">
          <div class="bar-wrapper">
            <div class="bar-fill-user" style="width: 0%;" data-target="${uScore}"></div>
          </div>
          <span style="font-size: 0.75rem; color: #a5b4fc; width: 35px; text-align: right;">${uScore}%</span>
        </div>
        <!-- Partner Bar -->
        <div style="display: flex; align-items: center; gap: 10px;">
          <div class="bar-wrapper">
            <div class="bar-fill-partner" style="width: 0%;" data-target="${pScore}"></div>
          </div>
          <span style="font-size: 0.75rem; color: #f472b6; width: 35px; text-align: right;">${pScore}%</span>
        </div>
      </div>
    `;
    matrix.appendChild(row);
  });
  
  // Trigger bar animations
  setTimeout(() => {
    document.querySelectorAll(".bar-fill-user").forEach((b) => {
      b.style.width = `${b.getAttribute("data-target")}%`;
    });
    document.querySelectorAll(".bar-fill-partner").forEach((b) => {
      b.style.width = `${b.getAttribute("data-target")}%`;
    });
  }, 100);
}

function renderPsychologicalBreakdown() {
  const strengthsContainer = document.getElementById("strengths-list");
  strengthsContainer.innerHTML = "";
  
  const narrative = resultData.ai_narrative || {};
  const strengths = narrative.relationship_strengths || [];
  
  if (strengths.length > 0) {
    strengths.forEach((s) => {
      const item = document.createElement("div");
      item.className = "strength-bullet";
      item.innerHTML = `<span class="bullet-icon">✔</span> <span>${s}</span>`;
      strengthsContainer.appendChild(item);
    });
  } else if (resultData.dominant_traits) {
    resultData.dominant_traits.forEach((t) => {
      const item = document.createElement("div");
      item.className = "strength-bullet";
      item.innerHTML = `<span class="bullet-icon">✔</span> <span>Strong ${t.name} (${Math.round(t.score)}%): ${t.description}</span>`;
      strengthsContainer.appendChild(item);
    });
  }
  
  document.getElementById("partner-needs-text").textContent =
    narrative.ideal_partner_qualities ||
    "Your responses suggest optimal harmony with a partner who mirrors your dedication to communication while offering complementary balance.";
    
  document.getElementById("growth-advice-box").textContent =
    narrative.growth_advice ||
    "Observe how stress impacts emotional regulation. Regular proactive check-ins maintain harmony.";
}

function renderNarrative() {
  const narrative = resultData.ai_narrative || {};
  document.getElementById("ai-engine-label").textContent = narrative.source || "Psychological Synthesis";
  document.getElementById("ai-summary-text").textContent = narrative.summary || "Your behavioral profile indicates a strong commitment to stability and clear communication.";
  document.getElementById("ai-partner-qualities").textContent = narrative.ideal_partner_qualities || "";
  
  if (narrative.disclaimer) {
    document.getElementById("ai-disclaimer").textContent = narrative.disclaimer;
  }
}

function renderCandidates() {
  const container = document.getElementById("candidates-grid");
  container.innerHTML = "";
  
  const matches = resultData.candidate_matches || [];
  matches.forEach((cand) => {
    const card = document.createElement("div");
    card.className = "candidate-card";
    card.id = `cand-card-${cand.id}`;
    
    card.innerHTML = `
      <div class="candidate-header">
        <div>
          <h4 style="font-size: 1.1rem; font-weight: 700;">${cand.name}</h4>
          <span style="font-size: 0.8rem; color: #a5b4fc;">${cand.archetype}</span>
        </div>
        <div class="candidate-match-pill">${Math.round(cand.compatibility_score)}% Match</div>
      </div>
      <p style="font-size: 0.88rem; color: var(--text-secondary); margin-bottom: 16px; line-height: 1.5;">
        ${cand.tagline}
      </p>
      <button class="btn btn-secondary btn-sm" style="width: 100%;" onclick="switchToCandidate('${cand.id}')">
        Compare With ${cand.name.split(' ')[0]} <span>⇄</span>
      </button>
    `;
    container.appendChild(card);
  });
}

window.switchToCandidate = function(candidateId) {
  const cand = (resultData.candidate_matches || []).find((c) => c.id === candidateId);
  if (!cand) return;
  
  currentPartnerProfile = cand.scores;
  currentPartnerName = cand.name;
  
  document.getElementById("compare-target-name").textContent = `Target: ${cand.name}`;
  animateScore(cand.compatibility_score);
  
  renderComparisonMatrix();
  
  // Highlight active card
  document.querySelectorAll(".candidate-card").forEach((c) => {
    c.style.borderColor = "var(--border-subtle)";
  });
  const activeCard = document.getElementById(`cand-card-${candidateId}`);
  if (activeCard) {
    activeCard.style.borderColor = "#ec4899";
  }
};

function renderSimulator() {
  const container = document.getElementById("simulator-sliders");
  container.innerHTML = "";
  
  Object.keys(DIMENSION_META).forEach((dim) => {
    const meta = DIMENSION_META[dim];
    const initialVal = Math.round(currentPartnerProfile[dim] || 75);
    
    const wrapper = document.createElement("div");
    wrapper.innerHTML = `
      <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
        <span>${meta.icon} ${meta.name}</span>
        <span id="slider-val-${dim}" style="color: #ec4899; font-weight: 700;">${initialVal}%</span>
      </div>
      <input type="range" id="slider-${dim}" min="10" max="100" value="${initialVal}" style="width: 100%; accent-color: #ec4899;" oninput="updateSliderVal('${dim}')">
    `;
    container.appendChild(wrapper);
  });
}

window.updateSliderVal = function(dim) {
  const slider = document.getElementById(`slider-${dim}`);
  const label = document.getElementById(`slider-val-${dim}`);
  if (slider && label) {
    label.textContent = `${slider.value}%`;
  }
};

document.getElementById("btn-calc-custom").addEventListener("click", async () => {
  const partnerVector = {};
  Object.keys(DIMENSION_META).forEach((dim) => {
    const slider = document.getElementById(`slider-${dim}`);
    partnerVector[dim] = slider ? parseFloat(slider.value) : 75.0;
  });
  
  try {
    const res = await fetch("/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_profile: resultData.user_profile,
        partner_profile: partnerVector,
      }),
    });
    
    if (!res.ok) throw new Error("Comparison failed");
    const data = await res.json();
    
    currentPartnerProfile = partnerVector;
    currentPartnerName = "Custom Simulated Partner";
    document.getElementById("compare-target-name").textContent = "Target: Custom Simulated Partner";
    
    animateScore(data.overall_compatibility);
    renderComparisonMatrix();
    
    const alertBox = document.getElementById("custom-result-alert");
    alertBox.style.display = "block";
    document.getElementById("custom-score-text").textContent =
      `Predicted Compatibility: ${data.overall_compatibility}% (${data.model_used})`;
      
  } catch (err) {
    alert("Could not compute custom compatibility: " + err.message);
  }
});

document.addEventListener("DOMContentLoaded", initResults);
