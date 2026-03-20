import csv
import random
import os

def generate_website_traffic_data(filename="data/traffic_data.csv", num_records=100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Header: user_id, session_duration_sec, bounce
    header = ['user_id', 'session_duration_sec', 'bounce']
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        
        for i in range(1, num_records + 1):
            user_id = f"user_{1000 + i}"
            # Variance in sessions: some very short (bounces), some long
            is_bounce = random.random() < 0.2
            if is_bounce:
                duration = random.uniform(1, 15)
            else:
                duration = random.uniform(30, 1200)
            
            writer.writerow([user_id, round(duration, 2), "yes" if is_bounce else "no"])
            
    print(f"Generated {num_records} records in {filename}")

if __name__ == "__main__":
    generate_website_traffic_data()
