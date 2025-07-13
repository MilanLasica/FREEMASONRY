# Business Configuration for AI Reply Generation

# Default business context - users can modify this
DEFAULT_BUSINESS_CONTEXT = {
    "company_name": "Your Business Name",
    "industry": "Your Industry",
    "tone": "professional",  # professional, friendly, casual, authoritative
    "personality": "helpful and knowledgeable",
    "key_services": [
        "Service 1",
        "Service 2", 
        "Service 3"
    ],
    "brand_values": [
        "Quality",
        "Innovation",
        "Customer satisfaction"
    ],
    "target_audience": "professionals and businesses",
    "reply_guidelines": [
        "Be helpful and informative",
        "Keep responses concise and relevant",
        "Always add value to the conversation",
        "Include a subtle call-to-action when appropriate",
        "Maintain professional tone"
    ],
    "avoid_topics": [
        "Political discussions",
        "Controversial subjects",
        "Direct competitors"
    ],
    "call_to_action_phrases": [
        "Learn more about our services",
        "Let's connect and discuss further", 
        "Feel free to reach out for more information",
        "Would love to help you with this"
    ]
}

# Reply templates for different types of tweets
REPLY_TEMPLATES = {
    "question": "Great question! {response}. {cta}",
    "complaint": "I understand your concern. {response}. {cta}",
    "positive": "Thanks for sharing! {response}. {cta}",
    "informational": "Interesting point! {response}. {cta}",
    "general": "{response}. {cta}"
}

# Claude.ai system prompt template
CLAUDE_SYSTEM_PROMPT = """You are a social media engagement specialist for {company_name}, a company in the {industry} industry. 

Your role is to generate thoughtful, engaging replies to tweets that are relevant to the business. 

Business Context:
- Company: {company_name}
- Industry: {industry}
- Tone: {tone}
- Personality: {personality}
- Key Services: {services}
- Brand Values: {values}
- Target Audience: {target_audience}

Guidelines:
{guidelines}

Avoid:
{avoid_topics}

Generate a reply that:
1. Is relevant to the original tweet
2. Adds value to the conversation
3. Maintains the specified tone and personality
4. Is concise (under 280 characters)
5. Includes a subtle call-to-action when appropriate
6. Feels natural and authentic

Do not include hashtags unless specifically relevant. Focus on being helpful and engaging rather than promotional."""

def get_business_context():
    """Get the current business context configuration"""
    return DEFAULT_BUSINESS_CONTEXT.copy()

def update_business_context(new_context):
    """Update business context (in a real app, this would save to database)"""
    global DEFAULT_BUSINESS_CONTEXT
    DEFAULT_BUSINESS_CONTEXT.update(new_context)
    return DEFAULT_BUSINESS_CONTEXT

def format_system_prompt(context=None):
    """Format the Claude system prompt with business context"""
    if context is None:
        context = get_business_context()
    
    return CLAUDE_SYSTEM_PROMPT.format(
        company_name=context["company_name"],
        industry=context["industry"],
        tone=context["tone"],
        personality=context["personality"],
        services=", ".join(context["key_services"]),
        values=", ".join(context["brand_values"]),
        target_audience=context["target_audience"],
        guidelines="\n".join([f"- {guideline}" for guideline in context["reply_guidelines"]]),
        avoid_topics=", ".join(context["avoid_topics"])
    )