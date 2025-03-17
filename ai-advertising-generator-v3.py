import streamlit as st
import google.generativeai as genai
import pandas as pd
import io  # For creating in-memory CSV files

# Configuration - consider using a config.ini file as in the previous response for API key
# Ensure you have your API key set up here
API_KEY = "YOUR_API_KEY" # Replace with your actual API Key
MODEL_NAME = 'gemini-1.5-flash-latest'

# Generate Advertisements Function (Modified)
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
            continue # Skip to the next ad block

    return ads

def create_csv_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded in csv format."""
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    b64 = st.components.v1.html(
        f'<a href="data:file/csv;base64,{base64.b64encode(csv_data.encode()).decode()}" download="advertisements.csv">Download CSV</a>',
        unsafe_allow_html=True
    )
    return b64

# Streamlit App
st.title("AI Advertising Generator")

# User Inputs
ad_idea = st.text_input("Your Advertising Idea:", "")
keywords = st.text_input("Keywords to emphasize:", "")

tone_options = ["Informative", "Humorous", "Serious", "Exciting", "Friendly", "Authoritative", "Witty", "Empathetic", "Trendy", "Inspirational"]
tone = st.selectbox("Select Advertising Tone:", tone_options)

age_group_options = ["0-18", "18-25", "26-35", "36-45", "46-55", "Over 55"]
age_group = st.selectbox("Select Target Age Group:", age_group_options)

# Call to Action Selection
cta_options = ["Shop Now", "Learn More", "Sign Up", "Contact Us", "Visit Website", "Free Trial"]  #Example options
call_to_action = st.selectbox("Select Call to Action:", cta_options)

# Ad Variation Slider
ad_variation = st.slider("Ad Variation (1-10):", min_value=1, max_value=10, value=5)

# Generate Button
if st.button("Generate Advertisements"):
    if ad_idea:
        with st.spinner("Generating advertisements..."):
            advertisement_text = generate_advertisements(ad_idea, API_KEY, tone, age_group, keywords, call_to_action, ad_variation)

            st.subheader("Generated Advertisements:")
            st.markdown(advertisement_text)

            #Parse the Ads
            ads = parse_advertisements(advertisement_text)

            #Create DataFrame
            if ads:  # Only if ads were successfully parsed
                df = pd.DataFrame(ads)

                #Create Download Link
                st.subheader("Download Advertisements as CSV")
                create_csv_download_link(df)

            else:
                st.warning("Could not parse the generated advertisements for CSV download.")


    else:
        st.warning("Please enter an advertising idea first!")

# Footer
st.markdown("---")
st.write("Powered by Nathan Rossow @ Burst Software & Google AI | © 2025 Advertising Solutions")
