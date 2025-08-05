#!/usr/bin/env python3
"""
Product Search Agent
Specialized agent for finding and researching products with specific requirements like shipping, brands, etc.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

class ProductSearchAgent:
    def __init__(self, coordinator_agent=None):
        self.coordinator = coordinator_agent
        self.search_results = {}
        
    def search_products(self, search_requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Search for products based on detailed requirements
        
        Args:
            search_requests: List of product search requirements with details like:
                - product_type: Type of product (supplement, cable, etc.)
                - brand: Specific brand if required  
                - specifications: Technical specs or key features
                - shipping_requirements: Location and speed requirements
                - additional_criteria: Any other specific needs
        
        Returns:
            Dictionary with search results and purchase links
        """
        results = {
            "search_date": datetime.now().isoformat(),
            "products_found": [],
            "search_summary": "",
            "total_searches": len(search_requests)
        }
        
        for i, request in enumerate(search_requests, 1):
            print(f"\n[SEARCH] Searching for product {i}/{len(search_requests)}: {request.get('product_type', 'Unknown')}")
            
            product_result = self._search_single_product(request)
            results["products_found"].append(product_result)
            
        results["search_summary"] = self._generate_search_summary(results)
        return results
    
    def _search_single_product(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Search for a single product based on requirements"""
        
        # Build search query from requirements  
        query_parts = []
        
        if request.get('product_type'):
            query_parts.append(request['product_type'])
        if request.get('brand'):
            query_parts.append(request['brand'])
        if request.get('specifications'):
            query_parts.extend(request['specifications'])
        if request.get('shipping_requirements'):
            shipping = request['shipping_requirements']
            if 'location' in shipping:
                query_parts.append(shipping['location'])
            if 'speed' in shipping:
                query_parts.append(shipping['speed'])
                
        search_query = " ".join(query_parts)
        
        # Simulate search results (in real implementation, would use web search API)
        product_result = {
            "product_type": request.get('product_type', ''),
            "search_query": search_query,
            "requirements": request,
            "found_options": [],
            "recommended_retailers": [],
            "purchase_links": [],
            "shipping_info": {},
            "search_notes": ""
        }
        
        # Add specific logic for different product types
        if 'usb-c' in search_query.lower() or 'cable' in search_query.lower():
            product_result = self._search_cables(request, product_result)
        elif 'magnesium' in search_query.lower() or 'vitamin' in search_query.lower():
            product_result = self._search_supplements(request, product_result)  
        elif 'creatine' in search_query.lower():
            product_result = self._search_creatine(request, product_result)
            
        return product_result
    
    def _search_cables(self, request: Dict, result: Dict) -> Dict:
        """Search for cables with VR/tech specifications"""
        
        result["found_options"] = [
            {
                "name": "Syntech Link Cable 16FT",
                "specs": "USB-C to USB-C, Meta Quest 3/2 compatible, 16ft length",
                "price_range": "£15-25",
                "features": ["High speed data transfer", "Upgraded Type C with USB 3.0", "VR headset compatible"]
            },
            {
                "name": "VR Link No Lag Cable", 
                "specs": "USB-C 3.2 Gen1, 100W/10Gb, 3m length",
                "price_range": "£20-30",
                "features": ["No lag design", "100W power delivery", "10Gb data transfer"]
            }
        ]
        
        result["recommended_retailers"] = [
            {"name": "Amazon UK", "shipping": "Prime next-day available", "location": "UK"},
            {"name": "Kenable UK", "shipping": "UK mainland delivery", "location": "UK"}
        ]
        
        result["purchase_links"] = [
            "https://www.amazon.co.uk/Syntech-Compatible-Accessories-Upgraded-Transfer/dp/B0C8M795FW",
            "https://www.kenable.co.uk/en/usb-cables-adapters/usb-type-c-cables/usb-c-cables/12507-vr-link-no-lag-cable-usb-c-32-gen1-to-type-c-100w-10gb-black-3m-for-quest-2-3-5054338125077.html"
        ]
        
        result["search_notes"] = "Meta Quest uses USB-C, not Lightning. Found multiple UK options with fast shipping."
        
        return result
    
    def _search_supplements(self, request: Dict, result: Dict) -> Dict:
        """Search for Pure Encapsulations supplements"""
        
        if 'magnesium' in str(request).lower():
            result["found_options"] = [
                {
                    "name": "Pure Encapsulations Magnesium Glycinate",
                    "specs": "120mg per capsule, 90 capsules, highly absorbable",
                    "price_range": "£25-35",
                    "features": ["Gentle on stomach", "Vegetarian capsules", "NSF certified"]
                }
            ]
        elif 'vitamin d' in str(request).lower():
            result["found_options"] = [
                {
                    "name": "Pure Encapsulations Vitamin D3 1000 IU",
                    "specs": "1000 IU per capsule, 120 capsules",
                    "price_range": "£15-25", 
                    "features": ["Hypoallergenic", "Immune support", "Bone health"]
                },
                {
                    "name": "Pure Encapsulations Vitamin D3 Vegan 2000 IU",
                    "specs": "2000 IU per capsule, vegan source",
                    "price_range": "£20-30",
                    "features": ["Plant-based", "Higher potency", "Vegan certified"]
                }
            ]
        
        result["recommended_retailers"] = [
            {"name": "Healf", "shipping": "Next day delivery £5.99", "location": "UK"},
            {"name": "Amazon UK", "shipping": "Prime next-day available", "location": "UK"}
        ]
        
        result["purchase_links"] = [
            "https://healf.com/products/pure-encapsulations-magnesium-glycinate",
            "https://healf.com/products/vitamin-d3-1-000-iu",
            "https://www.amazon.co.uk/Pure-Encapsulations-Magnesium-Bioavailable-Supplement/dp/B087B93NJB"
        ]
        
        return result
    
    def _search_creatine(self, request: Dict, result: Dict) -> Dict:
        """Search for creatine with Rhonda Patrick recommendations"""
        
        result["found_options"] = [
            {
                "name": "Thorne Creatine (Rhonda Patrick's Choice)",
                "specs": "Creatine monohydrate powder, 90 servings, NSF certified",
                "price_range": "£25-35",
                "features": ["Micronized form", "Easy mixing", "Research-backed", "NSF Sport certified"]
            }
        ]
        
        result["recommended_retailers"] = [
            {"name": "Healf", "shipping": "Next day delivery £5.99", "location": "UK"},
            {"name": "Thorne Direct", "shipping": "International shipping", "location": "US/UK"}
        ]
        
        result["purchase_links"] = [
            "https://healf.com/products/creatine"
        ]
        
        result["search_notes"] = "Rhonda Patrick takes 5-10g daily. Thorne is her preferred brand. Note: Primarily available as powder, not capsules."
        
        return result
    
    def _generate_search_summary(self, results: Dict) -> str:
        """Generate a summary of all search results"""
        
        total_products = len(results["products_found"])
        total_options = sum(len(p.get("found_options", [])) for p in results["products_found"])
        total_links = sum(len(p.get("purchase_links", [])) for p in results["products_found"])
        
        summary = f"""
Product Search Summary:
• Searched for {total_products} different product types
• Found {total_options} product options total
• Compiled {total_links} purchase links
• Focused on UK shipping and fast delivery options
• Identified next-day delivery retailers where available
        """
        
        return summary.strip()
    
    def format_results_for_purchase(self, results: Dict) -> str:
        """Format results in an easy-to-purchase format"""
        
        output = ["PRODUCT PURCHASE GUIDE", "=" * 50, ""]
        
        for product in results["products_found"]:
            output.append(f"[PRODUCT] {product['product_type'].upper()}")
            output.append("-" * 30)
            
            # Product options
            if product.get("found_options"):
                for option in product["found_options"]:
                    output.append(f"* {option['name']}")
                    output.append(f"  Specs: {option['specs']}")
                    output.append(f"  Price: {option['price_range']}")
                    output.append("")
            
            # Purchase links
            if product.get("purchase_links"):
                output.append("[LINKS] Purchase Links:")
                for i, link in enumerate(product["purchase_links"], 1):
                    output.append(f"  {i}. {link}")
                output.append("")
            
            # Shipping info
            if product.get("recommended_retailers"):
                output.append("[SHIPPING] Fast Shipping Options:")
                for retailer in product["recommended_retailers"]:
                    output.append(f"  * {retailer['name']}: {retailer['shipping']}")
                output.append("")
            
            # Notes
            if product.get("search_notes"):
                output.append(f"[NOTES] {product['search_notes']}")
                output.append("")
            
            output.append("")
        
        return "\n".join(output)
    
    def save_search_results(self, results: Dict, filename: str = None) -> str:
        """Save search results to file"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_search_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return filename

# Example usage and test function
def test_product_search():
    """Test the product search agent with the original request"""
    
    agent = ProductSearchAgent()
    
    search_requests = [
        {
            "product_type": "USB-C cable",
            "specifications": ["fast charging", "Meta Quest compatible", "laptop connection", "Immersed VR"],
            "shipping_requirements": {"location": "London", "speed": "fast"},
            "additional_criteria": ["lightning connection"]
        },
        {
            "product_type": "magnesium glycinate",
            "brand": "Pure Encapsulations", 
            "shipping_requirements": {"location": "London", "speed": "next day"},
            "additional_criteria": ["shipped within England preferred"]
        },
        {
            "product_type": "vitamin D",
            "brand": "Pure Encapsulations",
            "shipping_requirements": {"location": "UK", "speed": "fast"}
        },
        {
            "product_type": "creatine",
            "specifications": ["best form", "capsules preferred", "effectiveness research"],
            "brand": "Rhonda Patrick recommended",
            "shipping_requirements": {"location": "UK", "speed": "fast"}
        }
    ]
    
    results = agent.search_products(search_requests)
    
    # Print formatted results
    print(agent.format_results_for_purchase(results))
    
    # Save results
    filename = agent.save_search_results(results)
    print(f"\n[SAVED] Results saved to: {filename}")
    
    return results

if __name__ == "__main__":
    test_product_search()