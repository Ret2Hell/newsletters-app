Collecting workspace information# Newsletters App Setup Guide

This README explains how to set up and run both the backend (Python/FastAPI) and frontend (Next.js) parts of the Newsletters application.

## Project Structure

```
newsletters-app/
├── backend/          # FastAPI backend
│   ├── app/          # Application code
│   └── requirements.txt
└── frontend/         # Next.js frontend
    └── package.json
```

## Backend Setup

### 1. Create and Activate Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create or update the `.env` file in the backend directory with required configuration:

```
DATABASE_URL=sqlite:///newsletters.db
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the Server

```bash
# Start the FastAPI server
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

## Frontend Setup

### 1. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies with your preferred package manager
npm install
# or
yarn install
# or
pnpm install
# or
bun install
```

### 2. Configure Environment Variables

Create or update the `.env` file in the frontend directory with necessary configuration.

```
NEXT_PUBLIC_BASE_URL=http://127.0.0.1:8000
```

### 3. Start the Development Server

```bash
# Start the Next.js development server
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

The frontend will be available at http://localhost:3000

## Accessing the Application

- Frontend: http://localhost:3000
- Backend API: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs
