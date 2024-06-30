from flask import Blueprint, request, make_response
from flask import jsonify
from ..services.user import signup, login, token_required, get_user_info_from_token , add_user ,delete_user, validate_user,get_moderators , get_users, update_user
from ..models.user import Users

user_routes = Blueprint('user_routes', __name__)

@user_routes.route("/signup", methods=["POST"])
def signup_route():
    data = request.json
    response, status_code = signup(data)
    return make_response(response, status_code)

@user_routes.route("/login", methods=["POST"])
def login_route():
    auth = request.json
    response, status_code = login(auth)
    return make_response(response, status_code)


@user_routes.route("/user-info", methods=["GET"])
def get_user_info_route():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token is missing"}), 401
    
    user_info = get_user_info_from_token(token)
    
    if isinstance(user_info, Users):
        # Convert the user object to a dictionary
        user_dict = {
            "id": user_info.id,
            "username": user_info.username,
            "email": user_info.email,
            "role": user_info.role.value,
            "phoneNumber": user_info.phoneNumber
        }
        return jsonify(user_dict), 200
    else:
        return jsonify({"message": user_info}), 401




@user_routes.route("/add-user", methods=["POST"])
def add_user_route():
    data = request.json
    response = add_user(data)
    return make_response(response)

@user_routes.route("/delete-user/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    response = delete_user(user_id)
    return make_response(response)

@user_routes.route("/validate-user/<int:user_id>", methods=["PUT"])
def validate_user_route(user_id):
    response = validate_user(user_id)
    return make_response(response)

@user_routes.route("/moderators", methods=["GET"])
def get_moderators_route():
    response_data = get_moderators()
    return make_response(response_data)

@user_routes.route("/users", methods=["GET"])
def get_users_route():
    response_data = get_users()
    return make_response(response_data)


@user_routes.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.json

    if update_user(user_id, data):
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "Failed to update user"}), 500