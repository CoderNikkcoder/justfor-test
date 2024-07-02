from flask import Flask, request, jsonify
from mongo_config import init_mongo, mongo
from user_model import User
from bson.objectid import ObjectId

app = Flask(__name__)
init_mongo(app)

# Create a new user
@app.route("/users", methods=["POST"])
def add_user():
    user = User(**request.json)
    result = mongo.db.users.insert_one(user.to_dict())
    return jsonify(str(result.inserted_id)), 201

# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = mongo.db.users.find()
    result = []
    for user in users:
        user["_id"] = str(user["_id"])
        result.append(user)
    return jsonify(result)

# Get a user by ID
@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

# Update a user by ID
@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user = User(**request.json)
    result = mongo.db.users.update_one({"_id": ObjectId(id)}, {"set": user.to_dict()})
    if result.matched_count:
        return jsonify({"succesfully Updated": True})
    else:
        return jsonify({"error": "User not found"}), 404

# Delete a user by ID
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    result = mongo.db.users.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"succesfully Deleted": True})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)