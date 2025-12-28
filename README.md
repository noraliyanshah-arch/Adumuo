# Adumuo - Aduan Rakyat Muo

Modern municipal complaint system for Majlis Perbandaran Muar (MPM).

## 🎯 Project Overview

Adumuo is a digital platform that enables citizens to submit and track complaints to the Majlis Perbandaran Muar. Built with modern web technologies and a professional "Muar-Modern" design aesthetic.

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
- **Design:** Royal Blue (#002366) & Gold (#D4AF37) color scheme with glassmorphism

## 📋 Features

- ✅ Submit complaints with multi-step form
- ✅ Generate unique Reference IDs (MPM-2025-XXXX)
- ✅ Track complaint status with visual timeline
- ✅ Mobile-first responsive design
- ✅ n8n webhook integration ready

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   cd "MUAR APP"
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   createdb adumuo
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

6. **Run the backend server**
   ```bash
   cd backend
   python main.py
   ```
   The API will be available at `http://localhost:8000`

7. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Or serve it using a local server:
     ```bash
     # Using Python
     cd frontend
     python -m http.server 8080
     ```

## 📡 API Endpoints

### Create Complaint
```
POST /api/complaints
Content-Type: application/json

{
  "citizen_name": "Ahmad bin Abdullah",
  "category": "Infrastruktur",
  "description": "Pothole on Jalan Abdullah",
  "image_url": "https://example.com/image.jpg",
  "latitude": 2.0442,
  "longitude": 102.5689
}
```

### Get Complaint Status
```
GET /api/complaints/{ref_id}
```

### List All Complaints (Admin)
```
GET /api/complaints?skip=0&limit=100
```

## 🔗 n8n Integration

The API endpoints are designed to work seamlessly with n8n webhooks. Simply configure your n8n workflow to POST to `/api/complaints` with the same JSON structure.

Example n8n HTTP Request node:
- Method: POST
- URL: `http://your-server:8000/api/complaints`
- Body: JSON with complaint data

## 🗄️ Database Schema

```sql
CREATE TABLE complaints (
    id SERIAL PRIMARY KEY,
    ref_id VARCHAR(50) UNIQUE NOT NULL,
    citizen_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(500),
    latitude FLOAT,
    longitude FLOAT,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🎨 Design System

- **Primary Color:** Royal Blue (#002366)
- **Accent Color:** Gold (#D4AF37)
- **Font:** Inter
- **Style:** Glassmorphism with rounded corners (2xl)
- **Layout:** Mobile-first responsive design

## 📝 Reference ID Format

Reference IDs follow the format: `MPM-YYYY-XXXX`
- `MPM`: Majlis Perbandaran Muar prefix
- `YYYY`: Current year
- `XXXX`: 4-digit sequential number

Example: `MPM-2025-0001`

## 🔒 Status Values

- `Pending`: Complaint submitted, awaiting assignment
- `Assigned`: Complaint assigned to department/officer
- `Resolved`: Complaint has been resolved

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

This is a municipal project. For contributions, please contact the development team.

## 📄 License

Copyright © 2025 Majlis Perbandaran Muar

## 📞 Support

For technical support or questions, please contact the IT department of Majlis Perbandaran Muar.


