import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import json

BASE_URL = "https://books.toscrape.com/catalogue/category/books/"
GBP_TO_INR = 105.50
categories = {
    "Historical Fiction": "historical-fiction_4/index.html",
    "Mystery": "mystery_3/index.html",
    "Science Fiction": "science-fiction_16/index.html"
}

all_books = []

for category, category_path in categories.items():

    print("\n" + "=" * 70)
    print(f"SCRAPING CATEGORY: {category}")
    print("=" * 70)

    current_url = BASE_URL + category_path

    while current_url:
        response = requests.get(current_url)
        print(f"Status: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        print(f"Books on this page: {len(books)}")

        for book in books:

            try:

                title = book.find("h3").find("a")["title"]

                price = book.find("p",class_="price_color").get_text(strip=True)
                # TASK 2
                price = price.replace("Â£", "").replace("£", "").strip()

                # TASK 3
                price_gbp = float(price)
                price_inr = price_gbp * GBP_TO_INR

                rating_text = book.find("p", class_="star-rating")["class"][1]
                # TASK 2
                rating_map = {
                    "One": 1,
                    "Two": 2,
                    "Three": 3,
                    "Four": 4,
                    "Five": 5
                }

                rating = rating_map[rating_text]

                # TASK 2
                availability = book.find("p", class_="instock availability").get_text(strip=True)
                in_stock = "In stock" in availability

                print(f"Category: {category}")
                print(f"Title: {title}")
                print(f"Price (GBP): {price_gbp:.2f}")
                print(f"Price (INR): {price_inr:.2f}")
                print(f"Rating: {rating}")
                print(f"In Stock: {in_stock}")
                print("--" * 35)

                all_books.append({
                    "title": title,
                    "price_gbp": price_gbp,
                    "price_inr": price_inr,
                    "rating": rating,
                    "in_stock": in_stock,
                    "category": category
                })

            except Exception as e:
                print(f"Skipping book due to error: {e}")

        next_page = soup.find("li", class_="next")

        if next_page:
            next_link = next_page.find("a")["href"]
            current_url = (BASE_URL + category_path.rsplit("/", 1)[0] + "/" + next_link)

        else:
            current_url = None
            print(f"No more pages in {category}.")


print("\n" + "=" * 70)
print("SCRAPING COMPLETE")
print("=" * 70)

print(f"Total books stored: {len(all_books)}")

for category in categories:
    count = sum(1 for book in all_books 
                if book["category"] == category
    )
    print(f"{category}: {count}")

# TASK 5 creating JSON
with open("books.json", "w", encoding="utf-8") as file:
    json.dump(
        all_books,
        file,
        indent=4,
        ensure_ascii=False
    )

print("books.json created successfully.")

# TASK 4 Making SQL DATABASE
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS books")
cursor.execute("DROP TABLE IF EXISTS categories")

cursor.execute("""
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id)
    REFERENCES categories(category_id)
)
""")

for category in categories:

    cursor.execute(
        """
        INSERT INTO categories (category_name)
        VALUES (?)
        """,
        (category,)
    )


for book in all_books:

    cursor.execute(
        """
        SELECT category_id
        FROM categories
        WHERE category_name = ?
        """,
        (book["category"],)
    )

    category_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO books
        (
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            book["title"],
            book["price_gbp"],
            book["price_inr"],
            book["rating"],
            int(book["in_stock"]),
            category_id
        )
    )


conn.commit()

categories_table = pd.read_sql_query(
    "SELECT * FROM categories",
    conn
)

books_table = pd.read_sql_query(
    "SELECT * FROM books",
    conn
)

print("\nCategories Table:")
print(categories_table.to_string(index=False))

print("\nBooks Table:")
print(books_table.to_string(index=False))

cursor.execute("SELECT COUNT(*) FROM books")
book_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM categories")
category_count = cursor.fetchone()[0]

print("\n" + "=" * 70)
print("DATABASE")
print("=" * 70)

print(f"Books inserted into SQLite: {book_count}")
print(f"Categories inserted: {category_count}")

#TASK 5 Queries
queries = {
    "query_1": """
SELECT title, price_gbp, rating
FROM books
WHERE rating >= 4
ORDER BY rating DESC
LIMIT 10
""",

    "query_2": """
SELECT title, price_gbp
FROM books
WHERE price_gbp > 40
ORDER BY price_gbp DESC
""",

    "query_3": """
SELECT DISTINCT category_id
FROM books
""",

    "query_4": """
SELECT title, rating, category_id
FROM books
WHERE category_id IN (1, 2)
ORDER BY rating DESC
LIMIT 10
""",

    "query_5": """
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp
""",

    "query_6": """
SELECT
    books.title,
    books.price_gbp,
    books.rating,
    categories.category_name
FROM books
JOIN categories
ON books.category_id = categories.category_id
ORDER BY books.rating DESC
LIMIT 10
"""
}


query_results = {}


for query_name, query in queries.items():

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [description[0] for description in cursor.description]

    output = [
        dict(zip(columns, row))
        for row in rows
    ]

    query_results[query_name] = {"query": query.strip(), "output": output}

    print("\n" + "=" * 70)
    print(query_name.upper())
    print("=" * 70)

    print(query.strip())

    result = pd.DataFrame(rows, columns=columns)
    print(result.to_string(index=False))

with open("sql_query_results.json", "w",encoding="utf-8") as file:

    json.dump(
        query_results,
        file,
        indent=4,
        ensure_ascii=False
    )


print("\n" + "==" * 50)
print("SQL QUERIES COMPLETED")
print("==" * 50)

print("sql_query_results.json created successfully.")

# TASK-6
sql_dataframes = {}

for query_name, query in queries.items():
    df = pd.read_sql(query, conn)
    sql_dataframes[query_name] = df

    print("\n" + "==" * 55)
    print(query_name.upper())
    print("==" * 55)
    print(df.to_string(index=False))

books_df = pd.DataFrame(all_books)

category_names = sorted(set(book["category"] for book in all_books))

categories_df = pd.DataFrame({"category_id": range(1, len(category_names) + 1), "category_name": category_names})

category_map = dict(zip(categories_df["category_name"], categories_df["category_id"]))

books_df["category_id"] = books_df["category"].map(category_map)

merge_result = pd.merge(books_df, categories_df, on="category_id", how="inner")

merge_result = merge_result[["title", "price_gbp", "rating", "category_name"]].sort_values("rating", ascending=False, kind="stable").head(10)

sql_join_result = sql_dataframes["query_6"].copy()

sql_join_result = sql_join_result[["title", "price_gbp", "rating", "category_name"]].sort_values("rating", ascending=False).head(10)

print("\n" + "===" * 55)
print("JOIN RESULT USING PANDAS MERGE")
print("==" * 55)
print(merge_result.to_string(index=False))

print("\n" + "==" * 55)
print("SQL JOIN AND PANDAS MERGE EQUIVALENT")
print("==" * 55)
print(merge_result.reset_index(drop=True).equals(sql_join_result.reset_index(drop=True)))

conn.close()
print("Database connection closed.")