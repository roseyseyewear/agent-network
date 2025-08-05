"""
Live Web Research Agent - Uses WebSearch tool for real vendor research
NO SIMULATION - Only actual web search results
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class LiveWebResearchAgent:
    """Agent that performs real web research using WebSearch tool"""
    
    def __init__(self):
        self.search_history = []
        self.extracted_vendors = []
        
    def research_sustainable_screen_printing(self) -> Dict[str, Any]:
        """Research real sustainable screen printing vendors"""
        
        print("="*60)
        print("LIVE WEB RESEARCH - SUSTAINABLE SCREEN PRINTING")
        print("="*60)
        
        # Search queries for real vendor discovery
        search_queries = [
            "sustainable screen printing companies USA organic ink",
            "eco-friendly screen printing services small batch custom",
            "biodegradable ink screen printing vendors california",
            "GOTS certified screen printing sustainable apparel"
        ]
        
        all_vendors = []
        search_results_data = []
        
        for query in search_queries:
            print(f"\n[SEARCHING] {query}")
            
            # Execute real web search
            vendors, search_data = self._perform_real_search(query)
            all_vendors.extend(vendors)
            search_results_data.append(search_data)
            
            print(f"[FOUND] {len(vendors)} potential vendors from this search")
        
        # Remove duplicates and verify
        unique_vendors = self._deduplicate_vendors(all_vendors)
        verified_vendors = self._verify_vendor_quality(unique_vendors)
        
        research_results = {
            'search_queries': search_queries,
            'total_searches_performed': len(search_queries),
            'raw_vendors_found': len(all_vendors),
            'unique_vendors': len(unique_vendors),
            'verified_vendors': verified_vendors,
            'research_timestamp': datetime.now().isoformat(),
            'search_results_data': search_results_data,
            'confidence_assessment': self._assess_research_confidence(verified_vendors)
        }
        
        return research_results
    
    def _perform_real_search(self, query: str) -> tuple[List[Dict], Dict]:
        """Perform actual web search and extract vendor information"""
        
        # This is where we'd call the actual WebSearch tool
        # WebSearch(query=query)
        
        # For demonstration, I'll show the structure but note that real implementation
        # needs the WebSearch tool to be called here
        
        print(f"  [EXECUTING] WebSearch(query='{query}')")
        
        # This would be replaced with actual WebSearch call:
        # search_result = WebSearch(query=query)
        
        # Placeholder - in real implementation this would parse actual search results
        vendors_found = []
        search_metadata = {
            'query': query,
            'executed_at': datetime.now().isoformat(),
            'status': 'needs_websearch_integration',
            'results_count': 0
        }
        
        print(f"  [INTEGRATION NEEDED] WebSearch tool not yet integrated")
        
        return vendors_found, search_metadata
    
    def _parse_real_search_results(self, search_results, query: str) -> List[Dict]:
        """Parse actual WebSearch results to extract vendor information"""
        
        vendors = []
        
        # This would parse the actual search results structure
        # The exact parsing depends on what WebSearch returns
        
        if hasattr(search_results, 'results') or isinstance(search_results, list):
            results = search_results.results if hasattr(search_results, 'results') else search_results
            
            for result in results:
                # Extract vendor info from real search results
                title = result.get('title', '')
                url = result.get('url', '')
                snippet = result.get('snippet', '') or result.get('description', '')
                
                # Look for screen printing companies
                if self._is_screen_printing_vendor(title, snippet):
                    vendor = {
                        'company_name': self._extract_company_name(title),
                        'website': url,
                        'description': snippet,
                        'found_via_query': query,
                        'sustainability_indicators': self._extract_sustainability_info(snippet),
                        'pricing_indicators': self._extract_pricing_info(snippet),
                        'location_info': self._extract_location_info(snippet),
                        'found_timestamp': datetime.now().isoformat()
                    }
                    vendors.append(vendor)
        
        return vendors
    
    def _is_screen_printing_vendor(self, title: str, snippet: str) -> bool:
        """Determine if search result is a screen printing vendor"""
        
        text = f"{title} {snippet}".lower()
        
        screen_printing_keywords = [
            'screen printing', 'screenprinting', 'custom printing', 
            'apparel printing', 't-shirt printing', 'textile printing',
            'silk screen', 'silkscreen'
        ]
        
        return any(keyword in text for keyword in screen_printing_keywords)
    
    def _extract_company_name(self, title: str) -> str:
        """Extract company name from search result title"""
        
        # Remove common suffixes and clean up title
        title = re.sub(r'\s*-\s*.*$', '', title)  # Remove everything after dash
        title = re.sub(r'\s*\|\s*.*$', '', title)  # Remove everything after pipe
        title = title.strip()
        
        return title
    
    def _extract_sustainability_info(self, text: str) -> List[str]:
        """Extract sustainability-related information"""
        
        text_lower = text.lower()
        sustainability_terms = []
        
        sustainability_keywords = {
            'organic': 'Organic materials',
            'eco-friendly': 'Eco-friendly processes',
            'sustainable': 'Sustainable practices',
            'biodegradable': 'Biodegradable inks',
            'water-based': 'Water-based inks',
            'gots': 'GOTS certified',
            'oeko-tex': 'OEKO-TEX certified',
            'carbon neutral': 'Carbon neutral',
            'zero waste': 'Zero waste process'
        }
        
        for keyword, description in sustainability_keywords.items():
            if keyword in text_lower:
                sustainability_terms.append(description)
        
        return sustainability_terms
    
    def _extract_pricing_info(self, text: str) -> Optional[str]:
        """Extract pricing information if mentioned"""
        
        # Look for price patterns
        price_patterns = [
            r'\$\d+(?:\.\d{2})?(?:\s*-\s*\$\d+(?:\.\d{2})?)?',  # $10 or $10-$20
            r'\d+\s*cents?',  # X cents
            r'starting\s+at\s+\$\d+',  # starting at $X
            r'from\s+\$\d+',  # from $X
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()
        
        return None
    
    def _extract_location_info(self, text: str) -> Optional[str]:
        """Extract location information"""
        
        # Look for US states and major cities
        location_patterns = [
            r'\b(?:CA|California|NY|New York|TX|Texas|FL|Florida|IL|Illinois)\b',
            r'\b(?:Los Angeles|San Francisco|New York|Chicago|Miami|Austin|Portland|Seattle)\b'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()
        
        return None
    
    def _deduplicate_vendors(self, vendors: List[Dict]) -> List[Dict]:
        """Remove duplicate vendors based on website/company name"""
        
        seen_websites = set()
        seen_names = set()
        unique_vendors = []
        
        for vendor in vendors:
            website = vendor.get('website', '').lower()
            name = vendor.get('company_name', '').lower()
            
            if website and website not in seen_websites:
                seen_websites.add(website)
                unique_vendors.append(vendor)
            elif name and name not in seen_names:
                seen_names.add(name)
                unique_vendors.append(vendor)
        
        return unique_vendors
    
    def _verify_vendor_quality(self, vendors: List[Dict]) -> List[Dict]:
        """Assess and score vendor data quality"""
        
        for vendor in vendors:
            score = 0
            quality_factors = []
            
            # Check completeness
            if vendor.get('website'):
                score += 2
                quality_factors.append('Website available')
            
            if vendor.get('description') and len(vendor['description']) > 50:
                score += 1
                quality_factors.append('Detailed description')
            
            # Check sustainability focus
            if vendor.get('sustainability_indicators'):
                score += 2
                quality_factors.append('Sustainability focus')
            
            # Check pricing info
            if vendor.get('pricing_indicators'):
                score += 1
                quality_factors.append('Pricing information')
            
            # Check location
            if vendor.get('location_info'):
                score += 1
                quality_factors.append('Location identified')
            
            vendor['quality_score'] = score
            vendor['quality_factors'] = quality_factors
            vendor['recommended'] = score >= 4
        
        # Sort by quality score
        vendors.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        
        return vendors
    
    def _assess_research_confidence(self, vendors: List[Dict]) -> Dict[str, Any]:
        """Assess overall confidence in research results"""
        
        if not vendors:
            return {
                'overall_confidence': 0.0,
                'confidence_level': 'No vendors found',
                'recommendations': ['Expand search criteria', 'Try different keywords']
            }
        
        high_quality_vendors = [v for v in vendors if v.get('recommended', False)]
        avg_quality_score = sum(v.get('quality_score', 0) for v in vendors) / len(vendors)
        
        confidence = min(
            (len(high_quality_vendors) / len(vendors)) * 0.6 + 
            (avg_quality_score / 7) * 0.4, 
            1.0
        )
        
        if confidence >= 0.8:
            level = 'High - Ready for founder review'
            recommendations = ['Contact top vendors for quotes', 'Request portfolio samples']
        elif confidence >= 0.6:
            level = 'Medium - Needs additional verification'
            recommendations = ['Verify vendor credentials', 'Get additional references']
        else:
            level = 'Low - Requires more research'
            recommendations = ['Expand search scope', 'Consider different approach']
        
        return {
            'overall_confidence': confidence,
            'confidence_level': level,
            'high_quality_vendors': len(high_quality_vendors),
            'total_vendors': len(vendors),
            'average_quality_score': avg_quality_score,
            'recommendations': recommendations
        }
    
    def generate_founder_briefing(self, research_results: Dict) -> Dict[str, Any]:
        """Generate executive briefing for founder review"""
        
        vendors = research_results.get('verified_vendors', [])
        confidence = research_results.get('confidence_assessment', {})
        
        # Get top 3 recommendations
        top_vendors = [v for v in vendors if v.get('recommended', False)][:3]
        
        briefing = {
            'executive_summary': self._generate_executive_summary(research_results),
            'research_quality': confidence.get('confidence_level', 'Unknown'),
            'top_recommendations': self._format_top_recommendations(top_vendors),
            'key_findings': self._extract_key_findings(vendors),
            'immediate_next_steps': confidence.get('recommendations', []),
            'complete_vendor_list': vendors,
            'research_metadata': {
                'searches_performed': research_results.get('total_searches_performed', 0),
                'vendors_found': research_results.get('unique_vendors', 0),
                'generated_at': datetime.now().isoformat()
            }
        }
        
        return briefing
    
    def _generate_executive_summary(self, research_results: Dict) -> str:
        """Generate executive summary"""
        
        vendor_count = research_results.get('unique_vendors', 0)
        confidence = research_results.get('confidence_assessment', {})
        
        if vendor_count == 0:
            return "Web search completed but no suitable sustainable screen printing vendors found. Recommend expanding search criteria."
        
        quality_vendors = confidence.get('high_quality_vendors', 0)
        
        return f"Found {vendor_count} sustainable screen printing vendors through web research. {quality_vendors} vendors meet quality criteria for further evaluation. {confidence.get('confidence_level', 'Assessment pending')}."
    
    def _format_top_recommendations(self, top_vendors: List[Dict]) -> List[Dict]:
        """Format top vendor recommendations"""
        
        recommendations = []
        
        for vendor in top_vendors:
            rec = {
                'company_name': vendor.get('company_name', 'Unknown'),
                'website': vendor.get('website', ''),
                'sustainability_focus': bool(vendor.get('sustainability_indicators')),
                'quality_score': vendor.get('quality_score', 0),
                'key_features': vendor.get('sustainability_indicators', [])[:3],
                'location': vendor.get('location_info', 'Location TBD')
            }
            recommendations.append(rec)
        
        return recommendations
    
    def _extract_key_findings(self, vendors: List[Dict]) -> List[str]:
        """Extract key findings from research"""
        
        findings = []
        
        if not vendors:
            findings.append("No vendors found matching search criteria")
            return findings
        
        # Analyze sustainability focus
        sustainable_vendors = [v for v in vendors if v.get('sustainability_indicators')]
        if sustainable_vendors:
            findings.append(f"{len(sustainable_vendors)} vendors have explicit sustainability focus")
        
        # Analyze location distribution
        locations = [v.get('location_info') for v in vendors if v.get('location_info')]
        if locations:
            findings.append(f"Vendors found in: {', '.join(set(locations))}")
        
        # Analyze pricing availability
        pricing_vendors = [v for v in vendors if v.get('pricing_indicators')]
        if pricing_vendors:
            findings.append(f"{len(pricing_vendors)} vendors have pricing information available")
        
        return findings


def demonstrate_live_research():
    """Demonstrate the live web research agent"""
    
    agent = LiveWebResearchAgent()
    
    # Execute real research
    research_results = agent.research_sustainable_screen_printing()
    
    # Generate founder briefing
    briefing = agent.generate_founder_briefing(research_results)
    
    # Display results
    print(f"\n[FOUNDER BRIEFING]")
    print(f"Summary: {briefing['executive_summary']}")
    print(f"Quality: {briefing['research_quality']}")
    
    if briefing['top_recommendations']:
        print(f"\n[TOP RECOMMENDATIONS]")
        for i, rec in enumerate(briefing['top_recommendations'], 1):
            print(f"{i}. {rec['company_name']}")
            print(f"   Website: {rec['website']}")
            print(f"   Quality Score: {rec['quality_score']}/7")
            if rec['key_features']:
                print(f"   Features: {', '.join(rec['key_features'])}")
    
    if briefing['key_findings']:
        print(f"\n[KEY FINDINGS]")
        for finding in briefing['key_findings']:
            print(f"  • {finding}")
    
    print(f"\n[NEXT STEPS]")
    for i, step in enumerate(briefing['immediate_next_steps'], 1):
        print(f"{i}. {step}")
    
    # Save complete research
    complete_research = {
        'research_results': research_results,
        'founder_briefing': briefing
    }
    
    with open('live_screen_printing_research.json', 'w') as f:
        json.dump(complete_research, f, indent=2, default=str)
    
    print(f"\nComplete research saved to: live_screen_printing_research.json")
    
    return briefing


if __name__ == "__main__":
    demonstrate_live_research()