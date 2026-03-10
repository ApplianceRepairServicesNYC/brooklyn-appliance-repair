#!/usr/bin/env python3
"""
Add unique content to each Brooklyn location page to avoid duplicate content issues.
"""

import re
import hashlib
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/brooklyn-appliance-repair')

NEIGHBORHOOD_INTROS = [
    "As a cornerstone of {location}'s community, we've built our reputation on reliable, honest appliance repair service.",
    "{location} is known for its unique character - and our technicians know the neighborhood inside and out.",
    "From {location}'s historic homes to modern developments, we service every type of appliance setup.",
    "Our {location} customers appreciate our straightforward pricing and same-day service availability.",
    "{location} families trust us because we treat every home like our own - with care and respect.",
    "We're proud to serve {location}'s diverse community with expert appliance repair at fair prices.",
    "Whether you're in a {location} brownstone or high-rise, our technicians arrive prepared for any repair.",
    "{location}'s busy households need appliances that work - and we make sure they do.",
    "Our deep roots in {location} mean we understand the unique needs of local residents.",
    "Fast, friendly service has made us {location}'s go-to choice for appliance repairs.",
]

SERVICE_INTROS = [
    "Every service van carries hundreds of parts, so most repairs are completed in a single visit.",
    "We diagnose the problem accurately the first time - saving you time and money on unnecessary repairs.",
    "Our technicians are factory-trained on all major brands, from budget-friendly to luxury appliances.",
    "Upfront quotes mean no surprises - you approve the price before we start any repair work.",
    "We back every repair with a warranty because we stand behind the quality of our work.",
    "Emergency service available for urgent breakdowns - because some problems can't wait.",
    "Flexible scheduling including evenings and weekends to fit your busy Brooklyn lifestyle.",
    "We use genuine OEM parts whenever possible to ensure your repair lasts.",
    "Our friendly dispatchers make booking easy - call or schedule online in minutes.",
    "Decades of Brooklyn experience means we've seen and fixed every appliance problem imaginable.",
]

FAQ_SETS = [
    [
        ("How fast can you get to {location}?", "Our Brooklyn-based technicians typically reach {location} within 1-2 hours. Same-day service is our standard."),
        ("Do you repair all brands in {location}?", "Yes - LG, Samsung, Whirlpool, GE, Frigidaire, Maytag, Bosch, and all other major brands."),
        ("What's the service call fee for {location}?", "Our flat diagnostic fee covers the visit and diagnosis. It's applied to repair costs if you proceed."),
    ],
    [
        ("Are you licensed for {location} repairs?", "Absolutely. Fully licensed, insured, and background-checked technicians serve {location}."),
        ("Do you work weekends in {location}?", "Yes! We offer 7-day service. {location} residents can book Saturday and Sunday appointments."),
        ("What warranty do {location} repairs include?", "90-day parts and labor warranty on all repairs - {location} customers get full coverage."),
    ],
    [
        ("Can you fix commercial appliances in {location}?", "We primarily serve residential customers in {location}, but can handle some commercial units. Call to discuss."),
        ("Do you service {location} apartment buildings?", "Yes. We work with building management and individual tenants throughout {location}."),
        ("How do I pay for {location} service?", "Credit cards, debit, cash, or check accepted. Payment due when repair is complete."),
    ],
    [
        ("Is same-day repair possible in {location}?", "Usually yes! Call early for best same-day availability in {location}."),
        ("What if the repair costs more than a new appliance?", "We'll tell you honestly. {location} customers only pay for repairs that make economic sense."),
        ("Do you offer maintenance plans for {location}?", "We focus on repairs, but happy to discuss ongoing maintenance for {location} customers."),
    ],
    [
        ("How do I book a {location} appointment?", "Call or use our online scheduler. We'll confirm your {location} time slot immediately."),
        ("What areas around {location} do you serve?", "All of Brooklyn! {location} neighbors get the same fast, reliable service."),
        ("Do you provide repair estimates for {location}?", "Yes - free estimates provided before any work begins. No obligation for {location} residents."),
    ],
]

def get_hash_index(location, num_options):
    hash_val = int(hashlib.md5(location.encode()).hexdigest(), 16)
    return hash_val % num_options

def format_location(slug):
    return slug.replace("-", " ").title()

def generate_unique_section(location):
    idx1 = get_hash_index(location + "intro", len(NEIGHBORHOOD_INTROS))
    idx2 = get_hash_index(location + "service", len(SERVICE_INTROS))
    idx3 = get_hash_index(location + "faq", len(FAQ_SETS))

    neighborhood_intro = NEIGHBORHOOD_INTROS[idx1].format(location=location)
    service_intro = SERVICE_INTROS[idx2].format(location=location)
    faqs = FAQ_SETS[idx3]

    faq_html = ""
    for q, a in faqs:
        q_formatted = q.format(location=location)
        a_formatted = a.format(location=location)
        faq_html += f'''
        <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <h4 style="margin: 0 0 10px 0; color: var(--blue);">{q_formatted}</h4>
            <p style="margin: 0; color: #555;">{a_formatted}</p>
        </div>'''

    unique_section = f'''
    <!-- UNIQUE CONTENT FOR {location.upper()} -->
    <section style="padding: 40px 20px; background: #fff;">
        <div style="max-width: 900px; margin: 0 auto;">
            <h2 style="text-align: center; color: var(--blue); margin-bottom: 30px;">Why {location} Chooses Us</h2>
            <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px;">{neighborhood_intro}</p>
            <p style="font-size: 18px; line-height: 1.8; margin-bottom: 30px;">{service_intro}</p>

            <h3 style="color: var(--blue); margin: 30px 0 20px;">Frequently Asked Questions - {location}</h3>
            {faq_html}
        </div>
    </section>
    <!-- END UNIQUE CONTENT -->
'''
    return unique_section

def add_unique_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    if '<!-- UNIQUE CONTENT FOR' in content:
        return False

    rel_path = file_path.relative_to(BASE_DIR)
    parts = list(rel_path.parts)

    if len(parts) < 2 or parts[0] != 'brooklyn':
        return False

    if len(parts) > 3:
        return False

    location = format_location(parts[1])
    unique_section = generate_unique_section(location)

    if '</main>' in content:
        content = content.replace('</main>', unique_section + '</main>')
    elif '<footer' in content:
        content = re.sub(r'(<footer)', unique_section + r'\1', content, count=1)
    else:
        content = content.replace('</body>', unique_section + '</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    brooklyn_dir = BASE_DIR / 'brooklyn'
    count = 0

    for loc_dir in brooklyn_dir.iterdir():
        if loc_dir.is_dir():
            index_file = loc_dir / 'index.html'
            if index_file.exists():
                if add_unique_content(index_file):
                    count += 1

    print(f"Added unique content to {count} Brooklyn location pages")

if __name__ == "__main__":
    main()
