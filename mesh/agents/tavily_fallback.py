from typing import Any, Dict, Optional


def build_tavily_search_fallback(search_term: str, limit: int = 10) -> Dict[str, Any]:
    """Build a fallback spec targeting Tavily web search."""
    return {
        "module": "mesh.agents.tavily_search_agent",
        "class": "TavilySearchAgent",
        "input": {"tool": "tavily_web_search", "tool_arguments": {"search_term": search_term, "limit": limit}},
    }


def build_firecrawl_to_tavily_fallback(
    tool_name: Optional[str], function_args: Dict[str, Any], original_params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Standard mapping from Firecrawl tools or NL queries to Tavily search fallback.
    Returns a fallback spec or None when not applicable.
    """
    if tool_name == "firecrawl_web_search":
        search_term = function_args.get("search_term") or original_params.get("query") or ""
        limit = function_args.get("limit", 10)
        return build_tavily_search_fallback(search_term, limit)
    if tool_name == "firecrawl_scrape_url":
        url = function_args.get("url") or ""
        return build_tavily_search_fallback(url, 10)
    if tool_name == "firecrawl_extract_web_data":
        urls = function_args.get("urls") or []
        search_term = urls[0] if urls else (original_params.get("query") or "")
        return build_tavily_search_fallback(search_term, 10)

    if not tool_name:
        query = original_params.get("query") or ""
        return build_tavily_search_fallback(query, 10)

    return None
