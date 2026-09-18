"""Model training pipeline for compatibility regression and behavioral clustering."""

import os
import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Ensure backend root is on sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.data.questions import DIMENSIONS
from app.ml.feature_engineering import DIMENSION_KEYS, FEATURE_NAMES, extract_pair_features, features_to_vector

DATASET_DIR = BACKEND_DIR / "app" / "data" / "datasets"
MODELS_DIR = BACKEND_DIR / "app" / "models"
CSV_PATH = DATASET_DIR / "compatibility_data.csv"
MODEL_PATH = MODELS_DIR / "compatibility_model.pkl"
KMEANS_PATH = MODELS_DIR / "kmeans_archetypes.pkl"

ARCHETYPE_LABELS = {
    0: {
        "name": "The Grounded Anchor",
        "tagline": "Values deep family roots, financial security, and organized stability.",
        "badge": "Anchor",
    },
    1: {
        "name": "The Trailblazer",
        "tagline": "Driven by career vision, intellectual ambition, and mutual autonomy.",
        "badge": "Trailblazer",
    },
    2: {
        "name": "The Empathetic Harmonizer",
        "tagline": "Prioritizes deep emotional connection, open dialogue, and gentle conflict resolution.",
        "badge": "Harmonizer",
    },
    3: {
        "name": "The Spontaneous Explorer",
        "tagline": "Energized by adventure, social discovery, novelty, and flexible spontaneity.",
        "badge": "Explorer",
    },
    4: {
        "name": "The Thoughtful Diplomat",
        "tagline": "A calm, highly communicative presence who builds balanced, peaceful partnerships.",
        "badge": "Diplomat",
    },
}


def generate_synthetic_dataset(n_samples: int = 3000, random_state: int = 42) -> pd.DataFrame:
    """
    Generate statistically realistic pairwise compatibility data based on empirical
    relationship research principles.
    """
    rng = np.random.default_rng(random_state)
    
    rows = []
    
    # Archetype centers around which simulated profiles cluster
    archetype_centers = [
        [80, 75, 55, 60, 90, 88, 75, 45, 84, 85],  # Anchor
        [85, 68, 65, 85, 65, 82, 92, 68, 80, 72],  # Trailblazer
        [92, 90, 70, 65, 82, 74, 70, 58, 90, 78],  # Harmonizer
        [78, 72, 85, 80, 60, 62, 75, 92, 74, 52],  # Explorer
        [88, 80, 62, 72, 78, 80, 80, 64, 88, 80],  # Diplomat
    ]
    
    for _ in range(n_samples):
        # Sample person A and person B from varied distributions
        center_a = archetype_centers[rng.integers(0, len(archetype_centers))]
        center_b = archetype_centers[rng.integers(0, len(archetype_centers))]
        
        profile_a = {
            dim: float(np.clip(center_a[i] + rng.normal(0, 12), 10, 100))
            for i, dim in enumerate(DIMENSION_KEYS)
        }
        profile_b = {
            dim: float(np.clip(center_b[i] + rng.normal(0, 12), 10, 100))
            for i, dim in enumerate(DIMENSION_KEYS)
        }
        
        feats = extract_pair_features(profile_a, profile_b)
        
        # Ground truth relationship formula with non-linear penalties and interaction dynamics
        # Core alignment penalty: communication & conflict differences are most damaging
        comm_penalty = 0.22 * feats["communication_diff"]
        conflict_penalty = 0.22 * feats["conflict_handling_diff"]
        finance_penalty = 0.16 * feats["financial_attitude_diff"]
        family_penalty = 0.14 * feats["family_orientation_diff"]
        emotional_penalty = 0.12 * feats["emotional_openness_diff"]
        lifestyle_penalty = 0.10 * feats["lifestyle_preference_diff"]
        career_penalty = 0.06 * feats["career_orientation_diff"]
        social_penalty = 0.04 * feats["social_nature_diff"]
        indep_penalty = 0.03 * feats["independence_diff"]
        advent_penalty = 0.03 * feats["adventure_diff"]
        
        # Interaction compound penalty (when both communication AND conflict have high differences)
        compound_penalty = 0.08 * feats["comm_x_conflict_diff"]
        
        # High extreme difference penalty
        extreme_penalty = 0.05 * (feats["max_abs_diff"] ** 1.1)
        
        total_penalty = (
            comm_penalty + conflict_penalty + finance_penalty + family_penalty +
            emotional_penalty + lifestyle_penalty + career_penalty + social_penalty +
            indep_penalty + advent_penalty + compound_penalty + extreme_penalty
        )
        
        # Add realistic noise
        noise = rng.normal(0, 2.0)
        
        compatibility = float(np.clip(100.0 - (total_penalty * 0.82) + noise, 12.0, 99.0))
        
        row = dict(feats)
        row["compatibility_score"] = round(compatibility, 2)
        rows.append(row)
        
    df = pd.DataFrame(rows)
    return df


def train_models():
    """Train regression models and clustering pipeline; save serialized artifacts."""
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("1. Generating calibrated compatibility dataset...", flush=True)
    df = generate_synthetic_dataset(n_samples=1500)
    df.to_csv(CSV_PATH, index=False)
    print(f"   Saved {len(df)} pair records to {CSV_PATH}", flush=True)
    
    # 2. Train Compatibility Regressor
    X = df[FEATURE_NAMES]
    y = df["compatibility_score"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    candidates = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=60, learning_rate=0.1, max_depth=3, random_state=42),
    }
    
    results = {}
    best_model = None
    best_name = ""
    best_mae = float("inf")
    
    print("\n2. Training and evaluating regression models:", flush=True)
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        
        results[name] = {
            "mae": round(float(mae), 3),
            "rmse": round(float(rmse), 3),
            "r2": round(float(r2), 4),
        }
        print(f"   - {name}: MAE={mae:.3f}, RMSE={rmse:.3f}, R2={r2:.4f}", flush=True)
        
        if mae < best_mae:
            best_mae = mae
            best_model = model
            best_name = name
            
    print(f"\n   -> Best Model Selected: {best_name} (MAE: {best_mae:.3f})")
    
    model_payload = {
        "model": best_model,
        "model_name": best_name,
        "feature_names": FEATURE_NAMES,
        "metrics": results[best_name],
        "all_metrics": results,
    }
    joblib.dump(model_payload, MODEL_PATH)
    print(f"   Saved trained compatibility model to {MODEL_PATH}")
    
    # 3. Fit K-Means Archetype Clusterer on 10 behavioral dimensions
    print("\n3. Fitting K-Means Behavioral Archetype Clusterer (k=5)...")
    
    # Generate realistic population profile vectors for clustering
    rng = np.random.default_rng(42)
    pop_profiles = []
    archetype_anchors = [
        [82, 75, 55, 60, 90, 88, 76, 48, 84, 85],  # Anchor
        [86, 68, 65, 85, 65, 82, 92, 68, 80, 72],  # Trailblazer
        [92, 90, 70, 65, 82, 74, 70, 58, 90, 78],  # Harmonizer
        [78, 72, 82, 80, 60, 62, 75, 92, 74, 52],  # Explorer
        [88, 80, 62, 72, 78, 80, 80, 64, 88, 80],  # Diplomat
    ]
    for _ in range(2000):
        anchor = archetype_anchors[rng.integers(0, len(archetype_anchors))]
        sample = np.clip(anchor + rng.normal(0, 10, len(anchor)), 10, 100)
        pop_profiles.append(sample)
        
    pop_profiles = np.array(pop_profiles)
    
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(pop_profiles)
    
    # Map cluster indices to semantic archetypes by finding closest anchor
    cluster_centers = kmeans.cluster_centers_
    cluster_mapping = {}
    
    for c_idx in range(5):
        center = cluster_centers[c_idx]
        # Find closest archetype anchor
        dists = [np.linalg.norm(center - np.array(a)) for a in archetype_anchors]
        best_anchor_idx = int(np.argmin(dists))
        cluster_mapping[c_idx] = ARCHETYPE_LABELS[best_anchor_idx]
        
    kmeans_payload = {
        "kmeans": kmeans,
        "dimension_keys": DIMENSION_KEYS,
        "cluster_mapping": cluster_mapping,
        "archetype_labels": ARCHETYPE_LABELS,
    }
    joblib.dump(kmeans_payload, KMEANS_PATH)
    print(f"   Saved K-Means clustering model to {KMEANS_PATH}")
    print("\nTraining completed successfully!")
    return results


if __name__ == "__main__":
    train_models()
