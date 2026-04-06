from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

categories = {
     "grocery": 25,
    "shoes": 25,
    "earphones": 25,
    "sunglasses": 25,
    "laptops": 25,
    "watches": 25,
    "bags": 25,
    "headphones": 25
    
}

with open("products_data.txt", "w", encoding="utf-8") as f:

    for category, count in categories.items():
        print(f"Extracting {category}...")

        driver.get(f"https://www.amazon.in/s?k={category}")
        time.sleep(3)

        items = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

        collected = 0

        for item in items:
            try:
                title = item.find_element(By.TAG_NAME, "h2").text
                link = item.find_element(By.TAG_NAME, "a").get_attribute("href")

                if "/dp/" in link:
                    link = link.split("/ref=")[0]

                try:
                    price = item.find_element(By.CLASS_NAME, "a-price-whole").text
                except:
                    price = "N/A"

                f.write(f"{category} | {title} | ₹{price} | {link}\n")

                print(title, price)

                collected += 1

            except:
                continue

            if collected >= count:
                break

driver.quit()

print("✅ Done! Data saved.")