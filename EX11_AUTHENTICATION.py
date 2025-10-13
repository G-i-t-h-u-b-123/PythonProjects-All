import hashlib
import os


class FileAuthenticator:
    def __init__(self, filename):
        self.filename = filename
        self.users = {}  # Store username: hashed_password pairs


    def register_user(self, username, password):
        # Hash the password before storing
        hashed_password = self._hash_password(password)
        self.users[username] = hashed_password
        print(f"User {username} registered successfully.")


    def authenticate(self, username, password):
        if username not in self.users:
            return False
        hashed_password = self._hash_password(password)
        return self.users[username] == hashed_password


    def _hash_password(self, password):
        # Use SHA-256 for hashing
        return hashlib.sha256(password.encode()).hexdigest()


    def access_file(self, username, password):
        if self.authenticate(username, password):
            try:
                with open(self.filename, 'r') as file:
                    content = file.read()
                    print(f"File contents:\n{content}")
            except FileNotFoundError:
                print(f"File {self.filename} not found.")
        else:
            print("Authentication failed. Access denied.")


def main():
    authenticator = FileAuthenticator("secret_file.txt")


    # Register some users
    authenticator.register_user("wptc", "password123")
    authenticator.register_user("admin", "securepass")


    while True:
        print("\n1. Access file")
        print("2. Register new user")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")


        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            authenticator.access_file(username, password)
        elif choice == '2':
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            authenticator.register_user(username, password)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
