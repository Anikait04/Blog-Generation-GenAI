import streamlit as st
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Function to get response from the LLaMA model
def get_llama_response(input_text, no_words, blog_style):

    # Create the model
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_LOW_AND_ABOVE",  # Or BLOCK_MEDIUM_AND_ABOVE, BLOCK_ONLY_HIGH, BLOCK_NONE
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
    }]

    generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    
    # Prompt template
    template = """
    "Compose a blog post on the topic of '{input_text}' with a professional and straightforward style, aiming for approximately {no_words} words. The blog post should prioritize factual accuracy and present information concisely and clearly. Avoid colloquialisms, informal language, and overly casual phrasing. Focus on delivering the essential information regarding the topic using verifiable data and key concepts. The tone should be objective and authoritative, reflecting a focus on facts and clear communication, rather than subjective opinions or personal anecdotes "
    """
    
    prompt = PromptTemplate(
        input_variables=["blog_style", "no_words", "input_text"],
        template=template,
        safety_settings=safety_settings
    )
    
    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    safety_settings=safety_settings
    
    )
    
    user_prompt=prompt.format(blog_style=blog_style,
                                 input_text=input_text,
                                 no_words=no_words)
    # Generate response from LLaMA model
    response = model.generate_content(user_prompt)
    return response.text

# Streamlit app configuration
st.set_page_config(page_title="Generate Blogs",
                   page_icon='✨',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Blogs ✨")

# Input fields
input_text = st.text_input("Enter the Blog Topic")

# Creating two columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('Number of Words')
with col2:
    blog_style = st.selectbox('Writing the blog for',
                              ('Researchers', 'Data Scientist', 'Common People'),
                              index=0)

# Generate button
submit = st.button("Generate")

# Display the final response
if submit:
    if input_text and no_words and blog_style:
        response = get_llama_response(input_text, no_words, blog_style)
        st.write(response)
    else:
        st.warning("Please fill in all the fields.")
