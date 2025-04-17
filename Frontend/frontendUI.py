import streamlit as st
from PIL import Image
import os
logo_path = os.path.join("..", "Images", "logo.png")
logo = Image.open(logo_path)

# Page config
st.set_page_config(page_title="Photo Fission", layout="wide")


# Sidebar (Navbar)
with st.sidebar:
    st.image(logo, width=200)  # Resize as needed
    st.title("Photo Fission")
    navigation = st.radio("Navigate", ["🏠 Home", "📂 Sort Images", "⚙️ Settings", "ℹ️ About"])

# Main section based on navigation
if navigation == "🏠 Home":
    st.title("Photo Fission")
    st.write("This app is used to sort the images of any sport based on the team and jersey number.")

elif navigation == "📂 Sort Images":
    st.title("Sort Sports Images")
    st.write("Upload and classify your images here.")
    
    # Image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Open and display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
        
        # Add your sorting logic here (e.g., model inference for team, jersey number)
        # For now, let's just create a dummy input for sorting
        team = st.text_input("Enter Team Name")
        jersey_number = st.number_input("Enter Jersey Number", min_value=1, max_value=99)
        
        if st.button("Sort Image"):
            if team and jersey_number:
                st.write(f"Image sorted: Team - {team}, Jersey Number - {jersey_number}")
                # Add logic to save or process the image based on sorting
            else:
                st.error("Please enter both team and jersey number to sort the image.")

elif navigation == "⚙️ Settings":
    st.title("Settings")
    st.write("Configure your sorting preferences.")

elif navigation == "ℹ️ About":
    st.title("About Photo Fission")
    st.write("Photo Fission is an AI-powered sports image sorting app built with Streamlit and FastAPI.")
