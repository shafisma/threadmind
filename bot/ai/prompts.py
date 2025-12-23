SUMMARY_PROMPT = """
You are a {tone} AI assistant.

Summarize this Discord conversation.
Return:
- Key points
- Final decisions
- Open questions
"""

DECISION_PROMPT = """
Extract ONLY finalized decisions.
Ignore opinions. Don't use things like ``` and ```.

Return JSON:
[
  {{
    "decision": "...",
    "confidence": 0.0-1.0
  }}
]
"""

SENTIMENT_PROMPT = """
Analyze the sentiment and emotional tone of this Discord conversation.
Don't use markdown code blocks.

Return JSON:
{{
  "overall_sentiment": "positive|neutral|negative",
  "sentiment_score": -1.0 to 1.0,
  "tone": "professional|casual|frustrated|excited|neutral",
  "themes": ["theme1", "theme2"],
  "emotional_summary": "brief description"
}}
"""

ACTION_ITEMS_PROMPT = """
Extract ALL action items, TODOs, and tasks from this conversation.
Ignore completed items. Don't use markdown code blocks.

Return JSON:
[
  {{
    "task": "...",
    "assignee": "name or null",
    "priority": "high|medium|low",
    "deadline": "date or null"
  }}
]
"""

PARTICIPANTS_PROMPT = """
Analyze who participated and their contributions in this conversation.
Don't use markdown code blocks.

Return JSON:
[
  {{
    "name": "username",
    "message_count": number,
    "contribution_type": "question|answer|decision|discussion",
    "key_contributions": ["topic1", "topic2"]
  }}
]
"""

TIMELINE_PROMPT = """
Create a chronological timeline of key events/topics from this conversation.
Don't use markdown code blocks.

Return JSON:
[
  {{
    "timestamp_order": number,
    "event": "brief description",
    "type": "decision|question|announcement|discussion"
  }}
]
"""

COMPARISON_PROMPT = """
Compare these two summaries and highlight differences, similarities, and evolution.
Don't use markdown code blocks.

Summary 1: {summary1}

Summary 2: {summary2}

Return JSON:
{{
  "similarities": ["point1", "point2"],
  "differences": ["diff1", "diff2"],
  "evolution": "how the discussion evolved",
  "new_decisions": ["decision1"],
  "resolved_questions": ["question1"]
}}
"""

STATISTICS_PROMPT = """
Analyze statistics about Discord activity and decision-making patterns.
Data: {data}
Don't use markdown code blocks.

Return JSON:
{{
  "total_summaries": number,
  "avg_decisions_per_summary": number,
  "most_active_participants": ["name1", "name2"],
  "decision_categories": {{"category": count}},
  "trends": ["trend1", "trend2"],
  "top_topics": ["topic1", "topic2"]
}}
"""
