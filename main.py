from flask import Flask, request, jsonify
import time

app = Flask(__name__)
current_time = time.strftime("%Y-%m-%d %H:%M:%S")
current_year = int(time.strftime("%Y"))
user_list = [{"user_name" : "amin", "user_age" : "17"}]

#? main route
@app.route("/")
def index():
    return "Welcome to the Flask App!"

#? get all users
@app.route("/users")
def get_users():
    return jsonify(user_list)

#? get user by name
@app.route("/users/<string:user_name>")
def get_user(user_name):
    return jsonify([user for user in user_list if user.get("user_name") == user_name])

#? create new user
@app.route("/login", methods=["POST"])
def user_login():
    user_json = request.get_json()
    try:
        user_name = user_json["user_name"]
        user_age = user_json["user_age"]
    except:
        return "invalid input!."
    
    user_list.append({"user_name": user_name, "user_age": user_age})
    return "success"

#? update user
@app.route("/users/<string:user_name>", methods=["PUT"])
def update_user(user_name):
    user_json = request.get_json()
    try:
        new_user_name = user_json["user_name"]
        new_user_age = user_json["user_age"]
    except:
        return "invalid input!."
    
    updated = False
    for user in user_list:
        if user.get("user_name") == user_name:
            user["user_age"] = new_user_age
            user["user_name"] = new_user_name
            updated = True
            break

    if updated:
        return "success"
    else:
        return "user not found", 404

#? delete user
@app.route("/logout", methods=["DELETE"])
def user_logout():
    user_json = request.get_json()
    try:
        user_name = user_json["user_name"]
    except:
        return "invalid input!."
    
    global user_list
    user_list = [user for user in user_list if user.get("user_name") != user_name]
    return "success"

#? get current time
@app.route("/time")
def get_time():
    return jsonify({"current_time": current_time})

#? age calculator
@app.route("/age")
def age_calculator():
    user_json = request.get_json()
    try:
        user_birth_year = user_json["birth_year"]
        user_name = user_json["name"]
    except:
        return "invalid input!."
    
    user_age = current_year - user_birth_year
    return f"{user_name} age is: {user_age}"

if __name__ == '__main__':
    app.run(debug=True)