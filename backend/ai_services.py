"""
AI Services for Threads of Tradition platform.
Provides caption generation and price recommendation logic.
"""

import random


# Material base prices (in INR)
MATERIAL_PRICES = {
    'silk': 800,
    'cotton': 300,
    'wool': 500,
    'linen': 400,
    'jute': 250,
    'bamboo': 350,
    'khadi': 450,
    'pashmina': 1200,
    'chiffon': 600,
    'georgette': 550,
    'velvet': 700,
    'brocade': 900,
    'other': 350
}

# Caption templates for variety
CAPTION_TEMPLATES = [
    "Embrace the artistry of {location} with this exquisite {material} creation. Handcrafted with love over {time} hours by {artisan}, this piece embodies generations of Indian tradition and cultural heritage. Each thread tells a story of dedication and mastery.",
    
    "Discover the magic of handwoven {material} from the heart of {location}. Artisan {artisan} has poured {time} hours of meticulous craftsmanship into this masterpiece. A perfect blend of tradition and elegance for the discerning connoisseur.",
    
    "This stunning {material} piece carries the soul of {location}'s rich textile heritage. Created by skilled artisan {artisan} over {time} hours, it represents the pinnacle of Indian handloom tradition. Own a piece of living history.",
    
    "From the looms of {location} comes this breathtaking {material} creation. Artisan {artisan} has invested {time} hours to bring you authentic Indian craftsmanship. Each motif whispers tales of our ancestors.",
    
    "Experience the warmth of tradition with this handcrafted {material} treasure from {location}. {artisan}'s {time} hours of dedicated work shine through every intricate detail. A celebration of India's artisanal legacy.",
    
    "Unveil the beauty of authentic Indian handicraft with this {material} masterpiece. Born from {time} hours of patient work by {artisan} of {location}, it carries forward centuries of weaving tradition.",
    
    "Let this exquisite {material} piece transport you to the artistic heritage of {location}. Handmade by {artisan} with {time} hours of passionate craftsmanship, it's more than a product—it's a cultural treasure.",
    
    "Celebrate the spirit of Make in India with this gorgeous {material} creation from {location}. Artisan {artisan}'s {time} hours of labor have produced a timeless piece that honors our textile traditions."
]

# Material descriptions for enhanced captions
MATERIAL_DESCRIPTIONS = {
    'silk': 'luxurious silk',
    'cotton': 'soft, breathable cotton',
    'wool': 'warm, natural wool',
    'linen': 'elegant linen',
    'jute': 'eco-friendly jute',
    'bamboo': 'sustainable bamboo fiber',
    'khadi': 'authentic, hand-spun khadi',
    'pashmina': 'premium Kashmiri pashmina',
    'chiffon': 'delicate chiffon',
    'georgette': 'flowing georgette',
    'velvet': 'rich velvet',
    'brocade': 'ornate brocade',
    'other': 'traditional fiber'
}


def generate_caption(material: str, time_spent: float, artisan_name: str, location: str) -> str:
    """
    Generate an AI-powered marketing caption for a handmade product.
    
    Args:
        material: Type of material used (e.g., 'silk', 'cotton')
        time_spent: Hours spent making the product
        artisan_name: Name of the artisan
        location: Location of the artisan
    
    Returns:
        A marketing-style caption highlighting tradition and craftsmanship
    """
    # Get material description
    material_desc = MATERIAL_DESCRIPTIONS.get(material.lower(), material)
    
    # Format time spent
    if time_spent >= 24:
        days = time_spent / 24
        time_str = f"{days:.1f} days ({time_spent:.0f} hours)"
    else:
        time_str = f"{time_spent:.0f}"
    
    # Select random template
    template = random.choice(CAPTION_TEMPLATES)
    
    # Generate caption
    caption = template.format(
        material=material_desc,
        time=time_str,
        artisan=artisan_name,
        location=location
    )
    
    return caption


def recommend_price(material: str, time_spent: float) -> tuple:
    """
    Generate a price recommendation based on material and time spent.
    
    Args:
        material: Type of material used
        time_spent: Hours spent making the product
    
    Returns:
        Tuple of (min_price, max_price) in INR
    """
    # Get base price for material
    base_price = MATERIAL_PRICES.get(material.lower(), MATERIAL_PRICES['other'])
    
    # Calculate time-based component (₹50 per hour for skilled labor)
    hourly_rate = 50
    time_component = time_spent * hourly_rate
    
    # Handmade premium (30% of base price)
    handmade_premium = base_price * 0.30
    
    # Quality factor based on time investment
    if time_spent > 48:  # More than 2 days
        quality_multiplier = 1.5
    elif time_spent > 24:  # More than 1 day
        quality_multiplier = 1.3
    elif time_spent > 8:  # More than 8 hours
        quality_multiplier = 1.15
    else:
        quality_multiplier = 1.0
    
    # Calculate base recommended price
    base_recommended = (base_price + time_component + handmade_premium) * quality_multiplier
    
    # Price range with ±15% margin
    margin = 0.15
    min_price = round(base_recommended * (1 - margin), -1)  # Round to nearest 10
    max_price = round(base_recommended * (1 + margin), -1)
    
    # Ensure minimum prices
    min_price = max(min_price, 200)
    max_price = max(max_price, min_price + 100)
    
    return (min_price, max_price)


def get_available_materials() -> list:
    """Return list of available materials for dropdown."""
    return list(MATERIAL_PRICES.keys())


def generate_certificate_id() -> str:
    """Generate a fake certificate ID for demo purposes."""
    import uuid
    return f"TOT-CERT-{uuid.uuid4().hex[:8].upper()}"
