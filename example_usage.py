from client import InstacartCartSubstitutionAffinityResolver

def main():
    resolver = InstacartCartSubstitutionAffinityResolver()
    out_of_stock = {
        "title": "Avocado Oil Mayo 12oz",
        "category": "Condiments",
        "brand": "Primal Kitchen",
        "price_usd": 8.99,
        "dietary_tags": ["keto", "gluten_free"]
    }
    candidates = [
        {"title": "Chosen Foods Avocado Oil Mayo 12oz", "category": "Condiments", "brand": "Chosen Foods", "price_usd": 9.29, "dietary_tags": ["keto", "gluten_free"]},
        {"title": "Standard Soybean Mayo 30oz", "category": "Condiments", "brand": "Hellmanns", "price_usd": 4.99, "dietary_tags": []}
    ]
    res = resolver.resolve_out_of_stock_substitution(out_of_stock, candidates, {"max_price_delta_pct": 10.0})
    print("--- Instacart Real-Time Substitution Decision ---")
    print(f"Original (OOS): {res['original_item']}")
    print(f"Verdict: {res['action_verdict']}")
    if res['chosen_substitute']:
        print(f"Auto-Replaced With: {res['chosen_substitute']['title']} (${res['chosen_substitute']['price_usd']})")

if __name__ == "__main__":
    main()
