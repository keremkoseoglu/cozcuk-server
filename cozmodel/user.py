class User:

    ROLE_ADMIN = "A"
    ROLE_CONSUMER = "C"

    def __init__(self, username: str, password: str, email: str, role: str):
        self._validate_role(role)

        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def ensure_admin(self):
        if not self.is_admin():
            raise Exception("You are not an administrator")

    def get_dict(self) -> {}:
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role
        }

    def is_admin(self) -> bool:
        return self.role == self.ROLE_ADMIN

    def _validate_role(self, role: str):
        if not (role == self.ROLE_ADMIN or role == self.ROLE_CONSUMER):
            raise Exception("Invalid user role: " + role)

