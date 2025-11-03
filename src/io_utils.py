import csv

def load_csv(path):
    pairs = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                word = row[0].strip().lower()
                freq = float(row[1])
                pairs.append((word, freq))
    return pairs

def save_csv(path, items):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for word, freq in items:
            writer.writerow([word, freq])