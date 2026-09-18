# ❤️ Know Your Partner AI

> **Scientific Behavioral Profiling & Machine Learning Compatibility Engine**

Know Your Partner AI moves away from simplistic, self-rated quizzes. Instead, it measures real-world behavioral choices across **10 foundational dimensions**, transforms responses into normalized feature vectors, extracts pairwise difference and interaction metrics, and predicts compatibility using trained machine learning models.

---

## 🌟 Key Features

1. **40 Situational Questions**: 4 questions per dimension targeting actual real-world actions (conflict de-escalation, money windfall decisions, career relocations, domestic routine).
2. **10 Behavioral Dimensions**:
   - Communication
   - Emotional Openness
   - Conflict Handling
   - Financial Attitude
   - Family Orientation
   - Independence
   - Career Orientation
   - Adventure & Spontaneity
   - Social Nature
   - Lifestyle & Routine
3. **Machine Learning Pipeline**:
   - Pairwise feature extraction: absolute differences, interaction terms (`comm_x_conflict`, `finance_x_career`, `family_x_lifestyle`), and Euclidean distance.
   - Evaluates Linear Regression, Random Forest, and Gradient Boosting Regressors ($R^2 \approx 0.84$, $\text{MAE} \approx 1.64$).
   - K-Means Behavioral Clustering ($k=5$) identifying relational archetypes (*The Grounded Anchor*, *The Trailblazer*, *The Empathetic Harmonizer*, *The Spontaneous Explorer*, *The Thoughtful Diplomat*).
4. **Ideal Partner Synthesis & Candidate Matching**:
   - Synthesizes the complementary target profile.
   - Ranks real-world candidate archetypes by predicted compatibility.
5. **Psychological AI Narrative**:
   - Synthesizes relationship strengths, ideal partner traits, and communication advice (Google Gemini API with rich behavioral science heuristic fallback).
6. **Interactive Web Dashboard**:
   - Dual-bar 10-dimension comparison matrix.
   - Real-time custom partner slider simulator.
   - One-click report export and print preview.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Machine Learning Models
```bash
python backend/app/ml/train.py
```
This generates the calibrated dataset in `backend/app/data/datasets/compatibility_data.csv`, trains regression and clustering models, and saves the artifacts to `backend/app/models/`.

### 3. Run Automated Tests
```bash
python -m pytest -v
```

### 4. Start the Application Server
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser to:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📂 Project Structure

```
know-your-partner-ai/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI REST endpoints
│   │   │   ├── analysis.py  # Scoring & prediction endpoints
│   │   │   ├── questions.py # 40 situational questions & metadata
│   │   │   └── results.py   # Model info & submission retrieval
│   │   ├── data/            # Datasets, questions, SQLite database
│   │   │   ├── datasets/    # compatibility_data.csv
│   │   │   └── questions.py # 40 situational questions definition
│   │   ├── database/        # SQLite connection & models
│   │   ├── ml/              # Core ML pipeline
│   │   │   ├── scoring.py   # Raw & min-max score normalization
│   │   │   ├── feature_engineering.py # Pair difference vectors
│   │   │   ├── compatibility.py       # Candidate archetypes & math formula
│   │   │   ├── predict.py   # ML inference & archetype classification
│   │   │   └── train.py     # Regressor training & K-Means clustering
│   │   ├── models/          # Serialized .pkl models
│   │   ├── services/        # Orchestration & AI narrative synthesis
│   │   └── main.py          # FastAPI application entry point
│   └── requirements.txt
├── frontend/                # Interactive web client
│   ├── css/style.css        # Responsive dark/glassmorphic styling
│   ├── js/
│   │   ├── quiz.js          # 40-question quiz controller
│   │   ├── analysis.js      # Loading & ML progress animation
│   │   └── result.js        # Dashboard, dual-bar chart & simulator
│   ├── index.html           # Landing page
│   ├── quiz.html            # Step-by-step questionnaire
│   ├── analysis.html        # Processing screen
│   └── result.html          # Interactive results dashboard
├── notebooks/               # Research & exploration notebooks
│   ├── data_analysis.ipynb
│   ├── model_training.ipynb
│   └── model_testing.ipynb
├── tests/                   # Automated pytest suite (18 tests)
│   ├── test_scoring.py
│   ├── test_compatibility.py
│   └── test_api.py
└── requirements.txt
```

---

## 📡 API Reference

- `GET /api/questions` - Returns all 40 questions with answer choices.
- `GET /api/dimensions` - Returns the 10 behavioral dimensions with definitions.
- `POST /api/analyze` - Submits answers, calculates scores, runs ML model, and returns full analysis.
- `POST /api/compare` - Compares two arbitrary profile vectors and returns compatibility.
- `GET /api/candidates` - Retrieves available candidate archetypes.
- `GET /api/model-info` - Returns active ML model metadata, evaluation metrics, and archetypes.
- `GET /api/health` - Service health status.
