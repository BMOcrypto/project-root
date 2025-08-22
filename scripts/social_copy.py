# Social copy script
#!/usr/bin/env python3
"""
Generate social media posts for products and blog content
"""

import csv
from datetime import datetime
from pathlib import Path

def generate_social_copy():
    data_dir = Path("data")
    
    # Load products
    products = []
    with open(data_dir / "products.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('status', '').lower() == 'published':
                products.append(row)
    
    # Load posts
    posts = []
    with open(data_dir / "posts.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('status', '').lower() == 'published':
                posts.append(row)
    
    print("=== SOCIAL MEDIA COPY ===")
    print("\n--- PRODUCT PROMOTIONS ---")
    for product in products[:3]:  # Latest 3 products
        message = f"🚀 NEW: {product['title']} - ${product['price']}\n\n"
        message += f"{product['description']}\n\n"
        message += f"👉 Get it here: {product['external_url']}\n\n"
        message += f"#{' #'.join(product['tags'].split(','))}"
        print(message)
        print("\n" + "-"*50 + "\n")
    
    print("\n--- BLOG CONTENT ---")
    for post in posts[:3]:  # Latest 3 posts
        message = f"📖 NEW POST: {post['title']}\n\n"
        message += f"{post['excerpt']}\n\n"
        message += f"👉 Read more: https://yourusername.github.io/blog/{post['title'].lower().replace(' ', '-')}.html\n\n"  # Update with your base URL
        message += f"#{' #'.join(post['tags'].split(',')) if post.get('tags') else ''}"
        print(message)
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    generate_social_copy()