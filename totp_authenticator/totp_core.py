import pyotp
import qrcode
from io import BytesIO
import base64
from typing import Tuple

class TOTPManager:
    def __init__(self, issuer: str = "TOTP Authenticator"):
        self.issuer = issuer
    
    def generate_secret(self) -> str:
        """Generate a new random Base32 secret for TOTP"""
        return pyotp.random_base32()
    
    def generate_provisioning_uri(self, username: str, secret: str) -> str:
        """Generate the provisioning URI for QR code"""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=username,
            issuer_name=self.issuer
        )
    
    def generate_qr_code(self, provisioning_uri: str, filename: str = None) -> str:
        """Generate QR code and save to file or return as ASCII"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        if filename:
            # Save as image file
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return filename
        else:
            # Return ASCII representation
            return self._qr_to_ascii(qr)
    
    def _qr_to_ascii(self, qr) -> str:
        """Convert QR code to ASCII representation"""
        ascii_qr = []
        matrix = qr.get_matrix()
        
        for row in matrix:
            line = ""
            for cell in row:
                line += "██" if cell else "  "
            ascii_qr.append(line)
        
        return "\n".join(ascii_qr)
    
    def verify_totp(self, secret: str, token: str, window: int = 1) -> bool:
        """Verify the TOTP token against the secret"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=window)
        except Exception:
            return False
    
    def get_current_totp(self, secret: str) -> str:
        """Get the current TOTP for testing purposes"""
        totp = pyotp.TOTP(secret)
        return totp.now()
    
    def setup_new_user(self, username: str) -> Tuple[str, str, str]:
        """Complete setup for a new user - returns secret, URI, and QR filename"""
        secret = self.generate_secret()
        provisioning_uri = self.generate_provisioning_uri(username, secret)
        qr_filename = f"qr_{username}.png"
        self.generate_qr_code(provisioning_uri, qr_filename)
        
        return secret, provisioning_uri, qr_filename