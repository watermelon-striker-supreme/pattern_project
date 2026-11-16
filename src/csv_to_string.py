import csv

def convert_csv_to_string(filepath, max_rows=50000):
    normal_sequence = []
    anomaly_sequence = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        count = 0
        for row in reader:
            if count >= max_rows:
                break
                
            # Create a compact string representation of the row
            row_str = f"{row['proto']}_{row['service']}_{row['state']}_{row['spkts']}_{row['dpkts']}_"
            
            # The UNSW dataset has a 'label' column where 0 = Normal, 1 = Attack
            if row['label'] == '0':
                normal_sequence.append(row_str)
            else:
                anomaly_sequence.append(row_str)
                
            count += 1
            
    return "".join(normal_sequence), "".join(anomaly_sequence)

if __name__ == "__main__":
    train_file = "data/UNSW_NB15_training-set.csv"
    
    normal_str, anomaly_str = convert_csv_to_string(train_file)
    
    print(f"Normal Sequence Length: {len(normal_str)}")
    print(f"Anomaly Sequence Length: {len(anomaly_str)}")
    
    with open("data/normal_traffic.txt", "w") as f:
        f.write(normal_str)
        
    with open("data/anomaly_traffic.txt", "w") as f:
        f.write(anomaly_str)
    
    print("Saved to data/normal_traffic.txt and data/anomaly_traffic.txt")