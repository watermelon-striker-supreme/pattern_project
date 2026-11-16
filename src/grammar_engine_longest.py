import os

def read_fasta(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return "".join([line.strip() for line in lines if not line.startswith(">")])

def find_longest_repeated_substring(sequence, max_len=40):
    best_sub = None
    best_freq = 0
    
    # We search from the longest possible length down to 2
    for length in range(max_len, 1, -1):
        counts = {}
        for i in range(len(sequence) - length + 1):
            sub = sequence[i:i+length]
            if any(char.isdigit() for char in sub):
                continue
            counts[sub] = counts.get(sub, 0) + 1
            
        # Find if any substring of this length repeats
        for sub, freq in counts.items():
            if freq >= 2:
                # If we find a repeat at this length, we take it and stop searching shorter lengths
                return sub, freq
                
    return None, 0

def compress_longest_first(sequence, iterations=50):
    rules = {}
    current_seq = sequence
    
    print(f"--- INITIAL SEQUENCE LENGTH: {len(current_seq)} ---")

    for i in range(iterations):
        best_sub, freq = find_longest_repeated_substring(current_seq, max_len=40)
        
        if not best_sub:
            break

        new_symbol = chr(945 + i) 
        rules[new_symbol] = best_sub
        current_seq = current_seq.replace(best_sub, new_symbol)
        
        print(f"Rule {new_symbol} -> Length {len(best_sub)} (Freq: {freq}) | New Length: {len(current_seq)}")

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

if __name__ == "__main__":
    filepath = "data/phix174.fasta"
    if os.path.exists(filepath):
        raw_seq = read_fasta(filepath)
        rules, compressed = compress_longest_first(raw_seq, iterations=400)
        
        expanded = expand_rules(rules)
        residue, cost = parse_sequence(raw_seq, expanded)
        
        print(f"\n--- RESULTS ---")
        print(f"Total Rules: {len(rules)}")
        print(f"Residue (raw chars): {residue}")
        print(f"Parse Cost: {cost}")
    else:
        print("File not found.")