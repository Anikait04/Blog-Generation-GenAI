import streamlit as st
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_llama_response(input_text, no_words, blog_style, 
                       tone='Professional', 
                       complexity='Intermediate', 
                       language='English', 
                       seo_keywords=None, 
                       creativity=5, 
                       content_focus='Informative'):
    """
    Generate a blog post with advanced customization options
    
    Parameters:
    - input_text: Main blog topic
    - no_words: Desired word count
    - blog_style: Target audience
    - tone: Writing tone (Professional, Conversational, etc.)
    - complexity: Writing complexity level
    - language: Target language
    - seo_keywords: List of SEO keywords
    - creativity: Creativity level (0-10)
    - content_focus: Primary content type
    """

    # Safety settings to prevent inappropriate content
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_LOW_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        }
    ]

    # Dynamic generation configuration based on creativity
    generation_config = {
        "temperature": min(0.1 + (creativity * 0.09), 1.0),  # Scale temperature with creativity
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    # Advanced prompt template with more contextual parameters
    template = """
    Compose a {complexity} level blog post with a {tone} tone, targeting {blog_style} audience.

    Content Specifications:
    - Primary Topic: '{input_text}'
    - Language: {language}
    - Approximate Length: {no_words} words
    - Content Focus: {content_focus}
    
    Special Instructions:
    {seo_instructions}
    {creativity_instructions}

    Write a comprehensive, engaging, and well-structured blog post that:
    1. Provides deep insights into the topic
    2. Maintains a {tone} writing style
    3. Is accessible to {blog_style} audience
    4. Uses clear, precise language
    5. Incorporates a {content_focus} approach
    """
    
    # Prepare SEO and creativity instructions
    seo_instructions = f"SEO Keywords to integrate naturally: {', '.join(seo_keywords) if seo_keywords else 'None'}"
    
    creativity_instructions = f"""
    Creativity Level: {creativity}/10
    - If creativity is low (0-3), prioritize factual, straightforward content
    - If creativity is medium (4-7), include some engaging examples or analogies
    - If creativity is high (8-10), incorporate storytelling, unique perspectives, and innovative insights
    """
    
    # Create the prompt with all parameters
    full_prompt = template.format(
        input_text=input_text,
        no_words=no_words,
        blog_style=blog_style,
        tone=tone,
        complexity=complexity,
        language=language,
        content_focus=content_focus,
        seo_instructions=seo_instructions,
        creativity_instructions=creativity_instructions
    )
    
    # Initialize the model with dynamic configuration
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        safety_settings=safety_settings
        
    )
    
    # Generate the response
    response = model.generate_content(full_prompt)
    return response.text

# Optional: Add logging or tracking for generated content
def log_generation(topic, parameters):
    """
    Optional method to log blog generation details
    This can be expanded to include database logging, analytics, etc.
    """
    try:
        import datetime
        log_entry = {
            'timestamp': datetime.datetime.now(),
            'topic': topic,
            'parameters': parameters
        }
        # Placeholder for more advanced logging
        print(f"Blog Generated: {log_entry}")
    except Exception as e:
        print(f"Logging error: {e}")