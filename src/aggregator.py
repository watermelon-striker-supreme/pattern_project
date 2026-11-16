import glob
import json
import numpy as np
from sklearn.metrics import roc_auc_score

if __name__ == "__main__":
    files = glob.glob("mutation_data/result_*.json")
    if not files:
        print("No data found.")
        exit()
        
    spikes = [json.load(open(f))["max_spike"] for f in files]
    
    y_true = [1] * len(spikes) + [0] * len(spikes)
    y_scores = spikes + [0] * len(spikes)
    
    try:
        auc = roc_auc_score(y_true, y_scores)
    except ValueError:
        auc = 0.5
        
    mean_spike = np.mean(spikes)
    std_spike = np.std(spikes)
    detection_rate = (sum(1 for s in spikes if s > 0) / len(spikes)) * 100
    
    print(f"=== {len(files)} REALISTIC MUTATION TRIALS ===")
    print(f"Mean Local Spike: +{mean_spike:.4f}")
    print(f"Standard Deviation: {std_spike:.4f}")
    print(f"Detection Rate (spike > 0): {detection_rate:.2f}%")
    print(f"AUC-ROC Score: {auc:.4f}")
    print(f"Min Spike: {min(spikes)} | Max Spike: {max(spikes)}")