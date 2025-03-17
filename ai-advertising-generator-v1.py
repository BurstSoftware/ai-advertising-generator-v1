import streamlit as st
import google.generativeai as genai

def generate_advertisements(ad_idea, api_key):
    """Generate 10 advertisements using Google's Gemini model"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.0-pro') # Changed model name
        
        prompt = f"""Generate 10 unique advertisement ideas for {ad_idea}. 
        For each advertisement, provide:
        1. A catchy headline
        2. A brief description (2-3 sentences)
        Format each ad as:
        Ad [Number]:
        Headline: [Your headline]
        Description: [Your description]
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error generating advertisements: {str(e)}"

# Streamlit app setup
st.title("AI Advertising Generator")
st.write("Please enter your Google API key to use the advertisement generator!")

# API Key input
api_key = st.text_input("Google API Key:", type="password")

# Only show the main app if API key is provided
if api_key:
    st.write("Enter your advertising idea below to generate 10 unique advertisements!")
    
    # User input for advertising idea
    ad_idea = st.text_input("Your Advertising Idea:", "")
    
    # Generate response when user submits idea
    if st.button("Generate"):
        if ad_idea:
            with st.spinner("Generating advertisements..."):
                advertisements = generate_advertisements(ad_idea, api_key)
                
                st.subheader("Generated Advertisements:")
                st.markdown(advertisements)
                
                # Generate question, answer, and contact based on first ad
                question = f"How can I effectively promote {ad_idea} to reach my target audience?"
                answer = f"To effectively promote {ad_idea}, consider using the creative concepts generated above, tailored to your specific audience through multiple channels like social media, print, and digital advertising."
                contact = "For a detailed marketing strategy tailored to your needs, contact our advertising experts at: marketing@solutions.com or call us at (555) 123-4567."
                
                st.subheader("Follow-up Information:")
                st.write(f"**Question:** {question}")
                st.write(f"**Answer:** {answer}")
                st.write(f"**Contact:** {contact}")
        else:
            st.warning("Please enter an advertising idea first!")
else:
    st.warning("Please enter your Google API key to continue.")

# Add some basic styling and footer
st.markdown("---")
st.write("Powered by xAI & Google AI | © 2025 Advertising Solutions")
