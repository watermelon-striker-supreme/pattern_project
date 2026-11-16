import os
from grammar_engine import compress_sequence, expand_rules, sliding_window_parse

if __name__ == "__main__":
    normal_file = "data/normal_traffic.txt"
    anomaly_file = "data/anomaly_traffic.txt"
    
    if not os.path.exists(normal_file) or not os.path.exists(anomaly_file):
        print("Data files not found.")
        exit()
        
    with open(normal_file, "r") as f:
        normal_seq = f.read()
        
    with open(anomaly_file, "r") as f:
        anomaly_seq = f.read()
        
    train_size = 50000
    window_size = 1000
    
    print(f"--- TRAINING GRAMMAR ON FIRST {train_size} NORMAL CHARS ---")
    train_data = normal_seq[:train_size]
    rules, _ = compress_sequence(train_data, iterations=100)
    expanded_rules = expand_rules(rules)
    
    print(f"Extracted {len(rules)} rules.")
    
    test_normal_data = normal_seq[train_size:train_size + 100000]
    normal_costs = sliding_window_parse(test_normal_data, expanded_rules, window_size)
    normal_cost_per_char = [c / window_size for c in normal_costs]
    
    anomaly_costs = sliding_window_parse(anomaly_seq, expanded_rules, window_size)
    anomaly_cost_per_char = [c / window_size for c in anomaly_costs]
    
    print(f"\n--- WINDOW ANALYSIS (Window Size: {window_size}) ---")
    print(f"Normal Traffic Windows Analyzed: {len(normal_cost_per_char)}")
    if normal_cost_per_char:
        print(f"  Normal Mean Cost/Char: {sum(normal_cost_per_char)/len(normal_cost_per_char):.4f}")
        print(f"  Normal Max Cost/Char:  {max(normal_cost_per_char):.4f}")
        
    print(f"Anomaly Traffic Windows Analyzed: {len(anomaly_cost_per_char)}")
    if anomaly_cost_per_char:
        print(f"  Anomaly Mean Cost/Char: {sum(anomaly_cost_per_char)/len(anomaly_cost_per_char):.4f}")
        print(f"  Anomaly Max Cost/Char:  {max(anomaly_cost_per_char):.4f}")
        
    if normal_cost_per_char and anomaly_cost_per_char:
        mean_ratio = (sum(anomaly_cost_per_char)/len(anomaly_cost_per_char)) / (sum(normal_cost_per_char)/len(normal_cost_per_char))
        print(f"\nMean Anomaly/Normal Ratio: {mean_ratio:.4f}x")
        
        normal_threshold = max(normal_cost_per_char) * 1.1
        anomalies_detected = sum(1 for c in anomaly_cost_per_char if c > normal_threshold)
        detection_rate = (anomalies_detected / len(anomaly_cost_per_char)) * 100
        print(f"Anomaly Windows Exceeding Normal Max (+10% buffer): {anomalies_detected}")
        print(f"Window Detection Rate: {detection_rate:.2f}%")