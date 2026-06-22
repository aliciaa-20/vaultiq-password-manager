from auth import register_user as auth_register, login_user as auth_login


class AuthController:
    @staticmethod
    def register(username: str, password: str) -> bool:
        try:
            if not username or len(username.strip()) < 3:
                raise ValueError("Username must be at least 3 characters")
            if not password or len(password) < 8:
                raise ValueError("Password must be at least 8 characters")

            auth_register(username.strip(), password)
            return True
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Registration failed: {e}")

    @staticmethod
    def login(username: str, password: str) -> tuple:
        try:
            if not username or not password:
                raise ValueError("Username and password required")

            user_id, key = auth_login(username, password)
            return user_id, key
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Login failed: {e}")
