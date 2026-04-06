from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime

# 🔹 start browser
driver = webdriver.Chrome()

# 🔹 load last saved prices
last_prices = {}

try:
    with open("price_history.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            try:
                date, category, title, price, url = row

                # 🔥 clean + convert to int
                clean_price = int(str(price).replace("₹", "").replace(",", "").strip())

                last_prices[url] = clean_price
            except:
                continue
except:
    pass

# 🔹 load products
with open("products_data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    products = list(reader)

# 🔹 open output file
with open("price_history.csv", "a", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)

    # header
    if out.tell() == 0:
        writer.writerow(["Date", "Category", "Title", "Price", "URL"])

    for i, row in enumerate(products):
        try:
            category, title, old_price, url = row

            print(f"{i+1}/{len(products)} → Checking:", title)

            driver.get(url)
            time.sleep(1)

            try:
                price_text = driver.find_element(By.CLASS_NAME, "a-price-whole").text
                price_text = price_text.replace(",", "").strip()
                new_price = int(price_text)
            except:
                print("Price not found")
                continue

            old_saved_price = last_prices.get(url, -1)

            # 🔥 FINAL LOGIC (NO DUPLICATE GUARANTEE)
            if old_saved_price == -1:
                # first time entry
                date = datetime.now().strftime("%Y-%m-%d %H:%M")
                writer.writerow([date, category, title, new_price, url])
                last_prices[url] = new_price
                print("FIRST SAVE:", title, new_price)

            elif new_price != old_saved_price:
                # price changed
                date = datetime.now().strftime("%Y-%m-%d %H:%M")
                writer.writerow([date, category, title, new_price, url])
                last_prices[url] = new_price
                print("UPDATED:", title, new_price)

            else:
                # no change
                print("NO CHANGE:", title)

        except:
            continue

driver.quit()

print("✅ DONE — No duplicate data!")