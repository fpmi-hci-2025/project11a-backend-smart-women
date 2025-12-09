from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# База данных в памяти для демо
courses_db = [
    {"id": 1, "title": "Python для начинающих", "duration": "40 часов", "level": "Начальный"},
    {"id": 2, "title": "Анализ данных с Pandas", "duration": "60 часов", "level": "Средний"},
    {"id": 3, "title": "Веб-разработка на Flask", "duration": "50 часов", "level": "Средний"}
]

users_db = [
    {"id": 1, "name": "Анна", "email": "anna@example.com", "role": "student"},
    {"id": 2, "name": "Михаил", "email": "mikhail@example.com", "role": "professional"}
]

@app.route('/')
def home():
    return jsonify({
        "message": "OnLearn API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "courses": "/api/courses",
            "users": "/api/users"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "OnLearn Backend API",
        "timestamp": "2024-01-01T12:00:00Z"
    })

@app.route('/api/courses', methods=['GET'])
def get_courses():
    return jsonify({
        "count": len(courses_db),
        "courses": courses_db
    })

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if course:
        return jsonify(course)
    return jsonify({"error": "Course not found"}), 404

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({
        "count": len(users_db),
        "users": users_db
    })

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    new_user = {
        "id": len(users_db) + 1,
        "name": data['name'],
        "email": data['email'],
        "role": data.get('role', 'student')
    }
    users_db.append(new_user)
    
    return jsonify({
        "message": "User registered successfully",
        "user": new_user
    }), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)