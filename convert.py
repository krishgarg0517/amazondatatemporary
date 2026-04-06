import csv

with open("products_data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("products_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["Category", "Title", "Price", "URL"])

    for line in lines:
        parts = line.strip().split(" | ")
        writer.writerow(parts)

print("DONE")