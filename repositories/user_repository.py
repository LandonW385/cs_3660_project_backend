import json

from models.user_model import User



class UserRepository:
    @staticmethod
    def get_user_by_username(username: str) -> User:
        try:
            with open("./db/users.json", "r") as file:
                data = json.load(file)
                for user in data["users"]:
                    if user["username"] == username:
                        return User(
                            user["username"],
                            user["name"],
                            user["password_hash"],
                            user.get("coins", 0)  # Include coins
                        )
        except FileNotFoundError:
            raise Exception("User file not found")
        return None

    @staticmethod
    def get_user_data(session_id: str) -> dict:
        """
        Fetch user data by session_id.
        """
        try:
            with open("./db/users.json", "r") as file:
                data = json.load(file)
                users = data["users"]

                if session_id not in users:
                    raise KeyError("User not found")

                return users[session_id]
        except FileNotFoundError:
            raise Exception("User file not found")

    @staticmethod
    def save_user_data(username: str, user_data: User):
        """
        Save updated user data to the users.json file.
        """
        try:
            with open("./db/users.json", "r") as file:
                data = json.load(file)

            # Update the user's data
            for user in data["users"]:
                if user["username"] == username:
                    user["coins"] = user_data.coins
                    break

            # Save the updated data back to the file
            with open("./db/users.json", "w") as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            raise Exception("User file not found")

