import streamlit as st
from PIL import Image
import os
import requests
from io import BytesIO
from datetime import datetime
import base64
import time
import io
from zipfile import ZipFile

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
if "sorted_images" not in st.session_state:
    st.session_state.sorted_images = {}
if "current_path" not in st.session_state:
    st.session_state.current_path = []

# Utility: download link for individual image
def generate_download_link(file_name, b64_data):
    href = f'<a href="data:image/jpeg;base64,{b64_data}" download="{file_name}">📥 Download</a>'
    return href

# Utility: recursive folder renderer
def render_folder(folder, path=[]):
    st.markdown("### 📁 Explorer")
    
    if path:
        if st.button("🔙 Go Back"):
            st.session_state.current_path = path[:-1]
            st.rerun()
            return
    image_entries = []
    for key, value in folder.items():
        full_path = path + [key]
        if isinstance(value, dict):
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button("📂 " + key, key="/".join(full_path)):
                    st.session_state.current_path = full_path
                    st.rerun()
            with col2:
                if st.button("📦", key="zip_" + "/".join(full_path)):
                    buffer = io.BytesIO()
                    with ZipFile(buffer, "w") as zip_file:
                        def add_to_zip(subfolder, path_prefix):
                            for name, item in subfolder.items():
                                if isinstance(item, dict):
                                    add_to_zip(item, path_prefix + [name])
                                else:
                                    image_bytes = base64.b64decode(item)
                                    filename = "/".join(path_prefix + [name])
                                    zip_file.writestr(filename, image_bytes)
                        add_to_zip(value, full_path)
                    buffer.seek(0)
                    b64 = base64.b64encode(buffer.read()).decode()
                    href = f'<a href="data:application/zip;base64,{b64}" download="{key}.zip">📥 Download ZIP</a>'
                    st.markdown(href, unsafe_allow_html=True)
        else:
            image_entries.append((key, value, full_path))
        # Grid display for images
    if image_entries:
        st.markdown("### 🖼️ Images")
        cols = st.columns(4)
        for idx, (name, b64_img, full_path) in enumerate(image_entries):
            with cols[idx % 4]:
                img = Image.open(BytesIO(base64.b64decode(b64_img)))
                st.image(img, caption="/".join(full_path))
                href = generate_download_link(name, b64_img)
                st.markdown(href, unsafe_allow_html=True)

# Sidebar (Navbar)
with st.sidebar:
    st.image(logo, width=100)
    st.title("Photo Fission")
    navigation = st.radio("Navigate", ["🏠 Home", "📁 Explorer", "📞 Contact Us", "ℹ️ About"])

# Main sections
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
            st.image(image, caption=f"Uploaded: {file.name}")

    # Sorting type
    sorting_type = st.radio("Sorting Type", ["Team Name", "Jersey Number"], index=None)
    st.session_state.sorting_type = sorting_type

    if st.button("Sort Image"):
        if not st.session_state.sorting_type or not st.session_state.uploaded_files:
            st.error("Select sorting type and files!")
        else:
            with st.spinner("Uploading and sorting images..."):
                files = []
                for file in st.session_state.uploaded_files:
                    files.append(("files", (file.name, file, "image/jpeg")))
                # print(files)
                if st.session_state.sorting_type == "Team Name":
                    resp = requests.post("http://localhost:8000/team_name", files=files)
                    task_id = resp.json()["task_id"]
                elif st.session_state.sorting_type == "Jersey Number":
                    resp = requests.post("http://localhost:8000/jersey_number", files=files)
                    task_id = resp.json()["task_id"] 

                while True:
                    result = requests.get(f"http://localhost:8000/get_images/{task_id}").json()
                    if result["status"] == "done":
                        break
                    time.sleep(1)

                st.session_state.sorted_images = result["images"]
                st.session_state.current_path = []

                st.success("✅ Images sorted and resized!")

if navigation == "📁 Explorer":
    if st.session_state.sorted_images:
        def get_nested_folder(path, folder):
            for p in path:
                folder = folder[p]
            return folder

        nested_folder = get_nested_folder(st.session_state.current_path, st.session_state.sorted_images)
        render_folder(nested_folder, st.session_state.current_path)
    else:
        st.warning("⚠️ No sorted images available. Please upload and sort images first.")

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
