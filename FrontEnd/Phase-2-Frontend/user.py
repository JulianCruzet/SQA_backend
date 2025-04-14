import login_logout
class User:
    """Represents a user in the banking system."""
    
    def __init__(self, user_name: str, user_id: str, user_email: str, user_password: str):
        """Initializes a User instance."""
        self.user_name = user_name
        self.user_id = user_id
        self.user_email = user_email
        self.user_password = user_password
    
    def get_user_info(self):
        """Returns user information excluding the password."""
        return {
            "Account holder's Name": self.user_name,
            "Account holder's Id": self.user_id,
            "Account holder's Email": self.user_email
        }
    
    def authenticate(self, password: str) -> bool:
        """Checks if the provided password matches the user's password."""
        return self.user_password == password

def create_account():
    """Function to create a new user account."""
    user_name = input("Account holder's Name:")
    user_id = input("Account holder's Id:")
    user_email = input("Account holder's Email:")
    user_password = input("Enter User Password:")
    return User(user_name, user_id, user_email, user_password)



def main():
    users = []
    current_user = None
    
    while True:
        print("\n1. Create an Banking Account")
        print("2. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            users.append(create_account())
            print("Bank Account created successfully!")
        
        elif choice == "2":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
