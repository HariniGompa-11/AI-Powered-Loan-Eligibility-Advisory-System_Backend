import random
import string

def generate_otp(length: int = 6) -> str:
    """Generate a random OTP of specified length."""
    return ''.join(random.choices(string.digits, k=length))

def verify_otp(stored_otp: str, input_otp: str) -> bool:
    """Verify if the input OTP matches the stored OTP."""
    return stored_otp == input_otp
