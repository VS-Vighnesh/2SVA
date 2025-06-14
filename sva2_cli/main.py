import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
TOTP 2FA Authenticator
A command-line TOTP (Time-based One-Time Password) authenticator
compatible with Google Authenticator and other TOTP apps.
"""

from totp_authenticator.db import Database
from totp_authenticator.totp_core import TOTPManager
from .ui import TOTPInterface

class TOTPApp:
    def __init__(self):
        self.db = Database()
        self.totp = TOTPManager()
        self.ui = TOTPInterface()
    
    def register_user(self):
        """Handle user registration flow"""
        self.ui.console.print()
        username = self.ui.get_username("register")
        
        # Check if user already exists
        if self.db.user_exists(username):
            self.ui.show_error(f"User '{username}' already exists!")
            return
        
        try:
            # Generate TOTP secret and QR code
            secret, provisioning_uri, qr_filename = self.totp.setup_new_user(username)
            
            # Save user to database
            if self.db.add_user(username, secret):
                self.ui.show_success(f"User '{username}' registered successfully!")
                
                # Show QR setup instructions
                self.ui.show_qr_setup(username, qr_filename, provisioning_uri)
                
                # Verify setup by asking for a code
                self.ui.console.print()
                self.ui.show_info("Please scan the QR code and enter the code from your authenticator app to verify setup.")
                
                max_attempts = 3
                for attempt in range(max_attempts):
                    totp_code = self.ui.get_totp_code()
                    
                    if self.totp.verify_totp(secret, totp_code):
                        self.ui.show_success("✅ TOTP verification successful! Your 2FA is now set up.")
                        break
                    else:
                        remaining = max_attempts - attempt - 1
                        if remaining > 0:
                            self.ui.show_error(f"Invalid code. {remaining} attempts remaining.")
                        else:
                            self.ui.show_error("Setup failed. Too many invalid attempts.")
                            # Remove user from database if verification fails
                            # Note: In a real app, you might want to keep the user but mark as unverified
                            return
                
            else:
                self.ui.show_error("Failed to register user.")
                
        except Exception as e:
            self.ui.show_error(f"Registration failed: {str(e)}")
    
    def login_user(self):
        """Handle user login with 2FA"""
        self.ui.console.print()
        username = self.ui.get_username("login")
        
        # Check if user exists
        if not self.db.user_exists(username):
            self.ui.show_error(f"User '{username}' not found!")
            return
        
        # Get user's TOTP secret
        secret = self.db.get_user_secret(username)
        if not secret:
            self.ui.show_error("Failed to retrieve user authentication data.")
            return
        
        # Ask for TOTP code
        max_attempts = 3
        for attempt in range(max_attempts):
            totp_code = self.ui.get_totp_code()
            
            if self.totp.verify_totp(secret, totp_code):
                self.ui.show_success(f"🎉 Welcome back, {username}! Login successful.")
                return
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    self.ui.show_error(f"Invalid TOTP code. {remaining} attempts remaining.")
                else:
                    self.ui.show_error("Login failed. Too many invalid attempts.")
                    return
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                self.ui.show_header()
                
                choice = self.ui.show_menu()
                
                if choice == "1":
                    self.register_user()
                elif choice == "2":
                    self.login_user()
                elif choice == "3":
                    self.ui.show_info("Thank you for using TOTP 2FA Authenticator!")
                    break
                
                self.ui.console.print()
                self.ui.wait_for_enter()
                self.ui.clear_screen()
                
        except KeyboardInterrupt:
            self.ui.console.print("\n")
            self.ui.show_info("Application interrupted by user.")
        except Exception as e:
            self.ui.show_error(f"An unexpected error occurred: {str(e)}")
        finally:
            sys.exit(0)

def main():
    """Entry point of the application"""
    # Start your CLI app here
    app = TOTPApp()
    app.run()

if __name__ == "__main__":
    main()