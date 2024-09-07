import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

# Function to get response from the LLaMA model
def get_llama_response(input_text, no_words, blog_style):
    llm = CTransformers(
        model="LLM/llama-2-7b-chat.Q8_0.gguf",
        model_type='llama',
        config={'max_new_tokens': int(no_words),
                'temperature': 0.01}
    )
    
    # Prompt template
    template = """
    Write a blog for a {blog_style} job profile on the topic "{input_text}"
    with approximately {no_words} words.
    """
    
    prompt = PromptTemplate(
        input_variables=["blog_style", "no_words", "input_text"],
        template=template
    )

    # Generate response from LLaMA model
    response = llm(prompt.format(blog_style=blog_style,
                                 input_text=input_text,
                                 no_words=no_words))
    return response

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
