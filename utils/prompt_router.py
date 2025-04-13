def get_smart_prompt(query: str) -> str:
    query_lower = query.lower()

    if "experience" in query_lower:
        return f"Summarize the professional experiences described in this document.\n\nQuery: {query}"
    
    elif "author" in query_lower or "owner" in query_lower:
        return f"Identify the author or creator of this document.\n\nQuery: {query}"
    
    elif "summary" in query_lower:
        return f"Provide a high-level summary of this document.\n\nQuery: {query}"
    
    elif "keywords" in query_lower:
        return f"List important keywords or recurring topics found in this document.\n\nQuery: {query}"
    
    elif any(word in query_lower for word in ["contact", "email", "phone"]):
        return f"Extract contact details like name, email, or phone number from this document.\n\nQuery: {query}"
    
    else:
        return f"This query doesn't match predefined categories. Please clarify your request.\n\nQuery: {query}"
