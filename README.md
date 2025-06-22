# 🛍️ Smart Shopping with AI Recommendation System 🤖

An AI-powered shopping assistant built with **Streamlit**, **FastAPI**, and **Google Gemini AI**, designed to recommend, compare, and calculate EMI for products based on user preferences and budget. This system combines natural language processing, data visualization, and machine learning to deliver a smarter shopping experience.

---

## 🚀 Features

- 🤖 **AI Chatbot (Google Gemini):** Suggests best products based on user query and budget.
- 📊 **Product Comparison:** Compare two products side-by-side.
- 💰 **EMI Calculator:** Instantly calculate monthly EMI based on price, tenure, and interest rate.
- 🧠 **NLP-Powered Queries:** Understands short and long queries like *"Ryzen 5 laptop 16GB RAM 512GB SSD under 50K"*.
- 🎨 **Streamlit UI:** Interactive and visually appealing frontend.
- ⚡ **FastAPI Backend:** Fast and scalable backend API service.
- 📉 **Data Visualization:** EMI results shown in pie charts with Plotly.

---

## 🛠️ Tech Stack

| Layer        | Technology                          |
|--------------|--------------------------------------|
| 💬 Chatbot   | Google Gemini API (`gemini-1.5-flash`) |
| 🌐 Backend   | FastAPI                              |
| 🎨 Frontend  | Streamlit                            |
| 📊 Charts    | Plotly, Matplotlib                   |
| 📁 Data      | Pandas, CSV datasets                 |
| 🔒 Auth      | Session-based (in-memory) Login/Signup |
| 🧪 Testing   | Manual API and UI Testing            |

---

## 📂 Project Structure
Smart_Shopping/
│
├── backend/
│ ├── chatbot_model.py
│ ├── comparison_model.py
│ ├── main.py (FastAPI entry point)
│ ├── data/ (CSV files for products)
│
├── frontend/
│ ├── app.py (Streamlit UI)
│ └── styles/ (optional CSS for custom theming)
│
├── README.md
└── requirements.txt


---

## 🧠 How It Works

1. **User signs up or logs in** using the frontend interface.
2. Selects a feature: 🤖 Chatbot, 🔍 Product Comparison, or 💰 EMI Calculator.
3. The system sends the query to **FastAPI**, which processes it via:
   - Gemini AI for recommendations.
   - Data-driven logic for comparisons.
   - Mathematical formulas for EMI.
4. Returns beautifully formatted, emoji-rich responses via Streamlit.

---

## 🧪 Sample Prompt

```bash
Query: "Suggest a Ryzen 5 laptop with 16GB RAM and 512GB SSD under ₹55000"
🟧 Product 1:
📱 Name: XYZ RyzenBook 15
💰 Price: ₹52,999
💾 RAM/Storage: 16GB/512GB
⚙️ Processor: AMD Ryzen 5 5500U
⭐ Key Features: Backlit Keyboard, Fingerprint Sensor, FHD Display
---


