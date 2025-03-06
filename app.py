import streamlit as st
import pyperclip
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import os
from dotenv import load_dotenv
from llm_response import get_llama_response, log_generation
import time

# Load environment variables
load_dotenv()

# Streamlit app configuration
st.set_page_config(
    page_title="AI Blog Craft Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom colorful CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    body {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-container {
        background: linear-gradient(145deg, #ffffff 0%, #f0f0f0 100%);
        border-radius: 20px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        padding: 2rem;
        margin: 1rem;
    }
    
    .advanced-options {
        background: linear-gradient(to right, #e0eafc, #cfdef3);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .stSlider>div>div>div {
        background-color: #4e54c8 !important;
    }
    
    .stMultiselect>div>div {
        background: linear-gradient(to right, #4e54c8, #8f94fb);
        color: white;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Colorful Title Container
st.markdown("""
    <div class="title-container" style="background: linear-gradient(to right, #fc6076, #ff9a9a); color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
        <h1 style="margin:0; font-size:2.5em;">✨ AI Blog Craft Pro 📝</h1>
        <p style="margin:10px 0 0; opacity:0.8;">Unleash Your Content's Potential</p>
    </div>
""", unsafe_allow_html=True)

# Advanced Options Container
st.markdown('<div class="advanced-options">', unsafe_allow_html=True)
st.header("🔧 Advanced Customization")

# Create columns for advanced options
col1, col2, col3 = st.columns(3)

with col1:
    # Tone Selection with Tooltip
    tone = st.selectbox(
        "🎭 Writing Tone",
        [
            'Professional',
            'Conversational', 
            'Academic', 
            'Inspirational', 
            'Technical', 
            'Storytelling'
        ],
        index=0,
        help="Choose the emotional and stylistic approach of your writing. This affects the overall mood and language of the blog post."
    )

with col2:
    # Complexity Level with Tooltip
    complexity = st.select_slider(
        "🧠 Writing Complexity",
        options=['Beginner', 'Intermediate', 'Advanced', 'Expert'],
        value='Intermediate',
        help="Select the level of technical depth and vocabulary complexity. Higher levels use more sophisticated language and concepts."
    )

with col3:
    # Language Selection with Tooltip
    language = st.selectbox(
        "🌐 Language",
        [
            'English', 
            'Spanish', 
            'French', 
            'German', 
            'Portuguese', 
            'Chinese', 
            'Hindi'
        ],
        index=0,
        help="Choose the language for your blog post. This determines the linguistic context and vocabulary."
    )

# Additional Customization Row
col4, col5, col6 = st.columns(3)

with col4:
    # SEO Keywords with Tooltip
    seo_keywords = st.multiselect(
        "🔑 SEO Keywords",
        [
            'AI', 'Technology', 'Machine Learning', 
            'Data Science', 'Innovation', 'Blockchain', 
            'Sustainability', 'Future Trends'
        ],
        help="Select keywords to optimize your content for search engines. These will be naturally integrated into the blog post."
    )

with col5:
    # Creativity Slider with Enhanced Tooltip
    creativity = st.slider(
        "✨ Creativity Level", 
        min_value=0, 
        max_value=10, 
        value=5,
        help="""
        Adjust the level of creative expression in the blog post:
        - 0-3: Factual, straightforward content
        - 4-7: Engaging examples and mild creativity
        - 8-10: Highly innovative, storytelling approach
        """
    )

with col6:
    # Content Focus with Tooltip
    content_focus = st.selectbox(
        "🎯 Content Focus",
        [
            'Informative', 
            'Persuasive', 
            'Narrative', 
            'Analytical', 
            'Exploratory'
        ],
        index=0,
        help="Determine the primary purpose and structure of the content. Each focus guides the blog post's approach and style."
    )

st.markdown('</div>', unsafe_allow_html=True)

# Original Input Section
st.header("🚀 Blog Generation Parameters")

# Create columns for inputs
col7, col8, col9 = st.columns(3)

with col7:
    input_text = st.text_input(
        "📌 Blog Topic", 
        placeholder="Enter your blog topic here...",
        help="Provide a clear and specific topic for your blog post. Be concise yet descriptive."
    )

with col8:
    # Enhanced Word Count Input with Real-time Preview
    no_words = st.text_input(
        "📏 Number of Words", 
        placeholder="e.g., 500",
        help="Specify the approximate length of your blog post. The AI will aim to generate content close to this word count."
    )
    
    # Real-time Word Count Validation
    if no_words:
        try:
            word_count = int(no_words)
            if word_count < 100:
                st.warning("⚠️ Very short blog post. Consider increasing length.")
            elif word_count > 2000:
                st.warning("⚠️ Very long blog post. Consider reducing length.")
            else:
                st.success(f"✅ Target: {word_count} words")
        except ValueError:
            st.error("❌ Please enter a valid number")

with col9:
    # Target Audience with Tooltip
    blog_style = st.selectbox(
        "🎯 Target Audience",
        ['Researchers', 'Data Scientists', 'Common People'],
        index=0,
        help="Choose the primary audience for your blog post. This influences the complexity, terminology, and explanation depth."
    )

# Generate button with enhanced styling
generate_col1, generate_col2, generate_col3 = st.columns([2,2,6])
with generate_col2:
    submit = st.button("Generate Blog Post", use_container_width=True)

# Initialize session state for generated response
if 'generated_response' not in st.session_state:
    st.session_state.generated_response = None

# Response handling
if submit:
    # Validate inputs
    if not all([input_text, no_words, blog_style]):
        st.warning("🚨 Please fill in all the fields!")
    else:
        try:
            # Prepare parameters for logging
            generation_params = {
                'topic': input_text,
                'words': no_words,
                'audience': blog_style,
                'tone': tone,
                'complexity': complexity,
                'language': language,
                'seo_keywords': seo_keywords,
                'creativity': creativity,
                'content_focus': content_focus
            }

            # Log the generation attempt
            log_generation(input_text, generation_params)

            # Progress Bar with Text
            progress_text = st.empty()
            progress_bar = st.progress(0)
            for percent_complete in range(101):
                time.sleep(0.02)
                progress_bar.progress(percent_complete)
                progress_text.text(f"Generating content... {percent_complete}%")
            progress_text.empty()

            # Spinner during generation
            with st.spinner('✨ Crafting your blog post...'):
                # Call get_llama_response with all new parameters
                response = get_llama_response(
                    input_text, 
                    no_words, 
                    blog_style,
                    tone=tone,
                    complexity=complexity,
                    language=language,
                    seo_keywords=seo_keywords,
                    creativity=creativity,
                    content_focus=content_focus
                )
            
            # Store the response in session state
            st.session_state.generated_response = response
            
            # Character Count Preview
            st.info(f"📊 Generated Content: {len(response)} characters | Estimated Words: {len(response.split())}")
            
            # Display response in a styled container
            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.subheader("🖋️ Generated Blog Post")
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Copy Blog Post Button (Always visible when a response exists)
if st.session_state.generated_response:
    copy_col1, copy_col2, copy_col3 = st.columns([2,2,6])
    with copy_col2:
        if st.button("📋 Copy Blog Post", use_container_width=True):
            try:
                # Use pyperclip to copy the text
                pyperclip.copy(st.session_state.generated_response)
                st.success('Blog Post Copied to Clipboard! 📝')
            except Exception as e:
                st.error(f"Could not copy to clipboard: {e}")

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px; background: linear-gradient(to right, #f5f7fa, #e6e9f0);'>
    Created with 💖 using Streamlit and Google Generative AI
    </div>
""", unsafe_allow_html=True)