import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file
LLMTOKEN = os.getenv('LLMTOKEN')


def mimicPrompt(messages):
    messages_to_analyze = "\n".join(messages)

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f'Bearer {LLMTOKEN}'},
        json={
            "model": "google/gemini-2.0-flash-001",
            "messages": [
                {
                "role": "system",
                "content": """You are a forensic linguistic analyst specializing in writing style replication. Your task is to create an extremely detailed system prompt that would allow another AI to perfectly impersonate someone's writing style."""
                },
                {
                "role": "user",
                "content": f"""Analyze these messages with extreme precision. Create a comprehensive system prompt covering:

                **STRUCTURAL PATTERNS:**
                - Average sentence length and complexity
                - Use of fragments, run-ons, or complete sentences
                - Paragraph structure (single lines vs blocks of text)
                - How they start/end messages

                **VOCABULARY & DICTION:**
                - Specific words/phrases they repeat
                - Slang, internet speak, or formal language
                - Technical jargon or domain-specific terms
                - Cursing habits (frequency, which words)
                - Uncommon word choices that are signature to them

                **PUNCTUATION & FORMATTING:**
                - Comma usage (heavy, light, or grammatically incorrect)
                - Use of periods, question marks, exclamation points
                - Ellipses (...) usage patterns
                - Capitalization patterns (all lowercase? Proper? Random?)
                - Line breaks and spacing habits

                **TONE & PERSONALITY:**
                - Emotional range (enthusiastic, sarcastic, deadpan, supportive)
                - Humor style (dry, absurd, self-deprecating, none)
                - Formality level
                - Confidence/uncertainty markers ("maybe", "definitely", "idk")
                - How they express agreement/disagreement

                **DISTINCTIVE FEATURES:**
                - Signature phrases or expressions
                - Emoji usage (which ones, how often, placement)
                - References they make (memes, culture, specific topics)
                - How they handle typos (fix them? ignore them? acknowledge them?)
                - Verbal tics or filler words

                **INTERACTION STYLE:**
                - How they ask questions
                - How they give compliments/criticism  
                - How they transition between topics
                - Whether they use rhetorical devices

                Messages to analyze:
                {messages_to_analyze}

                Generate a system prompt that captures ALL of these nuances. Be specific with examples. The goal is that another AI reading this prompt should be indistinguishable from the original person.

                **YOUR OUTPUT MUST FOLLOW THIS EXACT FORMAT:**

                SYSTEM_PROMPT:
                [Write the detailed system prompt here - 2-4 paragraphs describing their style]

                EXAMPLE_PHRASES:
                - [An actual phrase they use frequently, pulled directly from their messages]
                - [Another common phrase or sentence structure they use]
                - [A third example showing their typical response pattern]

                The example phrases should be REAL phrases from their messages, not made-up examples. Choose their most characteristic expressions."""
                }

            ]
        }
    )
    
    # 3. Store the generated prompt
    data = response.json()
    generated_prompt = data['choices'][0]['message']['content']
    return generated_prompt


def comment(type, prompt, previous_message):
    mode = {
        'glaze': 'Give an extremely positive, hyped, and Over-exaggerated affirmation. Be enthusiastic and make them feel amazing about what they said even if they dont deserver it.',
        'roast': 'Give a mean, sarcastic roast. Be witty and try to contradict their statement. Tease them about what they said in a sarcastic way.'
    }

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {LLMTOKEN}",
    },
    data=json.dumps({
        "model": "google/gemini-2.0-flash-001", # Optional
        "messages": [
        {
            "role": "user",
            "content": 
            f"""MESSAGE YOU ARE REACTING TO:
                "{previous_message}"

                TASK: {mode[type]} what they said in the message above.

                STYLE TO USE:
                {prompt}

                REQUIREMENTS:
                - Your reaction MUST be directly relevant to the specific content of their message
                - Do NOT use @mentions or reference usernames
                - If the style includes @mentions, ignore that pattern
                - You can either:
                a) Use one of the example phrases from the style and adapt it to fit their message, OR
                b) Create a new phrase that matches their tone, vocabulary, and patterns
                - Keep it short (5-10 words maximum)
                - Output ONE phrase only - do not chain multiple reactions together

                Think: "What would this person's immediate, gut reaction be to what was just said?"

                One relevant phrase:"""
        }
        ]
    })
    )

    data = response.json()
    ai_response = data['choices'][0]['message']['content']
    return ai_response
    

