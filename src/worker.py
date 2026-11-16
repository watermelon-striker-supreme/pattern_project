import sys
sys.path.append('src')
import os
import json
import random
from grammar_engine_longest import read_fasta, compress_longest_first, expand_rules, parse_sequence

def mutate_sequence(sequence, num_mutations=5):
    seq_list = list(sequence)
    if len(sequence) < 100:
        return "".join(seq_list), []
        
    mutation_indices = []
    num_hotspots = 1 if num_mutations <= 3 else 2
    centers = random.sample(range(len(sequence)), num_hotspots)
    
    for _ in range(num_mutations):
        center = random.choice(centers)
        idx = center + random.randint(-10, 10)
        idx = max(0, min(idx, len(sequence) - 1))
        
        if idx not in mutation_indices:
            mutation_indices.append(idx)
            original = seq_list[idx]
            
            if original in "AT":
                new_char = "G" if original == "A" else "A"
                if random.random() > 0.7:
                    new_char = random.choice([c for c in "CG" if c != original])
            else:
                new_char = "T" if original == "C" else "C"
                if random.random() > 0.7:
                    new_char = random.choice([c for c in "AT" if c != original])
                    
            seq_list[idx] = new_char
            
    return "".join(seq_list), mutation_indices

def sliding_window_parse(sequence, expanded_rules, window_size=200):
    costs = []
    for i in range(0, len(sequence) - window_size + 1, window_size):
        chunk = sequence[i:i+window_size]
        _, cost = parse_sequence(chunk, expanded_rules)
        costs.append(cost)
    return costs

if __name__ == "__main__":
    job_id = int(sys.argv[1])
    random.seed(job_id)
    
    filepath = "data/phix174.fasta"
    if not os.path.exists(filepath):
        sys.exit(1)
        
    raw_seq = read_fasta(filepath)
    
    rules, _ = compress_longest_first(raw_seq, iterations=400)
    expanded_rules = expand_rules(rules)
    
    window_size = 200
    healthy_costs = sliding_window_parse(raw_seq, expanded_rules, window_size)
    
    mutated_seq, mut_indices = mutate_sequence(raw_seq, num_mutations=5)
    mutated_costs = sliding_window_parse(mutated_seq, expanded_rules, window_size)
    
    max_spike = 0
    for h_cost, m_cost in zip(healthy_costs, mutated_costs):
        diff = m_cost - h_cost
        if diff > max_spike:
            max_spike = diff
            
    os.makedirs("mutation_data", exist_ok=True)
    result = {
        "job_id": job_id,
        "max_spike": max_spike,
        "mutations": len(mut_indices)
    }
    
    with open(f"mutation_data/result_{job_id}.json", "w") as f:
        json.dump(result, f)