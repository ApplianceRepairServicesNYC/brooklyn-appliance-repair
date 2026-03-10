#!/usr/bin/env python3
import re
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/brooklyn-appliance-repair')

def remove_faqs(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    original = content
    content = re.sub(r'<h3[^>]*>Frequently Asked Questions[^<]*</h3>\s*(?:<div[^>]*>.*?</div>\s*)*', '', content, flags=re.DOTALL)
    content = re.sub(r'<div style="margin-bottom: 15px; padding: 12px; background: #f8f9fa; border-radius: 6px;">\s*<strong[^>]*>[^<]*\?</strong>\s*<p[^>]*>[^<]*</p>\s*</div>', '', content)
    content = re.sub(r'<div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">\s*<h4[^>]*>[^<]*\?</h4>\s*<p[^>]*>[^<]*</p>\s*</div>', '', content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

html_files = list(BASE_DIR.rglob('index.html'))
count = sum(1 for f in html_files if remove_faqs(f))
print(f"Removed FAQs from {count} pages")
