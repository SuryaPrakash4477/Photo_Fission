import streamlit as st
from PIL import Image
import os
import requests
from io import BytesIO
from datetime import datetime

# Load logo
logo_path = os.path.join("..", "Images", "logo.png")
logo = Image.open(logo_path)

# Page config
st.set_page_config(page_title="Photo Fission", layout="wide")

# Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "sorting_type" not in st.session_state:
    st.session_state.sorting_type = None

# Sidebar (Navbar)
with st.sidebar:
    st.image(logo, width=100)
    st.title("Photo Fission")
    navigation = st.radio("Navigate", ["🏠 Home", "📞 Contact Us", "ℹ️ About"])

# Main section based on navigation
if navigation == "🏠 Home":
    st.title("Photo Fission")
    st.write("This app is used to sort the images of any sport based on the team and jersey number.")

    uploaded_files = st.file_uploader("Choose images...", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files

    # Optional preview
    if st.checkbox("Preview uploaded images"):
        for file in st.session_state.uploaded_files:
            image = Image.open(file)
            st.image(image, caption=f"Uploaded: {file.name}", use_column_width=True)

    # Sorting type
    sorting_type = st.radio("Sorting Type", ["Team Name", "Jersey Number"], index=None)
    st.session_state.sorting_type = sorting_type

    if st.button("Sort Image"):
        if not st.session_state.sorting_type:
            st.error("Please select sorting type!!")
        elif not st.session_state.uploaded_files:
            st.error("Please select files!!")
        else:
            with st.spinner("Uploading and sorting images..."):
                compressed_files = []
                for file in st.session_state.uploaded_files:
                    img = Image.open(file)
                    buffer = BytesIO()
                    img.convert("RGB").save(buffer, format="JPEG", quality=70)
                    buffer.seek(0)
                    compressed_files.append(("files", (file.name, buffer, "image/jpeg")))

                try:
                    resp = requests.post("http://localhost:8000/team_name", files=compressed_files)
                    if resp.status_code == 200:
                        st.success(f"{resp.json()['msg']}. Images sorted by {st.session_state.sorting_type}")
                    else:
                        st.error(f"Error: {resp.status_code} - {resp.text}")
                except Exception as e:
                    st.error(f"Request failed: {str(e)}")

elif navigation == "📞 Contact Us":
    st.title("📞 Contact Us")
    st.write("Have a question or feedback? Drop us a message!")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send")

        if submitted:
            if name and email and message:
                with st.spinner("Sending your message..."):
                    try:
                        response = requests.post(
                            "http://localhost:8000/send_msg",
                            json={"name": name, "email": email, "message": message}
                        )
                        if response.status_code == 200:
                            st.success("✅ Thank you! Your message has been sent.")
                            print(datetime.now().strftime("%H:%M:%S"))
                        else:
                            st.error(f"❌ Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ Failed to send: {str(e)}")
            else:
                st.warning("⚠️ Please fill all fields.")

elif navigation == "ℹ️ About":
    st.title("About Photo Fission")
    st.write("Photo Fission is an AI-powered sports image sorting app built with Streamlit and FastAPI.")
