from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rpzucupg:AKjhjJ-DnKuIVP2G8ENw_5PdQLDkQZcR@trumpet.db.elephantsql.com/rpzucupg'  # Update with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


# Create tables if they don't exist
with app.app_context():
    db.create_all()


SECRET_KEY = 'random_key'
# Function to generate a JWT token
def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


@app.route("/api/login", methods=["POST"])
def loginapi():
    if request.method == "POST":
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            # Query the database to check if the user exists
            user = User.query.filter_by(email=email, password=password).first()

            if user:
                token = generate_token(user)
                return jsonify({"token": token, "user": user.username}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/api/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        try:
            data = request.get_json()
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # Email validation using regex
            email_pattern = re.compile(r'[^@]+@[^@]+\.[^@]+')
            is_valid_email = re.match(email_pattern, email)
            
            if not is_valid_email:
                return jsonify({"error": "Invalid email address"}), 400

            # Check if the email is already registered
            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                return jsonify({"error": "Email already exists"}), 400

            # Create a new user and add them to the database
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            # Generate a token for the new user
            token = generate_token(new_user)

            return jsonify({"token": token, "user": new_user.username}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

@app.route("/api/post", methods=["POST"])
def create_post():
    if request.method == "POST":
        try:
            data = request.get_json()
            title = data.get("title")
            content = data.get("content")
            user_id = str(data.get("user_id"))  # Convert user_id to a string

            # Check if the user exists
            print("User", user_id)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            new_post = Post(title=title, content=content, user_id=user_id)
            db.session.add(new_post)
            db.session.commit()

            return jsonify({"message": "Post created successfully", "post_id": new_post.id}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/api/comment", methods=["POST"])
def create_comment():
    if request.method == "POST":
        try:
            data = request.get_json()
            text = data.get("text")
            user_id = str(data.get("user_id"))  # The ID of the user posting the comment
            post_id = str(data.get("post_id") ) # The ID of the post being commented on

            # Check if the user and post exist
            if not user_id or not post_id:
                return jsonify({"error": "User or post not found"}), 404

            new_comment = Comment(text=text, user_id=user_id, post_id=post_id)
            db.session.add(new_comment)
            db.session.commit()

            return jsonify({"message": "Comment posted successfully", "comment_id": new_comment.id}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(port=5000)
