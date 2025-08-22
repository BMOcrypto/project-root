# Project Root

This is the main README for the project.
# Automated E-Commerce Store

A fully automated, free-to-host e-commerce store built with Python and GitHub Pages.

## Features

- **Automated Builds**: Daily scheduled builds via GitHub Actions
- **Product Management**: CSV-based product catalog with scheduling
- **Blog System**: Content marketing with scheduled posts
- **SEO Optimized**: Sitemap, RSS, and JSON-LD structured data
- **External Monetization**: Links to Gumroad, Payhip, or other platforms

## Setup

1. Fork this repository
2. Enable GitHub Pages in your repository settings
3. Update `data/site.yml` with your information
4. Add your products to `data/products.csv`
5. Add blog content to `data/posts.csv`
6. The site will automatically build and deploy

## Customization

- Modify templates in `site/templates/`
- Update styles in `site/assets/styles.css`
- Add product images to `site/assets/images/`

## Usage

- Set product status to "published" and add a publish_date to control visibility
- Use the social copy generator: `python scripts/social_copy.py`
- Manual build: `python scripts/build.py`

## Monetization

This site supports external monetization through:
- Gumroad product links
- Payhip digital downloads
- Printful integration
- Affiliate marketing links