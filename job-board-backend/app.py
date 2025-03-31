import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)
CORS(app)

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["job_board"]
jobs_collection = db["jobs"]

@app.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = list(jobs_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    return jsonify(jobs)

@app.route("/jobs", methods=["POST"])
def post_job():
    data = request.json
    if "title" not in data or "company" not in data:
        return jsonify({"error": "Title and company required"}), 400
    
    jobs_collection.insert_one(data)
    return jsonify({"message": "Job added"}), 201

if __name__ == "__main__":
    app.run(port=5000, debug=True)
