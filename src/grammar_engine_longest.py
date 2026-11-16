import os

def read_fasta(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return "".join([line.strip() for line in lines if not line.startswith(">")])

def find_best_substring_by_savings(sequence, max_len=60):
    best_sub = None
    best_freq = 0
    best_savings = 0
    
    # Scan all lengths
    for length in range(max_len, 1, -1):
        counts = {}
        for i in range(len(sequence) - length + 1):
            sub = sequence[i:i+length]
            # THE ISDIGIT BUG IS GONE
            counts[sub] = counts.get(sub, 0) + 1
            
        for sub, freq in counts.items():
            if freq >= 2:
                # YOUR EXACT FORMULA
                savings = (length * freq) - freq
                if savings > best_savings:
                    best_savings = savings
                    best_sub = sub
                    best_freq = freq
                    
    return best_sub, best_freq, best_savings

def compress_longest_first(sequence, iterations=500):
    rules = {}
    current_seq = sequence
    
    print(f"--- INITIAL SEQUENCE LENGTH: {len(current_seq)} ---")

    for i in range(iterations):
        best_sub, freq, savings = find_best_substring_by_savings(current_seq, max_len=60)
        
        if not best_sub or savings <= 0:
            break

        new_symbol = chr(945 + i) 
        rules[new_symbol] = best_sub
        current_seq = current_seq.replace(best_sub, new_symbol)
        
        print(f"Rule {new_symbol} -> Len {len(best_sub)} (Freq: {freq}) | Savings: {savings} | New Length: {len(current_seq)}")

    print(f"--- FINAL COMPRESSED SEQUENCE LENGTH: {len(current_seq)} ---")
    return rules, current_seq

def expand_rules(rules):
    expanded = {}
    for symbol, pattern in rules.items():
        expanded_pattern = "".join([expanded.get(char, char) for char in pattern])
        expanded[symbol] = expanded_pattern
    return expanded

def parse_sequence(sequence, expanded_rules):
    sorted_rules = sorted(expanded_rules.items(), key=lambda x: len(x[1]), reverse=True)
    residue = 0
    total_cost = 0
    i = 0
    
    while i < len(sequence):
        matched = False
        for symbol, pattern in sorted_rules:
            if sequence[i:i+len(pattern)] == pattern:
                i += len(pattern)
                total_cost += 1
                matched = True
                break
        if not matched:
            residue += 1
            total_cost += 2
            i += 1
            
    return residue, total_cost