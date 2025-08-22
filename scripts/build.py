# Build script
#!/usr/bin/env python3
"""
Static site generator for automated e-commerce store
Uses only Python stdlib + PyYAML
"""

import csv
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
import yaml
from xml.etree import ElementTree as ET

class SiteBuilder:
    def __init__(self):
        self.data_dir = Path("data")
        self.template_dir = Path("site/templates")
        self.assets_dir = Path("site/assets")
        self.output_dir = Path("_site")
        self.site_config = {}
        self.products = []
        self.posts = []
        
    def load_config(self):
        """Load site configuration from YAML"""
        with open(self.data_dir / "site.yml", "r") as f:
            self.site_config = yaml.safe_load(f)
    
    def load_products(self):
        """Load and filter products based on status and date"""
        with open(self.data_dir / "products.csv", "r") as f:
            reader = csv.DictReader(f)
            today = datetime.now().date()
            
            for row in reader:
                # Check if product should be published
                if row.get('status', '').lower() != 'published':
                    continue
                    
                # Check publish date if exists
                if row.get('publish_date'):
                    try:
                        publish_date = datetime.strptime(row['publish_date'], '%Y-%m-%d').date()
                        if publish_date > today:
                            continue
                    except ValueError:
                        pass
                
                self.products.append(row)
        
        # Sort by date if available, newest first
        self.products.sort(key=lambda x: x.get('publish_date', ''), reverse=True)
    
    def load_posts(self):
        """Load and filter blog posts based on status and date"""
        with open(self.data_dir / "posts.csv", "r") as f:
            reader = csv.DictReader(f)
            today = datetime.now().date()
            
            for row in reader:
                # Check if post should be published
                if row.get('status', '').lower() != 'published':
                    continue
                    
                # Check publish date if exists
                if row.get('publish_date'):
                    try:
                        publish_date = datetime.strptime(row['publish_date'], '%Y-%m-%d').date()
                        if publish_date > today:
                            continue
                    except ValueError:
                        pass
                
                self.posts.append(row)
        
        # Sort by date, newest first
        self.posts.sort(key=lambda x: x.get('publish_date', ''), reverse=True)
    
    def render_template(self, template_name, context):
        """Simple template rendering with variable replacement"""
        with open(self.template_dir / template_name, "r") as f:
            content = f.read()
        
        # Add site config to context
        context.update(self.site_config)
        
        # Replace variables in template
        for key, value in context.items():
            placeholder = "{{ " + key + " }}"
            content = content.replace(placeholder, str(value))
        
        return content
    
    def generate_pages(self):
        """Generate all HTML pages"""
        # Create output directories
        (self.output_dir / "products").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "blog").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "assets").mkdir(parents=True, exist_ok=True)
        
        # Home page
        context = {
            "featured_products": self.products[:4],
            "recent_posts": self.posts[:3]
        }
        home_html = self.render_template("index.html", context)
        with open(self.output_dir / "index.html", "w") as f:
            f.write(home_html)
        
        # Products index
        context = {"products": self.products}
        products_html = self.render_template("products_index.html", context)
        with open(self.output_dir / "products/index.html", "w") as f:
            f.write(products_html)
        
        # Individual product pages
        for product in self.products:
            context = {"product": product}
            product_html = self.render_template("product.html", context)
            product_slug = re.sub(r'[^a-z0-9]+', '-', product['title'].lower()).strip('-')
            with open(self.output_dir / f"products/{product_slug}.html", "w") as f:
                f.write(product_html)
        
        # Blog index
        context = {"posts": self.posts}
        blog_html = self.render_template("blog_index.html", context)
        with open(self.output_dir / "blog/index.html", "w") as f:
            f.write(blog_html)
        
        # Individual post pages
        for post in self.posts:
            context = {"post": post}
            post_html = self.render_template("post.html", context)
            post_slug = re.sub(r'[^a-z0-9]+', '-', post['title'].lower()).strip('-')
            with open(self.output_dir / f"blog/{post_slug}.html", "w") as f:
                f.write(post_html)
    
    def generate_sitemap(self):
        """Generate sitemap.xml for SEO"""
        urlset = ET.Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        
        # Home page
        self.add_sitemap_url(urlset, self.site_config['base_url'], "1.0", "daily")
        
        # Product pages
        for product in self.products:
            product_slug = re.sub(r'[^a-z0-9]+', '-', product['title'].lower()).strip('-')
            product_url = f"{self.site_config['base_url']}/products/{product_slug}.html"
            self.add_sitemap_url(urlset, product_url, "0.8", "weekly")
        
        # Blog posts
        for post in self.posts:
            post_slug = re.sub(r'[^a-z0-9]+', '-', post['title'].lower()).strip('-')
            post_url = f"{self.site_config['base_url']}/blog/{post_slug}.html"
            self.add_sitemap_url(urlset, post_url, "0.7", "monthly")
        
        # Write sitemap
        tree = ET.ElementTree(urlset)
        tree.write(self.output_dir / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    
    def add_sitemap_url(self, urlset, loc, priority, changefreq):
        """Add a URL to the sitemap"""
        url_elem = ET.SubElement(urlset, "url")
        ET.SubElement(url_elem, "loc").text = loc
        ET.SubElement(url_elem, "priority").text = priority
        ET.SubElement(url_elem, "changefreq").text = changefreq
        ET.SubElement(url_elem, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    
    def generate_rss(self):
        """Generate RSS feed for blog"""
        rss = ET.Element("rss")
        rss.set("version", "2.0")
        
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title").text = self.site_config.get('title', '')
        ET.SubElement(channel, "description").text = self.site_config.get('description', '')
        ET.SubElement(channel, "link").text = self.site_config['base_url']
        
        for post in self.posts[:10]:  # Latest 10 posts
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = post['title']
            ET.SubElement(item, "description").text = post.get('excerpt', '')
            post_slug = re.sub(r'[^a-z0-9]+', '-', post['title'].lower()).strip('-')
            ET.SubElement(item, "link").text = f"{self.site_config['base_url']}/blog/{post_slug}.html"
            ET.SubElement(item, "pubDate").text = post.get('publish_date', '')
        
        tree = ET.ElementTree(rss)
        tree.write(self.output_dir / "rss.xml", encoding="utf-8", xml_declaration=True)
    
    def copy_assets(self):
        """Copy CSS and other assets to output directory"""
        if self.assets_dir.exists():
            shutil.copytree(self.assets_dir, self.output_dir / "assets", dirs_exist_ok=True)
    
    def build(self):
        """Main build method"""
        print("Starting build process...")
        
        # Clean output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir()
        
        # Load data
        self.load_config()
        self.load_products()
        self.load_posts()
        
        # Generate site
        self.generate_pages()
        self.generate_sitemap()
        self.generate_rss()
        self.copy_assets()
        
        print(f"Build complete! Generated {len(self.products)} products and {len(self.posts)} posts.")

if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()