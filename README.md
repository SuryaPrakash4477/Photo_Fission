# 📸 Photo Fission

Photo Fission is an intelligent image sorting application for sports photography. It automatically analyzes images containing players from different teams, classifies them based on the number of players from each team or jersey numbers, and organizes them into appropriate folders.

---

## 🚀 Overview

Photo Fission helps automate the sorting of sports images based on two criteria:

1. Team Dominance (For Example Cricket):  
   The system identifies players from each team in a photo. If more players from Team India are present than Team Australia, the image will be moved to the India folder, and vice versa.

2. Jersey Number-Based Classification (Optional):  
   Users can opt to sort images based on individual players' **jersey numbers**. All images of a player with the same jersey number will be grouped into their own folder.

This system is useful for sports analysts, photographers, and fans who want to keep their photo collections organized based on team appearances or player-specific highlights.

---

## 💻 Tech Stack

### 🖼️ Frontend

- Built using [Streamlit](https://streamlit.io/) for a fast, interactive UI.
- Users can upload images, choose sorting preferences (team vs jersey number), and view the organized folders.

### 🧠 Backend

- Developed with [FastAPI](https://fastapi.tiangolo.com/) for high-performance, asynchronous API services.
- Responsible for image analysis, player detection, team identification, and sorting logic.

---

## 📂 Folder Structure (Example)

```
photo_fission/
├── frontend/                # Streamlit UI
├── backend/                 # FastAPI application
├── sorted_photos/
│   ├── India/
│   ├── Australia/
│   ├── 7/                  # Jersey number folders (optional)
│   └── 10/
└── README.md
```

---

## ⚙️ Features

- ✅ Upload single or multiple sports images.
- ✅ Automatically detect and classify players.
- ✅ Sort images into folders based on:
  - Team majority (e.g., India or Australia)
  - Player jersey numbers (optional)
- ✅ Clean and interactive UI
- ✅ Fast and scalable backend API

---

## 📌 Future Improvements

- Add support for more sports and teams.
- Improve detection accuracy using deep learning models.
- Add manual override and tagging features.

---

## 🏁 Getting Started

1. Clone the repository 
   ```bash
   git clone https://github.com/yourusername/photo-fission.git
   cd photo-fission
   ```

2. Start the Backend (FastAPI)
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. Start the Frontend (Streamlit)
   ```bash
   cd frontend
   streamlit run app.py
   ```

---

## 📬 Contact

For any feedback or queries, feel free to reach out!

---
