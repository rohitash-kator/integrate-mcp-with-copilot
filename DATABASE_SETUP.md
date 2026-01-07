# Database Integration Guide

This project now uses MongoDB for persistent data storage.

## Setup Instructions

### Prerequisites
- MongoDB installed locally or access to MongoDB Atlas
- Python 3.8+

### Local MongoDB Setup

1. **Install MongoDB** (if not already installed):
   - **macOS**: `brew install mongodb-community`
   - **Ubuntu/Debian**: Follow [official MongoDB installation guide](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
   - **Windows**: Download from [mongodb.com](https://www.mongodb.com/try/download/community)

2. **Start MongoDB**:
   ```bash
   # macOS
   brew services start mongodb-community
   
   # Ubuntu/Linux
   sudo systemctl start mongod
   
   # Windows
   # MongoDB should start automatically after installation
   ```

3. **Verify MongoDB is running**:
   ```bash
   mongosh  # or mongo (older versions)
   ```

### Application Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env if needed (default values should work for local development)
   ```

3. **Initialize and seed the database**:
   ```bash
   python src/seed_db.py
   ```

4. **Run the application**:
   ```bash
   cd src
   python -m uvicorn app:app --reload
   ```

The API will be available at `http://localhost:8000`

## MongoDB Atlas (Cloud)

To use MongoDB Atlas instead:

1. Create a MongoDB Atlas account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster and get your connection string
3. Update `.env`:
   ```
   MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   ```

## Database Schema

### Activities Collection
```json
{
  "_id": ObjectId,
  "name": "Chess Club",
  "description": "Learn strategies and compete in chess tournaments",
  "schedule": "Fridays, 3:30 PM - 5:00 PM",
  "max_participants": 12,
  "participants": ["email1@example.com", "email2@example.com"],
  "created_at": ISODate,
  "updated_at": ISODate
}
```

## API Endpoints

- `GET /activities` - Get all activities
- `POST /activities/{activity_name}/signup?email=` - Sign up for an activity
- `DELETE /activities/{activity_name}/unregister?email=` - Unregister from an activity

## Troubleshooting

**Connection Error**: Make sure MongoDB is running
```bash
# Check MongoDB status
mongosh
```

**Permission Error**: Check MongoDB user credentials in `.env`

**Port Already in Use**: MongoDB default is port 27017. Check if another process is using it.
