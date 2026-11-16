import os

def read_fasta(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return "".join([line.strip() for line in lines if not line.startswith(">")])

def find_best_substring(sequence, max_len=5):
    counts = {}
    for length in range(2, max_len + 1):
        for i in range(len(sequence) - length + 1):
            sub = sequence[i:i+length]
            if any(char.isdigit() for char in sub):
                continue
            counts[sub] = counts.get(sub, 0) + 1
            
    best_sub = None
    best_freq = 0
    best_savings = 0

    for sub, freq in counts.items():
        if freq < 2:
            continue
        savings = (len(sub) - 1) * freq - len(sub) - 1
        if savings > best_savings:
            best_savings = savings
            best_sub = sub
            best_freq = freq

    return best_sub, best_freq

def compress_sequence(sequence, iterations=100):
    rules = {}
    current_seq = sequence
    for i in range(iterations):
        best_sub, freq = find_best_substring(current_seq, max_len=5)
        if not best_sub or freq < 2:
            break
        new_symbol = chr(945 + i) 
        rules[new_symbol] = best_sub
        current_seq = current_seq.replace(best_sub, new_symbol)
    return rules, current_seq

def apply_existing_grammar(sequence, rules):
    current_seq = sequence
    for symbol, pattern in rules.items():
        current_seq = current_seq.replace(pattern, symbol)
    return current_seq

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

def sliding_window_parse(sequence, expanded_rules, window_size=200):
    costs = []
    for i in range(0, len(sequence) - window_size + 1, window_size):
        chunk = sequence[i:i+window_size]
        _, cost = parse_sequence(chunk, expanded_rules)
        costs.append(cost)
    return costs