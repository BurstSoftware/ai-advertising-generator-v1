import streamlit as st
import google.generativeai as genai
import pandas as pd
import io  # For creating in-memory CSV files
import os
#from dotenv import load_dotenv # Removed dotenv import

#load_dotenv()  # Load environment variables from .env #Commented out dotenv loading

#API_KEY = os.getenv("API_KEY")  # Access API key from environment # Commented out dotenv
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash-latest")  # Default if not set
VERSION = os.getenv("VERSION", "1.0")  # Default if not set


def generate_advertisements(ad_idea, api_key, tone, age_group, keywords="", call_to_action="", ad_variation=5):
    """Generate advertisements with options for keywords, CTA, and variation."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)

        prompt = f"""Generate 10 unique advertisement ideas for {ad_idea}.
        Target audience: {age_group}.
        Tone: {tone}.
        Emphasize these keywords: {keywords}.
        Include this call to action: {call_to_action}.
        Vary the advertisements to a level of {ad_variation} out of 10, 1 being minimal variation and 10 being high variation.
        For each advertisement, provide:
        Ad [Number]:
        Headline: [Your headline]
        Description: [Your description]
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        st.error(f"Error generating advertisements: {str(e)}") # Display error in Streamlit
        return ""  # Return empty string to avoid further errors


def parse_advertisements(advertisement_text):
    """Parses the advertisement text into a list of dictionaries."""
    ads = []
    ad_blocks = advertisement_text.split("Ad ")  # Split into individual ad blocks

    for ad_block in ad_blocks[1:]:  # Skip the first empty element
        try:
            number, content = ad_block.split(":", 1)  # Split into number and content
            lines = content.strip().split("\n")  # Split content into lines
            headline = lines[0].split(": ", 1)[1].strip()  # Extract headline
            description = lines[1].split(": ", 1)[1].strip()  # Extract description

            ads.append({"Ad Number": number.strip(), "Headline": headline, "Description": description})
        except Exception as e:
            print(f"Error parsing ad block: {ad_block}, Error: {e}")  # Debugging
            continue  # Skip to the next ad block

    return ads


def create_csv_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded in csv format."""
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    import base64
    b64 = base64.b64encode(csv_data.encode()).decode()  # Encode to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="advertisements.csv">Download CSV File</a>'
    return href


# Streamlit App
st.title("AI Advertising Generator")

# API Key Input
API_KEY = st.text_input("Enter your Google API Key:", type="password")

# Check if API key is available
if not API_KEY:
    st.warning("Please enter your Google API Key to continue.")
    st.stop() # Stop the app if the API key is missing

# User Inputs
ad_idea = st.text_input("Your Advertising Idea:", "")
keywords = st.text_input("Keywords to emphasize:", "")

tone_options = ["Informative", "Humorous", "Serious", "Exciting", "Friendly", "Authoritative", "Witty",
                "Empathetic", "Trendy", "Inspirational"]
tone = st.selectbox("Select Advertising Tone:", tone_options)

age_group_options = ["0-18", "18-25", "26-35", "36-45", "46-55", "Over 55"]
age_group = st.selectbox("Select Target Age Group:", age_group_options)

# Call to Action Selection
cta_options = ["Shop Now", "Learn More", "Sign Up", "Contact Us", "Visit Website", "Free Trial"]  # Example options
call_to_action = st.selectbox("Select Call to Action:", cta_options)

# Ad Variation Slider
ad_variation = st.slider("Ad Variation (1-10):", min_value=1, max_value=10, value=5)

# Generate Button
if st.button("Generate Advertisements"):
    if ad_idea:
        with st.spinner("Generating advertisements..."):
            advertisement_text = generate_advertisements(ad_idea, API_KEY, tone, age_group, keywords, call_to_action,
                                                        ad_variation)

        if advertisement_text: # Only proceed if there's advertisement text
            st.subheader("Generated Advertisements:")
            st.markdown(advertisement_text)

            # Parse the Ads
            ads = parse_advertisements(advertisement_text)

            # Create DataFrame and Download Link
            if ads:
                df = pd.DataFrame(ads)
                csv_link = create_csv_download_link(df)  # Get the HTML link
                st.markdown(f"#### Download Advertisements as CSV\n\n{csv_link}", unsafe_allow_html=True)  # display the link
            else:
                st.warning("Could not parse the generated advertisements for CSV download.")
    else:
        st.warning("Please enter an advertising idea first!")

# Footer
st.markdown("---")
st.write(f"Powered by Nathan Rossow @ Burst Software & Google AI | Version: {VERSION} | © 2025 Advertising Solutions")
