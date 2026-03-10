#!/usr/bin/env python3
"""
Add contextual internal links to all pages for better SEO link building.
Similar to wolf-bergen-county's approach.
"""

import re
import hashlib
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/brooklyn-appliance-repair')
SITE_URL = 'https://brooklynappliancerepairservice.com'

# Brooklyn neighborhoods with nearby neighborhoods
NEIGHBORHOODS = {
    'bath-beach': {'name': 'Bath Beach', 'nearby': ['bensonhurst', 'gravesend', 'coney-island']},
    'bay-ridge': {'name': 'Bay Ridge', 'nearby': ['dyker-heights', 'sunset-park', 'fort-greene']},
    'bedford-stuyvesant': {'name': 'Bedford-Stuyvesant', 'nearby': ['crown-heights', 'bushwick', 'clinton-hill']},
    'bensonhurst': {'name': 'Bensonhurst', 'nearby': ['bath-beach', 'gravesend', 'borough-park']},
    'boerum-hill': {'name': 'Boerum Hill', 'nearby': ['cobble-hill', 'downtown-brooklyn', 'carroll-gardens']},
    'borough-park': {'name': 'Borough Park', 'nearby': ['bensonhurst', 'kensington', 'sunset-park']},
    'brighton-beach': {'name': 'Brighton Beach', 'nearby': ['coney-island', 'sheepshead-bay', 'manhattan-beach']},
    'brooklyn-heights': {'name': 'Brooklyn Heights', 'nearby': ['dumbo', 'downtown-brooklyn', 'cobble-hill']},
    'brownsville': {'name': 'Brownsville', 'nearby': ['east-new-york', 'ocean-hill', 'canarsie']},
    'bushwick': {'name': 'Bushwick', 'nearby': ['williamsburg', 'bedford-stuyvesant', 'ridgewood']},
    'canarsie': {'name': 'Canarsie', 'nearby': ['east-flatbush', 'flatlands', 'brownsville']},
    'carroll-gardens': {'name': 'Carroll Gardens', 'nearby': ['cobble-hill', 'red-hook', 'gowanus']},
    'city-line': {'name': 'City Line', 'nearby': ['east-new-york', 'cypress-hills', 'brownsville']},
    'clinton-hill': {'name': 'Clinton Hill', 'nearby': ['fort-greene', 'bedford-stuyvesant', 'prospect-heights']},
    'cobble-hill': {'name': 'Cobble Hill', 'nearby': ['carroll-gardens', 'boerum-hill', 'brooklyn-heights']},
    'columbia-street-waterfront-district': {'name': 'Columbia Street Waterfront', 'nearby': ['red-hook', 'carroll-gardens', 'cobble-hill']},
    'coney-island': {'name': 'Coney Island', 'nearby': ['brighton-beach', 'sea-gate', 'gravesend']},
    'crown-heights': {'name': 'Crown Heights', 'nearby': ['prospect-lefferts-gardens', 'bedford-stuyvesant', 'prospect-heights']},
    'cypress-hills': {'name': 'Cypress Hills', 'nearby': ['east-new-york', 'city-line', 'highland-park']},
    'ditmas-park': {'name': 'Ditmas Park', 'nearby': ['flatbush', 'midwood', 'kensington']},
    'downtown-brooklyn': {'name': 'Downtown Brooklyn', 'nearby': ['brooklyn-heights', 'boerum-hill', 'fort-greene']},
    'dumbo': {'name': 'DUMBO', 'nearby': ['brooklyn-heights', 'vinegar-hill', 'downtown-brooklyn']},
    'dyker-heights': {'name': 'Dyker Heights', 'nearby': ['bay-ridge', 'bensonhurst', 'borough-park']},
    'east-flatbush': {'name': 'East Flatbush', 'nearby': ['flatbush', 'canarsie', 'brownsville']},
    'east-new-york': {'name': 'East New York', 'nearby': ['brownsville', 'cypress-hills', 'city-line']},
    'farragut': {'name': 'Farragut', 'nearby': ['flatbush', 'east-flatbush', 'flatlands']},
    'fiske-terrace': {'name': 'Fiske Terrace', 'nearby': ['midwood', 'flatbush', 'ditmas-park']},
    'flatbush': {'name': 'Flatbush', 'nearby': ['ditmas-park', 'east-flatbush', 'midwood']},
    'flatlands': {'name': 'Flatlands', 'nearby': ['canarsie', 'mill-basin', 'marine-park']},
    'fort-greene': {'name': 'Fort Greene', 'nearby': ['clinton-hill', 'downtown-brooklyn', 'prospect-heights']},
    'georgetown': {'name': 'Georgetown', 'nearby': ['flatlands', 'canarsie', 'mill-basin']},
    'gerritsen-beach': {'name': 'Gerritsen Beach', 'nearby': ['marine-park', 'sheepshead-bay', 'mill-basin']},
    'gowanus': {'name': 'Gowanus', 'nearby': ['park-slope', 'carroll-gardens', 'red-hook']},
    'gravesend': {'name': 'Gravesend', 'nearby': ['bensonhurst', 'coney-island', 'sheepshead-bay']},
    'greenpoint': {'name': 'Greenpoint', 'nearby': ['williamsburg', 'bushwick', 'dumbo']},
    'greenwood-heights': {'name': 'Greenwood Heights', 'nearby': ['sunset-park', 'park-slope', 'south-slope']},
    'highland-park': {'name': 'Highland Park', 'nearby': ['cypress-hills', 'east-new-york', 'bushwick']},
    'homecrest': {'name': 'Homecrest', 'nearby': ['sheepshead-bay', 'gravesend', 'midwood']},
    'kensington': {'name': 'Kensington', 'nearby': ['borough-park', 'ditmas-park', 'windsor-terrace']},
    'marine-park': {'name': 'Marine Park', 'nearby': ['mill-basin', 'flatlands', 'gerritsen-beach']},
    'midwood': {'name': 'Midwood', 'nearby': ['flatbush', 'ditmas-park', 'homecrest']},
    'mill-basin': {'name': 'Mill Basin', 'nearby': ['marine-park', 'flatlands', 'canarsie']},
    'navy-yard': {'name': 'Navy Yard', 'nearby': ['vinegar-hill', 'fort-greene', 'clinton-hill']},
    'ocean-hill': {'name': 'Ocean Hill', 'nearby': ['brownsville', 'bedford-stuyvesant', 'bushwick']},
    'ocean-parkway': {'name': 'Ocean Parkway', 'nearby': ['kensington', 'midwood', 'borough-park']},
    'paerdegat-basin': {'name': 'Paerdegat Basin', 'nearby': ['canarsie', 'flatlands', 'east-flatbush']},
    'park-slope': {'name': 'Park Slope', 'nearby': ['prospect-heights', 'gowanus', 'south-slope']},
    'plum-beach': {'name': 'Plum Beach', 'nearby': ['sheepshead-bay', 'gerritsen-beach', 'marine-park']},
    'prospect-heights': {'name': 'Prospect Heights', 'nearby': ['park-slope', 'crown-heights', 'fort-greene']},
    'prospect-lefferts-gardens': {'name': 'Prospect Lefferts Gardens', 'nearby': ['crown-heights', 'flatbush', 'east-flatbush']},
    'prospect-park-south': {'name': 'Prospect Park South', 'nearby': ['flatbush', 'ditmas-park', 'kensington']},
    'red-hook': {'name': 'Red Hook', 'nearby': ['carroll-gardens', 'gowanus', 'columbia-street-waterfront-district']},
    'remsen-village': {'name': 'Remsen Village', 'nearby': ['canarsie', 'east-flatbush', 'brownsville']},
    'rugby': {'name': 'Rugby', 'nearby': ['east-flatbush', 'flatbush', 'remsen-village']},
    'sea-gate': {'name': 'Sea Gate', 'nearby': ['coney-island', 'brighton-beach', 'gravesend']},
    'sheepshead-bay': {'name': 'Sheepshead Bay', 'nearby': ['gravesend', 'homecrest', 'marine-park']},
    'south-slope': {'name': 'South Slope', 'nearby': ['park-slope', 'greenwood-heights', 'windsor-terrace']},
    'starrett-city': {'name': 'Starrett City', 'nearby': ['canarsie', 'east-new-york', 'flatlands']},
    'stuyvesant-heights': {'name': 'Stuyvesant Heights', 'nearby': ['bedford-stuyvesant', 'ocean-hill', 'crown-heights']},
    'sunset-park': {'name': 'Sunset Park', 'nearby': ['bay-ridge', 'greenwood-heights', 'borough-park']},
    'vinegar-hill': {'name': 'Vinegar Hill', 'nearby': ['dumbo', 'navy-yard', 'brooklyn-heights']},
    'weeksville': {'name': 'Weeksville', 'nearby': ['crown-heights', 'bedford-stuyvesant', 'brownsville']},
    'williamsburg': {'name': 'Williamsburg', 'nearby': ['greenpoint', 'bushwick', 'bedford-stuyvesant']},
    'windsor-terrace': {'name': 'Windsor Terrace', 'nearby': ['kensington', 'park-slope', 'south-slope']},
    'wingate': {'name': 'Wingate', 'nearby': ['east-flatbush', 'crown-heights', 'prospect-lefferts-gardens']},
}

# Appliance types for cross-linking
APPLIANCES = [
    ('refrigerator-repair', 'refrigerator repair'),
    ('washer-repair', 'washer repair'),
    ('dryer-repair', 'dryer repair'),
    ('dishwasher-repair', 'dishwasher repair'),
    ('oven-repair', 'oven repair'),
    ('cooktop-repair', 'cooktop repair'),
]

# Major brands for cross-linking
BRANDS = [
    ('lg', 'LG'),
    ('samsung', 'Samsung'),
    ('whirlpool', 'Whirlpool'),
    ('ge', 'GE'),
    ('bosch', 'Bosch'),
    ('kitchenaid', 'KitchenAid'),
    ('frigidaire', 'Frigidaire'),
    ('maytag', 'Maytag'),
]

def get_hash_index(text, num_options):
    """Get deterministic index based on hash."""
    return int(hashlib.md5(text.encode()).hexdigest(), 16) % num_options


def add_neighborhood_links(content, neighborhood_slug):
    """Add contextual links to a neighborhood page."""
    if neighborhood_slug not in NEIGHBORHOODS:
        return content, False

    info = NEIGHBORHOODS[neighborhood_slug]
    name = info['name']
    nearby = info['nearby']

    # Filter to only existing nearby neighborhoods
    valid_nearby = [n for n in nearby if n in NEIGHBORHOODS]
    if not valid_nearby:
        return content, False

    # Pick 2 nearby neighborhoods based on hash
    idx1 = get_hash_index(neighborhood_slug + "1", len(valid_nearby))
    idx2 = get_hash_index(neighborhood_slug + "2", len(valid_nearby))
    if idx2 == idx1:
        idx2 = (idx1 + 1) % len(valid_nearby)

    nearby1 = valid_nearby[idx1]
    nearby2 = valid_nearby[idx2]
    nearby1_name = NEIGHBORHOODS[nearby1]['name']
    nearby2_name = NEIGHBORHOODS[nearby2]['name']

    # Pick an appliance and brand
    app_idx = get_hash_index(neighborhood_slug + "app", len(APPLIANCES))
    brand_idx = get_hash_index(neighborhood_slug + "brand", len(BRANDS))
    appliance_slug, appliance_name = APPLIANCES[app_idx]
    brand_slug, brand_name = BRANDS[brand_idx]

    # Build the links paragraph
    links_html = f'''
            <p style="font-size: 17px; line-height: 1.7; margin-bottom: 20px;">We proudly serve {name} and neighboring areas including <a href="{SITE_URL}/brooklyn/{nearby1}/">{nearby1_name}</a> and <a href="{SITE_URL}/brooklyn/{nearby2}/">{nearby2_name}</a>. Our technicians are experts in <a href="{SITE_URL}/appliances/{appliance_slug}/">{appliance_name}</a> and all <a href="{SITE_URL}/brands/{brand_slug}/">{brand_name} appliances</a>.</p>
'''

    # Find the unique content section and add links before the closing </div>
    pattern = r'(<!-- UNIQUE CONTENT FOR [^>]+ -->.*?<div style="max-width: \d+px; margin: 0 auto;">)(.*?)(</div>\s*</section>\s*<!-- END UNIQUE CONTENT -->)'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        # Check if links already added
        if 'proudly serve' in match.group(2) and '/brooklyn/' in match.group(2):
            return content, False

        new_content = match.group(1) + match.group(2) + links_html + match.group(3)
        content = content[:match.start()] + new_content + content[match.end():]
        return content, True

    return content, False


def add_brand_links(content, brand_slug):
    """Add contextual links to a brand page."""
    # Pick 2 random neighborhoods
    neighborhood_list = list(NEIGHBORHOODS.keys())
    idx1 = get_hash_index(brand_slug + "n1", len(neighborhood_list))
    idx2 = get_hash_index(brand_slug + "n2", len(neighborhood_list))
    if idx2 == idx1:
        idx2 = (idx1 + 1) % len(neighborhood_list)

    n1 = neighborhood_list[idx1]
    n2 = neighborhood_list[idx2]
    n1_name = NEIGHBORHOODS[n1]['name']
    n2_name = NEIGHBORHOODS[n2]['name']

    # Pick an appliance
    app_idx = get_hash_index(brand_slug + "app", len(APPLIANCES))
    appliance_slug, appliance_name = APPLIANCES[app_idx]

    # Get brand name
    brand_name = brand_slug.upper()
    for b_slug, b_name in BRANDS:
        if b_slug == brand_slug:
            brand_name = b_name
            break

    links_html = f'''
            <p style="font-size: 17px; line-height: 1.7; margin-bottom: 20px;">Our {brand_name} repair services cover all Brooklyn neighborhoods including <a href="{SITE_URL}/brooklyn/{n1}/">{n1_name}</a> and <a href="{SITE_URL}/brooklyn/{n2}/">{n2_name}</a>. We specialize in <a href="{SITE_URL}/appliances/{appliance_slug}/">{appliance_name}</a> for {brand_name} and all major brands.</p>
'''

    pattern = r'(<!-- UNIQUE CONTENT FOR [^>]+ -->.*?<div style="max-width: \d+px; margin: 0 auto;">)(.*?)(</div>\s*</section>\s*<!-- END UNIQUE CONTENT -->)'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        if 'repair services cover' in match.group(2):
            return content, False

        new_content = match.group(1) + match.group(2) + links_html + match.group(3)
        content = content[:match.start()] + new_content + content[match.end():]
        return content, True

    return content, False


def add_appliance_links(content, appliance_slug):
    """Add contextual links to an appliance page."""
    # Pick 2 random neighborhoods
    neighborhood_list = list(NEIGHBORHOODS.keys())
    idx1 = get_hash_index(appliance_slug + "n1", len(neighborhood_list))
    idx2 = get_hash_index(appliance_slug + "n2", len(neighborhood_list))
    if idx2 == idx1:
        idx2 = (idx1 + 1) % len(neighborhood_list)

    n1 = neighborhood_list[idx1]
    n2 = neighborhood_list[idx2]
    n1_name = NEIGHBORHOODS[n1]['name']
    n2_name = NEIGHBORHOODS[n2]['name']

    # Pick 2 brands
    brand_idx1 = get_hash_index(appliance_slug + "b1", len(BRANDS))
    brand_idx2 = get_hash_index(appliance_slug + "b2", len(BRANDS))
    if brand_idx2 == brand_idx1:
        brand_idx2 = (brand_idx1 + 1) % len(BRANDS)

    brand1_slug, brand1_name = BRANDS[brand_idx1]
    brand2_slug, brand2_name = BRANDS[brand_idx2]

    # Get appliance name
    appliance_name = appliance_slug.replace('-', ' ').title()

    links_html = f'''
            <p style="font-size: 17px; line-height: 1.7; margin-bottom: 20px;">Our {appliance_name.lower()} services are available throughout Brooklyn including <a href="{SITE_URL}/brooklyn/{n1}/">{n1_name}</a> and <a href="{SITE_URL}/brooklyn/{n2}/">{n2_name}</a>. We repair all major brands including <a href="{SITE_URL}/brands/{brand1_slug}/">{brand1_name}</a> and <a href="{SITE_URL}/brands/{brand2_slug}/">{brand2_name}</a>.</p>
'''

    pattern = r'(<!-- UNIQUE CONTENT FOR [^>]+ -->.*?<div style="max-width: \d+px; margin: 0 auto;">)(.*?)(</div>\s*</section>\s*<!-- END UNIQUE CONTENT -->)'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        if 'services are available throughout' in match.group(2):
            return content, False

        new_content = match.group(1) + match.group(2) + links_html + match.group(3)
        content = content[:match.start()] + new_content + content[match.end():]
        return content, True

    return content, False


def process_file(file_path):
    """Process a single file and add appropriate links."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Skip if no unique content section
    if '<!-- UNIQUE CONTENT FOR' not in content:
        return False

    rel_path = file_path.relative_to(BASE_DIR)
    parts = list(rel_path.parts)

    modified = False

    # Neighborhood page: /brooklyn/{neighborhood}/index.html
    if len(parts) >= 2 and parts[0] == 'brooklyn' and parts[-1] == 'index.html':
        neighborhood_slug = parts[1]
        content, modified = add_neighborhood_links(content, neighborhood_slug)

    # Brand page: /brands/{brand}/index.html
    elif len(parts) >= 2 and parts[0] == 'brands' and parts[-1] == 'index.html':
        brand_slug = parts[1]
        content, modified = add_brand_links(content, brand_slug)

    # Appliance page: /appliances/{appliance}/index.html
    elif len(parts) >= 2 and parts[0] == 'appliances' and parts[-1] == 'index.html':
        appliance_slug = parts[1]
        content, modified = add_appliance_links(content, appliance_slug)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    html_files = list(BASE_DIR.rglob('index.html'))
    print(f"Found {len(html_files)} total pages")

    count = 0
    for f in html_files:
        if 'assets' in str(f) or 'sitemap' in str(f):
            continue
        if process_file(f):
            count += 1

    print(f"Added internal links to {count} pages")


if __name__ == "__main__":
    main()
