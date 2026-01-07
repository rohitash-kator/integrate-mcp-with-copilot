"""
High School Management System API

A FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

Uses MongoDB for persistent data storage.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from bson.objectid import ObjectId
from datetime import datetime

from database import connect_to_mongo, close_mongo_connection, get_database, init_collections
from models import Activity, SignupResponse

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    connect_to_mongo()
    init_collections()
    print("✓ Application started - MongoDB connected")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    close_mongo_connection()
    print("✓ Application shutdown - MongoDB connection closed")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Get all activities from MongoDB."""
    db = get_database()
    activities_data = {}
    
    try:
        # Fetch all activities from MongoDB
        for activity in db.activities.find():
            activity_name = activity["name"]
            activities_data[activity_name] = {
                "description": activity["description"],
                "schedule": activity["schedule"],
                "max_participants": activity["max_participants"],
                "participants": activity.get("participants", [])
            }
        
        return activities_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch activities: {str(e)}")


@app.post("/activities/{activity_name}/signup", response_model=SignupResponse)
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity in MongoDB."""
    db = get_database()
    
    try:
        # Find the activity
        activity = db.activities.find_one({"name": activity_name})
        
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        # Check if student is already signed up
        if email in activity.get("participants", []):
            raise HTTPException(
                status_code=400,
                detail="Student is already signed up"
            )
        
        # Check if activity is full
        max_participants = activity["max_participants"]
        current_participants = len(activity.get("participants", []))
        
        if current_participants >= max_participants:
            raise HTTPException(
                status_code=400,
                detail="Activity is at maximum capacity"
            )
        
        # Add student to activity
        db.activities.update_one(
            {"name": activity_name},
            {
                "$push": {"participants": email},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return SignupResponse(
            message=f"Signed up {email} for {activity_name}",
            activity_name=activity_name,
            email=email
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")


@app.delete("/activities/{activity_name}/unregister", response_model=SignupResponse)
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity in MongoDB."""
    db = get_database()
    
    try:
        # Find the activity
        activity = db.activities.find_one({"name": activity_name})
        
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        # Check if student is signed up
        if email not in activity.get("participants", []):
            raise HTTPException(
                status_code=400,
                detail="Student is not signed up for this activity"
            )
        
        # Remove student from activity
        db.activities.update_one(
            {"name": activity_name},
            {
                "$pull": {"participants": email},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return SignupResponse(
            message=f"Unregistered {email} from {activity_name}",
            activity_name=activity_name,
            email=email
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unregister failed: {str(e)}")
