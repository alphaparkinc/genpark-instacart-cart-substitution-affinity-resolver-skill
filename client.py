"""
Instacart-inspired Grocery Substitution & Affinity Resolver (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
from typing import Dict, Any, List, Optional

class InstacartCartSubstitutionAffinityResolver:
    def __init__(self, engine_name: str = "Instacart-Smart-Substitution-Core"):
        self.engine_name = engine_name

    def compute_substitution_suitability(self, original: Dict[str, Any], candidate: Dict[str, Any], prefs: Dict[str, Any]) -> float:
        # 1. Category strict alignment
        if candidate.get("category") != original.get("category"):
            return 0.0
            
        # 2. Dietary constraints gatekeeper (must have all required tags)
        orig_tags = set(original.get("dietary_tags", []))
        cand_tags = set(candidate.get("dietary_tags", []))
        strict_diet = set(prefs.get("strict_dietary_requirements", [])) | orig_tags
        if not strict_diet.issubset(cand_tags):
            return 0.0
            
        # 3. Price delta constraint (max allowed inflation)
        orig_price = float(original.get("price_usd", 10.0))
        cand_price = float(candidate.get("price_usd", 10.0))
        max_delta_pct = float(prefs.get("max_price_delta_pct", 15.0))
        price_diff_pct = ((cand_price - orig_price) / max(1.0, orig_price)) * 100.0
        if price_diff_pct > max_delta_pct:
            return 0.0
            
        # 4. Affinity score
        affinity = 1.0
        if candidate.get("brand") == original.get("brand"):
            affinity += 0.5
        if candidate.get("brand") in prefs.get("preferred_brands", []):
            affinity += 0.3
        # Favor equal or lower price
        if cand_price <= orig_price:
            affinity += 0.2
            
        return round(affinity, 3)

    def resolve_out_of_stock_substitution(self, original_item: Dict[str, Any], available_inventory: List[Dict[str, Any]], customer_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prefs = customer_preferences or {}
        
        ranked_substitutes = []
        for item in available_inventory:
            score = self.compute_substitution_suitability(original_item, item, prefs)
            if score > 0.0:
                ranked_substitutes.append({**item, "substitution_affinity_score": score})
                
        ranked_substitutes.sort(key=lambda x: x["substitution_affinity_score"], reverse=True)
        best_match = ranked_substitutes[0] if ranked_substitutes else None
        
        return {
            "resolver": self.engine_name,
            "original_item": original_item["title"],
            "eligible_substitutes_found": len(ranked_substitutes),
            "chosen_substitute": best_match,
            "action_verdict": "AUTONOMOUS_SUBSTITUTION_CONFIRMED" if best_match else "REFUND_ITEM_CUSTOMER_PROMPT_REQUIRED"
        }
