#!/usr/bin/env python3
"""
Add unique content to ALL Brooklyn pages sitewide.
"""

import re
import hashlib
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/brooklyn-appliance-repair')

LOCATION_INTROS = [
    "As a cornerstone of {location}'s community, we've built our reputation on reliable service.",
    "{location} is known for its unique character - our technicians know the neighborhood well.",
    "From {location}'s historic homes to modern buildings, we service every appliance setup.",
    "Our {location} customers appreciate straightforward pricing and same-day availability.",
    "{location} families trust us because we treat every home with care and respect.",
    "We're proud to serve {location}'s diverse community with expert repair at fair prices.",
    "Whether you're in a {location} brownstone or high-rise, we arrive prepared.",
    "{location}'s busy households need working appliances - we make sure they do.",
    "Our deep roots in {location} mean we understand local residents' needs.",
    "Fast, friendly service has made us {location}'s go-to repair choice.",
]

SERVICE_INTROS = {
    "washer": [
        "Washer repair in {location} - front load, top load, stackable units all serviced.",
        "Our {location} washer technicians fix spinning, draining, and startup issues.",
        "{location} washer repair with genuine parts for lasting results.",
    ],
    "dryer": [
        "Dryer repair in {location} - heating, drum, and electrical problems solved.",
        "Gas and electric dryer repair serving {location} residents same-day.",
        "Don't let laundry pile up - {location} dryer repair available today.",
    ],
    "refrigerator": [
        "Refrigerator repair in {location} - cooling, ice maker, compressor service.",
        "Our {location} fridge experts handle all brands including premium models.",
        "Fast {location} refrigerator repair - same-day appointments available.",
    ],
    "dishwasher": [
        "Dishwasher repair in {location} - leaks, drainage, cleaning issues fixed.",
        "Our {location} dishwasher technicians repair all brands affordably.",
        "{location} dishwasher not cleaning? Same-day diagnosis and repair.",
    ],
    "oven": [
        "Oven repair in {location} - heating elements, igniters, controls fixed.",
        "Gas, electric, convection oven repair serving {location}.",
        "{location} oven problems solved quickly by certified technicians.",
    ],
    "cooktop": [
        "Cooktop repair in {location} - burners, igniters, elements serviced.",
        "Gas, electric, induction cooktop repair for {location} homes.",
        "{location} cooktop not heating? Fast, reliable repair available.",
    ],
    "microwave": [
        "Microwave repair in {location} - magnetrons, turntables, controls fixed.",
        "Built-in and countertop microwave repair serving {location}.",
        "{location} microwave issues? Affordable same-day repair.",
    ],
    "default": [
        "Professional appliance repair in {location} - all brands serviced.",
        "Our {location} technicians carry parts for same-day repairs.",
        "Trusted appliance repair serving {location} with reliability.",
    ],
}

BRAND_INTROS = {
    "lg": "LG appliances feature ThinQ smart technology and TurboWash systems. Our certified technicians understand LG's advanced features.",
    "samsung": "Samsung appliances combine innovation with reliability. We're experts in Samsung's smart features and Family Hub systems.",
    "whirlpool": "Whirlpool is a trusted American brand. Our technicians quickly diagnose and repair all Whirlpool models.",
    "ge": "GE appliances are found in homes everywhere. We service all GE lines including Profile and Cafe.",
    "frigidaire": "Frigidaire offers dependable appliances. Our technicians handle all Frigidaire repair needs.",
    "maytag": "Maytag is built for durability. We repair all Maytag appliances with genuine parts.",
    "kitchenaid": "KitchenAid blends professional performance with home convenience. We handle KitchenAid's premium features.",
    "bosch": "Bosch German engineering demands precision repair. Our technicians service Bosch's efficient designs.",
    "thermador": "Thermador luxury appliances require expert care. We're certified for Thermador repairs.",
    "sub-zero": "Sub-Zero refrigeration represents the best. Our specialists service Sub-Zero's dual systems.",
    "wolf": "Wolf professional cooking needs expert service. We repair Wolf to factory specs.",
    "viking": "Viking professional appliances bring restaurant quality home. We're Viking repair experts.",
    "miele": "Miele German engineering ensures longevity. We service all Miele appliances with care.",
    "default": "We service all major brands with factory-trained expertise and genuine parts.",
}

FAQ_TEMPLATES = [
    [
        ("How fast can you reach {location}?", "Our Brooklyn technicians reach {location} within 1-2 hours."),
        ("Is there a trip charge for {location}?", "Our flat diagnostic fee covers all of Brooklyn including {location}."),
    ],
    [
        ("Are you licensed for {location}?", "Yes - licensed, insured, and background-checked for {location}."),
        ("Weekend service in {location}?", "Yes - 7 days a week for {location} residents."),
    ],
    [
        ("What warranty for {location} repairs?", "90-day parts and labor warranty on all {location} work."),
        ("Do you fix luxury brands in {location}?", "Yes - certified for high-end brands in {location} homes."),
    ],
    [
        ("Same-day repair in {location}?", "Yes! Most {location} repairs completed same-day."),
        ("Payment options?", "Credit cards, cash, checks accepted for {location} service."),
    ],
]

def get_hash_index(text, num_options):
    return int(hashlib.md5(text.encode()).hexdigest(), 16) % num_options

def format_name(slug):
    return slug.replace("-", " ").title()

def get_service_type(slug):
    if "washer" in slug: return "washer"
    if "dryer" in slug: return "dryer"
    if "refrigerator" in slug: return "refrigerator"
    if "dishwasher" in slug: return "dishwasher"
    if "oven" in slug: return "oven"
    if "cooktop" in slug: return "cooktop"
    if "microwave" in slug: return "microwave"
    return "default"

def generate_content(page_type, location=None, service=None, brand=None):
    if page_type == "location":
        idx = get_hash_index(location, len(LOCATION_INTROS))
        intro = LOCATION_INTROS[idx].format(location=location)
        faq_idx = get_hash_index(location + "faq", len(FAQ_TEMPLATES))
        faqs = FAQ_TEMPLATES[faq_idx]

    elif page_type == "location_service":
        svc_type = get_service_type(service)
        svc_intros = SERVICE_INTROS.get(svc_type, SERVICE_INTROS["default"])
        idx = get_hash_index(location + service, len(svc_intros))
        intro = svc_intros[idx].format(location=location)
        faq_idx = get_hash_index(location + service, len(FAQ_TEMPLATES))
        faqs = FAQ_TEMPLATES[faq_idx]

    elif page_type == "brand":
        brand_key = brand.lower().replace(" ", "-")
        intro = BRAND_INTROS.get(brand_key, BRAND_INTROS["default"])
        faqs = []

    else:
        return None

    faq_html = ""
    for q, a in faqs:
        q_fmt = q.format(location=location) if location else q
        a_fmt = a.format(location=location) if location else a
        faq_html += f'''
        <div style="margin-bottom: 15px; padding: 12px; background: #f8f9fa; border-radius: 6px;">
            <strong style="color: var(--blue);">{q_fmt}</strong>
            <p style="margin: 8px 0 0 0; color: #555;">{a_fmt}</p>
        </div>'''

    title = location or brand or "Service"
    section = f'''
    <!-- UNIQUE CONTENT FOR {title.upper()} -->
    <section style="padding: 30px 20px; background: #fff;">
        <div style="max-width: 800px; margin: 0 auto;">
            <p style="font-size: 17px; line-height: 1.7; margin-bottom: 20px;">{intro}</p>
            {faq_html}
        </div>
    </section>
    <!-- END UNIQUE CONTENT -->
'''
    return section

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    if '<!-- UNIQUE CONTENT FOR' in content:
        return False

    rel_path = file_path.relative_to(BASE_DIR)
    parts = list(rel_path.parts)

    if parts[-1] == 'index.html':
        parts = parts[:-1]

    if len(parts) == 0:
        return False

    if parts[0] == 'brooklyn' and len(parts) == 2:
        page_type = "location"
        location = format_name(parts[1])
        unique_content = generate_content(page_type, location=location)

    elif parts[0] == 'brooklyn' and len(parts) == 3:
        page_type = "location_service"
        location = format_name(parts[1])
        service = parts[2]
        unique_content = generate_content(page_type, location=location, service=service)

    elif parts[0] == 'brands' and len(parts) >= 2:
        page_type = "brand"
        brand = format_name(parts[1])
        unique_content = generate_content(page_type, brand=brand)

    else:
        return False

    if not unique_content:
        return False

    if '</main>' in content:
        content = content.replace('</main>', unique_content + '</main>')
    elif '<footer' in content:
        content = re.sub(r'(<footer)', unique_content + r'\1', content, count=1)
    else:
        content = content.replace('</body>', unique_content + '</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    html_files = list(BASE_DIR.rglob('index.html'))
    print(f"Found {len(html_files)} total pages")

    count = 0
    for f in html_files:
        if 'assets' in str(f) or 'sitemap' in str(f):
            continue
        if process_file(f):
            count += 1

    print(f"Added unique content to {count} pages")

if __name__ == "__main__":
    main()
