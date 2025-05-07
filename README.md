## 📸 SnapConnect: Instagram Lite Clone

[![Deploy](https://deploy-badge.vercel.app/?url=https://vercel.com/hajra-maliks-projects-8ea01fda/instagram-lite-clone-l972\&name=SnapConnect)](https://vercel.com/hajra-maliks-projects-8ea01fda/instagram-lite-clone-l972)

**SnapConnect** is a lightweight clone of Instagram, designed with scalability and cloud-native technologies in mind. This project serves as a prototype social media platform with post uploads, user management, and cloud storage integration.

### 🚀 Features

* 📷 User authentication and profile management
* 🖼 Upload posts with images to AWS S3
* 📡 Real-time updates via Apache Kafka
* 🗂 MongoDB + DynamoDB + Cassandra for efficient storage
* 🌐 Streamlit-based frontend (planned)
* 🔒 JWT-based authentication
* 🧪 Automated testing with `pytest`

---

### 🛠 Tech Stack

| Layer           | Technology                              |
| --------------- | --------------------------------------- |
| Backend         | FastAPI                                 |
| Database        | MongoDB, Cassandra, AWS DynamoDB        |
| Messaging       | Apache Kafka                            |
| Storage         | AWS S3                                  |
| Frontend        | HTML/CSS (initial), Streamlit (planned) |
| Orchestration   | Apache NiFi, AWS                        |
| Data Processing | Apache Spark, Flink                     |

---

### 📁 Project Structure

```
Instagram-Lite-Clone/
├── backend/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── tests/
│   ├── main.py
│   └── .env
├── frontend/
│   ├── index.html
│   └── followers.html
├── requirements.txt
```

---

### ⚙️ Setup Instructions

#### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r ../requirements.txt
uvicorn main:app --reload
```

> ⚠️ Make sure to set AWS credentials and environment variables in `.env`.

#### 2. Frontend Setup

Open `frontend/index.html` in your browser. Future versions will use Streamlit for UI.

---

### 🧪 Testing

```bash
pytest
```

---

### 📦 Deployment

The application is deployed on Vercel and can be accessed here:

🔗 [Live Demo](https://vercel.com/hajra-maliks-projects-8ea01fda/instagram-lite-clone-l972)

---

### 📚 License

This project is licensed under the MIT License.



