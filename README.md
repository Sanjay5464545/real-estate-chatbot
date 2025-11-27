# 🏠 Real Estate Analysis Chatbot

An AI-powered real estate market analysis chatbot that provides intelligent insights on property trends, pricing, and market comparisons using **Groq's Llama 3.3 (70B)** model.

![React](https://img.shields.io/badge/React-18.x-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![AI](https://img.shields.io/badge/AI-Groq_Llama_3.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌐 Live Demo

- **Frontend:** [https://real-estate-chatbot-git-main-sanjays-projects-7a11b0da.vercel.app](https://real-estate-chatbot-git-main-sanjays-projects-7a11b0da.vercel.app)
- **Backend API:** [https://real-estate-chatbot-mxfl.onrender.com/api/analyze/](https://real-estate-chatbot-mxfl.onrender.com/api/analyze/)

## ✨ Features

- 🤖 **AI-Powered Analysis** - Powered by Groq's Llama 3.3 70B parameter model
- 📊 **Interactive Charts** - Visual price trend analysis with Chart.js
- 📈 **Data Tables** - Detailed real estate data presentation
- 🔍 **Area Comparison** - Compare multiple locations side-by-side
- 💬 **Conversational UI** - Natural language interaction
- 📱 **Responsive Design** - Works seamlessly on all devices
- ⚡ **Real-time Processing** - Instant AI responses with Excel data integration

## 🚀 Tech Stack

### Frontend
- **React** - UI framework
- **Bootstrap** - Responsive styling
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **Deployed on Vercel**

### Backend
- **Django** - Web framework
- **Django REST Framework** - API development
- **Pandas** - Data processing
- **Openpyxl** - Excel file handling
- **Groq API** - AI model integration
- **Deployed on Render**

### AI Model
- **Groq Llama 3.3 70B Versatile** - Advanced language model for market analysis

## 📋 Prerequisites

- Node.js 16+ and npm
- Python 3.10+
- Groq API Key ([Get one free](https://console.groq.com))

## 🛠️ Installation

### 1. Clone the Repository
git clone https://github.com/Sanjay5464545/real-estate-chatbot.git
cd real-estate-chatbot

text

### 2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt

text

Create `.env` file in `backend/` folder:
GROQ_API_KEY=your_groq_api_key_here

text

Run migrations and start server:
python manage.py migrate
python manage.py runserver

text

Backend will run on `http://127.0.0.1:8000`

### 3. Frontend Setup
cd frontend
npm install
npm start

text

Frontend will run on `http://localhost:3000`

## 📁 Project Structure

real-estate-chatbot/
├── backend/
│ ├── analysis/ # Django app for chatbot logic
│ │ ├── views.py # API endpoints
│ │ └── urls.py
│ ├── realestate_backend/ # Django project settings
│ │ ├── settings.py
│ │ └── urls.py
│ ├── real_estate_data.xlsx # Sample data
│ ├── requirements.txt
│ └── manage.py
│
├── frontend/
│ ├── public/
│ ├── src/
│ │ ├── App.js # Main React component
│ │ ├── App.css # Styles
│ │ └── index.js
│ ├── package.json
│ └── README.md
│
└── README.md

text

## 💻 Usage

### Try These Queries:

1. **General Greeting:**
   - "Hello"
   - "Hi there"

2. **Area Analysis:**
   - "Analyze Wakad"
   - "Show me data for Aundh"
   - "Price trends in Kharadi"

3. **Comparisons:**
   - "Compare Aundh and Baner"
   - "Which is better, Wakad or Akurdi?"

4. **Market Insights:**
   - "Real estate trends in Pune"
   - "Property demand analysis"

## 🔌 API Endpoints

### POST `/api/analyze/`

**Request Body:**
{
"query": "Analyze Wakad"
}

text

**Response:**
{
"success": true,
"summary": "AI-generated market analysis...",
"chart_data": {
"labels": ["2020", "2021", "2022"],
"values":
},
"table_data": [
{
"Area": "Wakad",
"Year": 2022,
"Price": 6000000,
"Total_Sales": 150
}
]
}

text

## 🌍 Deployment

### Frontend (Vercel)
1. Push code to GitHub
2. Import project to Vercel
3. Set Root Directory: `frontend`
4. Deploy

### Backend (Render)
1. Create new Web Service
2. Connect GitHub repo
3. Set Root Directory: `backend`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn realestate_backend.wsgi:application`
6. Add Environment Variable: `GROQ_API_KEY`

## 🔐 Environment Variables

### Backend (.env)
GROQ_API_KEY=your_groq_api_key

text

## 📊 Sample Data Format

Excel file should contain:
- Area/Location
- Year
- Price/Total_Sales
- Other relevant real estate metrics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Sanjay**
- GitHub: [@Sanjay5464545](https://github.com/Sanjay5464545)

## 🙏 Acknowledgments

- Groq for providing the Llama 3.3 AI model API
- Sigmavalue for the assignment opportunity
- React and Django communities

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ and ☕ for Sigmavalue Full Stack Developer Assignment