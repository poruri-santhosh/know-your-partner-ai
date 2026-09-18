// Know Your Partner AI - Analysis & ML Pipeline Progress Engine

const STEPS = [
  { progress: 20, text: "Normalizing 40 situational behavioral signals..." },
  { progress: 45, text: "Extracting 10-dimension personality vector..." },
  { progress: 65, text: "Classifying relational archetype via K-Means clustering..." },
  { progress: 85, text: "Evaluating pairwise distances with trained ML regressors..." },
  { progress: 95, text: "Synthesizing psychological narrative and relationship insights..." },
];

const elProgress = document.getElementById("analysis-progress");
const elStepLabel = document.getElementById("step-label");
const elErrorBox = document.getElementById("error-box");
const elErrorMessage = document.getElementById("error-message");
const elSpinner = document.getElementById("spinner");

async function runAnalysis() {
  elErrorBox.style.display = "none";
  elSpinner.style.display = "block";
  
  // Retrieve answers
  const raw = sessionStorage.getItem("kyp_answers");
  if (!raw) {
    window.location.href = "quiz.html";
    return;
  }
  
  let answers;
  try {
    answers = JSON.parse(raw);
  } catch (e) {
    window.location.href = "quiz.html";
    return;
  }
  
  // Animate initial steps
  let stepIdx = 0;
  const stepInterval = setInterval(() => {
    if (stepIdx < STEPS.length - 1) {
      stepIdx++;
      elProgress.style.width = `${STEPS[stepIdx].progress}%`;
      elStepLabel.textContent = STEPS[stepIdx].text;
    }
  }, 450);
  
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers: answers }),
    });
    
    clearInterval(stepInterval);
    
    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || "Analysis failed on the server.");
    }
    
    const result = await response.json();
    
    // Store result
    sessionStorage.setItem("kyp_result", JSON.stringify(result));
    
    // Final progress state
    elProgress.style.width = "100%";
    elStepLabel.textContent = "Analysis complete! Loading your profile...";
    
    setTimeout(() => {
      window.location.href = "result.html";
    }, 600);
    
  } catch (err) {
    clearInterval(stepInterval);
    console.error("Analysis error:", err);
    elSpinner.style.display = "none";
    elErrorBox.style.display = "block";
    elErrorMessage.textContent = err.message || "An unexpected error occurred while analyzing your profile.";
  }
}

document.addEventListener("DOMContentLoaded", runAnalysis);
