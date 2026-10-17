#!/usr/bin/env python3
import json
import sys
from client import InstacartCartSubstitutionAffinityResolver

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        resolver = InstacartCartSubstitutionAffinityResolver()
        orig = {"title": "Organic Oat Milk 64oz", "category": "Dairy Alternative", "brand": "Oatly", "price_usd": 5.49, "dietary_tags": ["vegan", "organic", "dairy_free"]}
        inv = [
            {"title": "Califia Farms Organic Oat Milk 64oz", "category": "Dairy Alternative", "brand": "Califia", "price_usd": 5.79, "dietary_tags": ["vegan", "organic", "dairy_free"]},
            {"title": "Whole Dairy Milk 1 Gal", "category": "Dairy", "brand": "Horizon", "price_usd": 4.99, "dietary_tags": ["organic"]}
        ]
        res = resolver.resolve_out_of_stock_substitution(orig, inv, {"max_price_delta_pct": 10.0})
        assert res["action_verdict"] == "AUTONOMOUS_SUBSTITUTION_CONFIRMED"
        assert res["chosen_substitute"]["brand"] == "Califia"
        print(f"[TEST PASS] Instacart Substitution Resolved: {res['chosen_substitute']['title']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-instacart-substitution-resolver", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "resolve_out_of_stock_substitution", "description": "Instacart grocery out-of-stock substitution resolver"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                resolver = InstacartCartSubstitutionAffinityResolver()
                out = resolver.resolve_out_of_stock_substitution(args.get("original_item", {}), args.get("available_inventory", []), args.get("customer_preferences"))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
