# import os
# from pathlib import Path
# from typing import List, Optional
# import aiofiles
# from cryptography.fernet import Fernet
# from dotenv import load_dotenv  # ✅ For .env file loading

# # -----------------------------------------------------
# # Load environment variables (.env)
# # -----------------------------------------------------
# load_dotenv()

# # -----------------------------------------------------
# # Upload Directory Setup
# # -----------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent
# UPLOAD_DIR = BASE_DIR / "static" / "uploads"
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# # -----------------------------------------------------
# # Environment Variable Helper
# # -----------------------------------------------------
# def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
#     """Fetch environment variable safely."""
#     return os.getenv(key, default)

# # -----------------------------------------------------
# # File Upload Helpers
# # -----------------------------------------------------
# async def save_upload_file(upload_file, dest_filename: str) -> str:
#     """Save a single uploaded file and return its relative path."""
#     dest_path = UPLOAD_DIR / dest_filename
#     async with aiofiles.open(dest_path, "wb") as out_file:
#         content = await upload_file.read()
#         await out_file.write(content)
#     # Return relative path for database saving
#     return str(dest_path.relative_to(BASE_DIR))

# async def save_multiple_files(files) -> List[str]:
#     """Save multiple uploaded files and return list of relative paths."""
#     paths = []
#     for file in files:
#         file_name = f"{int(__import__('time').time())}_{file.filename}"
#         saved_path = await save_upload_file(file, file_name)
#         paths.append(saved_path)
#     return paths

# # -----------------------------------------------------
# # Encryption Helpers
# # -----------------------------------------------------
# def get_fernet_key() -> str:
#     key = os.getenv("FERNET_KEY")
#     if not key:
#         raise ValueError("❌ FERNET_KEY not configured in .env file.")
#     return key

# def get_fernet(key: Optional[str] = None):
#     key = key or get_fernet_key()
#     key_bytes = key.encode() if isinstance(key, str) else key
#     return Fernet(key_bytes)

# def encrypt_password(key: Optional[str], plaintext: str) -> str:
#     f = get_fernet(key)
#     return f.encrypt(plaintext.encode()).decode()

# def decrypt_password(key: Optional[str], token: str) -> str:
#     f = get_fernet(key)
#     return f.decrypt(token.encode()).decode()






import os
from pathlib import Path
from typing import List, Optional
import aiofiles
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import time

# -----------------------------------------------------
# Load environment variables (.env)
# -----------------------------------------------------
load_dotenv()

# -----------------------------------------------------
# Upload Directory Setup
# -----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"

# ✅ Ensure upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------
# Environment Variable Helper
# -----------------------------------------------------
def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Fetch environment variable safely."""
    return os.getenv(key, default)

# -----------------------------------------------------
# File Upload Helpers
# -----------------------------------------------------
async def save_upload_file(upload_file, dest_filename: Optional[str] = None) -> str:
    """Save a single uploaded file and return its relative path (clickable)."""
    if not upload_file:
        return None

    # Ensure unique filename
    filename = dest_filename or f"{int(time.time())}_{upload_file.filename}"
    dest_path = UPLOAD_DIR / filename

    async with aiofiles.open(dest_path, "wb") as out_file:
        content = await upload_file.read()
        await out_file.write(content)

    # ✅ Return relative path (this works with /static mount)
    return f"static/uploads/{filename}"


async def save_multiple_files(files) -> List[str]:
    """Save multiple uploaded files and return list of relative paths."""
    if not files:
        return []
    paths = []
    for file in files:
        file_name = f"{int(time.time())}_{file.filename}"
        saved_path = await save_upload_file(file, file_name)
        paths.append(saved_path)
    return paths

# -----------------------------------------------------
# Encryption Helpers
# -----------------------------------------------------
def get_fernet_key() -> str:
    """Retrieve Fernet key from environment variables."""
    key = os.getenv("FERNET_KEY")
    if not key:
        raise ValueError("❌ FERNET_KEY not configured in .env file.")
    return key


def get_fernet(key: Optional[str] = None):
    """Return Fernet instance."""
    key = key or get_fernet_key()
    key_bytes = key.encode() if isinstance(key, str) else key
    return Fernet(key_bytes)


def encrypt_password(key: Optional[str], plaintext: str) -> str:
    """Encrypt plain text password."""
    f = get_fernet(key)
    return f.encrypt(plaintext.encode()).decode()


def decrypt_password(key: Optional[str], token: str) -> str:
    """Decrypt previously encrypted password."""
    f = get_fernet(key)
    return f.decrypt(token.encode()).decode()
