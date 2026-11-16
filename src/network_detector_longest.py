import os
from grammar_engine_longest import compress_longest_first, expand_rules, parse_sequence

def sliding_window_parse(sequence, expanded_rules, window_size=1000):
    costs = []
    for i in range(0, len(sequence) - window_size + 1, window_size):
        chunk = sequence[i:i+window_size]
        _, cost = parse_sequence(chunk, expanded_rules)
        costs.append(cost)
    return costs

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
    
    print(f"--- TRAINING LONGEST-FIRST GRAMMAR ON FIRST {train_size} NORMAL CHARS ---")
    train_data = normal_seq[:train_size]
    
    rules, compressed_string = compress_longest_first(train_data, iterations=500)
    expanded_rules = expand_rules(rules)
    
    print(f"Extracted {len(rules)} rules.")
    
    # --- THE RESIDUAL ANALYSIS ---
    print(f"\n--- RESIDUAL ANALYSIS ---")
    print(f"Final Compressed Length: {len(compressed_string)}")
    
    # Count raw characters (A-Z, a-z, 0-9, -, _)
    raw_chars = [c for c in compressed_string if ord(c) < 945] # 945 is the start of Greek letters
    print(f"Residue Count (Raw Characters): {len(raw_chars)}")
    
    # Print a sample of the raw residue
    print("\nSample of Raw Residue (first 500 chars):")
    print("".join(raw_chars[:500]))

    # --- WINDOW ANALYSIS ---
    test_normal_data = normal_seq[train_size:train_size + 100000]
    normal_costs = sliding_window_parse(test_normal_data, expanded_rules, window_size)
    normal_cost_per_char = [c / window_size for c in normal_costs]
    
    anomaly_costs = sliding_window_parse(anomaly_seq, expanded_rules, window_size)
    anomaly_cost_per_char = [c / window_size for c in anomaly_costs]
    
    print(f"\n--- WINDOW ANALYSIS (Window Size: {window_size}) ---")
    if normal_cost_per_char:
        print(f"  Normal Mean Cost/Char: {sum(normal_cost_per_char)/len(normal_cost_per_char):.4f}")
        print(f"  Normal Max Cost/Char:  {max(normal_cost_per_char):.4f}")
        
    if anomaly_cost_per_char:
        print(f"  Anomaly Mean Cost/Char: {sum(anomaly_cost_per_char)/len(anomaly_cost_per_char):.4f}")
        print(f"  Anomaly Max Cost/Char:  {max(anomaly_cost_per_char):.4f}")
        
        normal_threshold = max(normal_cost_per_char) * 1.1
        anomalies_detected = sum(1 for c in anomaly_cost_per_char if c > normal_threshold)
        detection_rate = (anomalies_detected / len(anomaly_cost_per_char)) * 100
        print(f"\nWindow Detection Rate: {detection_rate:.2f}%")