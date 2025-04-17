import streamlit as st
from PIL import Image
import os
import requests

# Load logo
logo_path = os.path.join("..", "Images", "logo.png")
logo = Image.open(logo_path)

TYPE = None

# Page config
st.set_page_config(page_title="Photo Fission", layout="wide")

# Sidebar (Navbar)
with st.sidebar:
    st.image(logo, width=100)  # Resize as needed
    st.title("Photo Fission")
    navigation = st.radio("Navigate", ["🏠 Home", "📞 Contact Us", "ℹ️ About"])

# Main section based on navigation
if navigation == "🏠 Home":
    st.title("Photo Fission")
    st.write("This app is used to sort the images of any sport based on the team and jersey number.")

    # Image upload
    uploaded_files = st.file_uploader("Choose images...", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

    if uploaded_files:
        for file in uploaded_files:
            image = Image.open(file)
            st.image(image, caption=f"Uploaded Image: {file.name}")

    # Sorting type
    sorting_type = st.radio("Sorting Type", ["Team Name", "Jersey Number"], index=0)
    if sorting_type == "Team Name":
        TYPE = "Team Name"
    else:
        TYPE = "Jersey Number"
        
    if st.button("Sort Image"):
        if TYPE:
            if uploaded_files:
                st.success(f"Image sorted based on {TYPE}")
                # You can save the image like this if you want:
                # save_path = os.path.join("sorted_images", team, str(jersey_number))
                # os.makedirs(save_path, exist_ok=True)
                # image.save(os.path.join(save_path, file.name))
            else:
                st.error("Please select files!!")
        else:
            st.error("Please enter both team and jersey number to sort the image.")

elif navigation == "📞 Contact Us":
    st.title("📞 Contact Us")
    st.write("Have a question or feedback? Drop us a message!")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Message")

        submitted = st.form_submit_button("Send Message")

        if submitted:
            if name and email and message:
                respData = requests.post("http://0.0.0.0:8000/send_msg", data={"name":name, "email": email, "message": message})
                st.success("Thanks for contacting us! We'll get back to you soon.")
                # You can also add logic to send this data to an email or API
            else:
                st.error("Please fill out all fields before submitting.")

elif navigation == "ℹ️ About":
    st.title("About Photo Fission")
    st.write("Photo Fission is an AI-powered sports image sorting app built with Streamlit and FastAPI.")
