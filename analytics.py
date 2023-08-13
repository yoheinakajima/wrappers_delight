import csv
import matplotlib.pyplot as plt

def calculate_cost(tokens):
    COST_PER_TOKEN = 0.01
    return tokens * COST_PER_TOKEN

def plot_token_usage():
    dates = []
    token_counts = []
    with open("log.csv", "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            dates.append(row[0])
            token_counts.append(int(row[3]))
    
    plt.plot(dates, token_counts)
    plt.xticks(rotation=45)
    plt.ylabel("Tokens")
    plt.xlabel("Timestamp")
    plt.title("Token Usage Over Time")
    plt.tight_layout()
    plt.savefig("token_usage.png")

def plot_model_distribution():
    models = {}
    with open("log.csv", "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            model = row[4]
            models[model] = models.get(model, 0) + 1
            
    plt.pie(models.values(), labels=models.keys(), autopct='%1.1f%%')
    plt.title("Model Usage Distribution")
    plt.savefig("model_distribution.png")

if __name__ == '__main__':
    # This is just for demo purposes, allowing you to run analytics.py directly.
    plot_token_usage()
    plot_model_distribution()
