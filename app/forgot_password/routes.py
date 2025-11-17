# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# import jwt
# from passlib.context import CryptContext
# from app.database import get_db
# from app.signup.models import User
# from app.forgot_password.models import PasswordResetToken
# from app.forgot_password.schemas import ForgotPasswordRequest, ResetPasswordRequest
# from app.utils.email_service import send_reset_email

# import os
# from dotenv import load_dotenv

# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
# ALGORITHM = "HS256"

# router = APIRouter(tags=["Forgot Password"])

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # ----------------------------------------------------
# # 1️⃣ Request Password Reset
# # ----------------------------------------------------
# @router.post("/forgot-password/request")
# def request_password_reset(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == request.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Generate token valid for 15 minutes
#     token_data = {
#         "sub": user.email,
#         "exp": datetime.utcnow() + timedelta(minutes=15)
#     }
#     token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

#     # Store token in DB
#     reset_entry = PasswordResetToken(
#         user_id=user.id,
#         token=token,
#         expires_at=datetime.utcnow() + timedelta(minutes=15)
#     )
#     db.add(reset_entry)
#     db.commit()

#     # Send email
#     reset_link = f"http://localhost:8888/forgot-password/reset/{token}"
#     send_reset_email(user.email, reset_link)

#     return {"message": "Password reset link sent to your email"}

# # ----------------------------------------------------
# # 2️⃣ Reset Password
# # ----------------------------------------------------
# @router.post("/forgot-password/reset/{token}")
# def reset_password(token: str, request: ResetPasswordRequest, db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#         if not email:
#             raise HTTPException(status_code=400, detail="Invalid token")
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Reset link expired")
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=400, detail="Invalid reset link")

#     # Get user
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Validate token record
#     token_record = db.query(PasswordResetToken).filter(
#         PasswordResetToken.token == token
#     ).first()
#     if not token_record or token_record.expires_at < datetime.utcnow():
#         raise HTTPException(status_code=400, detail="Reset link invalid or expired")

#     # Update password
#     hashed_password = pwd_context.hash(request.new_password)
#     user.password = hashed_password
#     db.commit()

#     return {"message": "Password reset successful"}


# from fastapi import APIRouter, Depends, HTTPException, Form
# from fastapi.responses import HTMLResponse
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# from app.database import get_db
# from app.signup.models import User
# from app.utils.email_service import send_reset_email
# from passlib.context import CryptContext
# from pydantic import BaseModel
# import os

# router = APIRouter(tags=["Forgot Password"])

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")
# ALGORITHM = "HS256"

# # ------------------------------------------------------------------------------
# # 1️⃣  Schema for forgot password request
# # ------------------------------------------------------------------------------
# class ForgotPasswordRequest(BaseModel):
#     email: str


# # ------------------------------------------------------------------------------
# # 2️⃣  API to send reset link via email
# # ------------------------------------------------------------------------------
# @router.post("/forgot-password/request")
# async def request_password_reset(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == data.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="Email not found")

#     # create JWT token (valid for 30 minutes)
#     token_data = {"sub": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)}
#     token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

#     reset_link = f"http://127.0.0.1:8888/forgot-password/reset?token={token}"
#     send_reset_email(user.email, reset_link)
#     return {"message": "Reset link sent successfully!"}


# # ------------------------------------------------------------------------------
# # 3️⃣  Show reset password HTML form (GET)
# # ------------------------------------------------------------------------------
# @router.get("/forgot-password/reset")
# async def show_reset_form(token: str):
#     html_content = f"""
#     <html>
#         <head>
#             <title>Reset Password</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     background-color: #f4f4f4;
#                     padding: 40px;
#                     display: flex;
#                     justify-content: center;
#                 }}
#                 form {{
#                     background-color: white;
#                     padding: 30px;
#                     border-radius: 10px;
#                     box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#                     width: 300px;
#                 }}
#                 input {{
#                     width: 100%;
#                     padding: 8px;
#                     margin: 6px 0;
#                     border: 1px solid #ccc;
#                     border-radius: 5px;
#                 }}
#                 button {{
#                     background-color: #007bff;
#                     color: white;
#                     padding: 10px 20px;
#                     border: none;
#                     border-radius: 5px;
#                     cursor: pointer;
#                     width: 100%;
#                 }}
#                 button:hover {{
#                     background-color: #0056b3;
#                 }}
#             </style>
#         </head>
#         <body>
#             <form action="/forgot-password/reset" method="post">
#                 <h2>Reset Your Password</h2>
#                 <input type="hidden" name="token" value="{token}">
#                 <label>New Password:</label><br>
#                 <input type="password" name="new_password" required><br><br>
#                 <label>Confirm Password:</label><br>
#                 <input type="password" name="confirm_password" required><br><br>
#                 <button type="submit">Reset Password</button>
#             </form>
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)


# # ------------------------------------------------------------------------------
# # 4️⃣  Handle form submission and update password (POST)
# # ------------------------------------------------------------------------------
# @router.post("/forgot-password/reset")
# async def reset_password(
#     token: str = Form(...),
#     new_password: str = Form(...),
#     confirm_password: str = Form(...),
#     db: Session = Depends(get_db),
# ):
#     if new_password != confirm_password:
#         return HTMLResponse("<h3>❌ Passwords do not match</h3>")

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#     except JWTError:
#         return HTMLResponse("<h3>❌ Invalid or expired token</h3>")

#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         return HTMLResponse("<h3>❌ User not found</h3>")

#     # Update the user's password
#     user.password = pwd_context.hash(new_password)
#     db.commit()

#     return HTMLResponse("<h3>✅ Password reset successful! You can close this tab.</h3>")


# from fastapi import APIRouter, Depends, HTTPException, Form
# from fastapi.responses import HTMLResponse
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# from app.database import get_db
# from app.signup.models import User
# from app.utils.email_service import send_reset_email
# from passlib.context import CryptContext
# from pydantic import BaseModel
# import os

# router = APIRouter(tags=["Forgot Password"])

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")
# ALGORITHM = "HS256"


# # --------------------------------------------------------------------------
# # 1️⃣ Schema for forgot password request
# # --------------------------------------------------------------------------
# class ForgotPasswordRequest(BaseModel):
#     email: str


# # --------------------------------------------------------------------------
# # 2️⃣ API to send reset link via email
# # --------------------------------------------------------------------------
# @router.post("/forgot-password/request")
# async def request_password_reset(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == data.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="Email not found")

#     # create JWT token (valid for 30 minutes)
#     token_data = {"sub": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)}
#     token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

#     reset_link = f"http://127.0.0.1:6500/forgot-password/reset?token={token}"
#     send_reset_email(user.email, reset_link)
#     return {"message": "✅ Reset link sent successfully! Check your email."}


# # --------------------------------------------------------------------------
# # 3️⃣ Show reset password HTML form (GET)
# # --------------------------------------------------------------------------
# @router.get("/forgot-password/reset")
# async def show_reset_form(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#     except JWTError:
#         return HTMLResponse("<h3>❌ Invalid or expired link</h3>")

#     html_content = f"""
#     <html>
#         <head>
#             <title>Reset Password</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     background-color: #f4f4f4;
#                     padding: 40px;
#                     display: flex;
#                     justify-content: center;
#                 }}
#                 form {{
#                     background-color: white;
#                     padding: 30px;
#                     border-radius: 10px;
#                     box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#                     width: 320px;
#                 }}
#                 input {{
#                     width: 100%;
#                     padding: 8px;
#                     margin: 6px 0;
#                     border: 1px solid #ccc;
#                     border-radius: 5px;
#                 }}
#                 button {{
#                     background-color: #007bff;
#                     color: white;
#                     padding: 10px 20px;
#                     border: none;
#                     border-radius: 5px;
#                     cursor: pointer;
#                     width: 100%;
#                 }}
#                 button:hover {{
#                     background-color: #0056b3;
#                 }}
#             </style>
#         </head>
#         <body>
#             <form action="/forgot-password/reset" method="post">
#                 <h2>Reset Your Password</h2>
#                 <input type="hidden" name="token" value="{token}">
#                 <label>Email:</label><br>
#                 <input type="email" name="email" value="{email}" readonly><br><br>
#                 <label>New Password:</label><br>
#                 <input type="password" name="new_password" required><br><br>
#                 <label>Confirm Password:</label><br>
#                 <input type="password" name="confirm_password" required><br><br>
#                 <button type="submit">Reset Password</button>
#             </form>
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)


# # --------------------------------------------------------------------------
# # 4️⃣ Handle form submission and update password (POST)
# # --------------------------------------------------------------------------
# @router.post("/forgot-password/reset")
# async def reset_password(
#     token: str = Form(...),
#     email: str = Form(...),
#     new_password: str = Form(...),
#     confirm_password: str = Form(...),
#     db: Session = Depends(get_db),
# ):
#     if new_password != confirm_password:
#         return HTMLResponse("<h3>❌ Passwords do not match</h3>")

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email_from_token = payload.get("sub")
#         if email != email_from_token:
#             return HTMLResponse("<h3>❌ Email does not match token</h3>")
#     except JWTError:
#         return HTMLResponse("<h3>❌ Invalid or expired token</h3>")

#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         return HTMLResponse("<h3>❌ User not found</h3>")

#     # Update the user's password
#     user.password = pwd_context.hash(new_password)
#     db.commit()

#     return HTMLResponse("<h3>✅ Password reset successful! You can close this tab now.</h3>")


# from fastapi import APIRouter, Depends, HTTPException, Form
# from fastapi.responses import HTMLResponse
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# from app.database import get_db
# from app.signup.models import User
# from app.utils.email_service import send_reset_email
# from passlib.context import CryptContext
# from pydantic import BaseModel
# import os

# router = APIRouter(tags=["Forgot Password"])

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")
# ALGORITHM = "HS256"


# # --------------------------------------------------------------------------
# # 1️⃣ Schema for forgot password request
# # --------------------------------------------------------------------------
# class ForgotPasswordRequest(BaseModel):
#     email: str


# # --------------------------------------------------------------------------
# # 2️⃣ API to send reset link via email
# # --------------------------------------------------------------------------
# @router.post("/forgot-password/request")
# async def request_password_reset(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == data.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="Email not found")

#     token_data = {"sub": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)}
#     token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

#     reset_link = f"http://192.168.7.7:6500/forgot-password/reset?token={token}"
#     send_reset_email(user.email, reset_link)
#     return {"message": "✅ Reset link sent successfully! Check your email."}


# # --------------------------------------------------------------------------
# # 3️⃣ Show reset password HTML form (GET)
# # --------------------------------------------------------------------------
# @router.get("/forgot-password/reset")
# async def show_reset_form(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#     except JWTError:
#         return HTMLResponse("<h3>❌ Invalid or expired link</h3>")

#     html_content = f"""
#     <html>
#         <head>
#             <title>Reset Password</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     background-color: #f4f4f4;
#                     padding: 40px;
#                     display: flex;
#                     justify-content: center;
#                 }}
#                 form {{
#                     background-color: white;
#                     padding: 30px;
#                     border-radius: 10px;
#                     box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#                     width: 320px;
#                 }}
#                 input {{
#                     width: 100%;
#                     padding: 8px;
#                     margin: 6px 0;
#                     border: 1px solid #ccc;
#                     border-radius: 5px;
#                 }}
#                 button {{
#                     background-color: #007bff;
#                     color: white;
#                     padding: 10px 20px;
#                     border: none;
#                     border-radius: 5px;
#                     cursor: pointer;
#                     width: 100%;
#                 }}
#                 button:hover {{
#                     background-color: #0056b3;
#                 }}
#             </style>
#         </head>
#         <body>
#             <form action="/forgot-password/reset" method="post">
#                 <h2>Reset Your Password</h2>
#                 <input type="hidden" name="token" value="{token}">
#                 <label>Email:</label><br>
#                 <input type="email" name="email" value="{email}" readonly><br><br>
#                 <label>New Password:</label><br>
#                 <input type="password" name="new_password" required><br><br>
#                 <label>Confirm Password:</label><br>
#                 <input type="password" name="confirm_password" required><br><br>
#                 <button type="submit">Reset Password</button>
#             </form>
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)


# # --------------------------------------------------------------------------
# # 4️⃣ Handle form submission and update password (POST)
# # --------------------------------------------------------------------------
# @router.post("/forgot-password/reset")
# async def reset_password(
#     token: str = Form(...),
#     email: str = Form(...),
#     new_password: str = Form(...),
#     confirm_password: str = Form(...),
#     db: Session = Depends(get_db),
# ):
#     if new_password != confirm_password:
#         return HTMLResponse("<h3>❌ Passwords do not match</h3>")

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email_from_token = payload.get("sub")
#         if email != email_from_token:
#             return HTMLResponse("<h3>❌ Email does not match token</h3>")
#     except JWTError:
#         return HTMLResponse("<h3>❌ Invalid or expired token</h3>")

#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         return HTMLResponse("<h3>❌ User not found</h3>")

#     # ✅ FIXED — Correct field name for updating password
#     user.hashed_password = pwd_context.hash(new_password)
#     db.commit()

#     return HTMLResponse("<h3>✅ Password reset successful! You can now login with your new password.</h3>")

# from fastapi import APIRouter, Depends, HTTPException, Form
# from fastapi.responses import HTMLResponse
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# from app.database import get_db
# from app.signup.models import User
# from app.utils.email_service import send_reset_email
# from passlib.context import CryptContext
# from pydantic import BaseModel
# import os

# router = APIRouter(tags=["Forgot Password"])

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")
# ALGORITHM = "HS256"


# # --------------------------------------------------------------------------
# # 1️⃣ Schema for forgot password request
# # --------------------------------------------------------------------------
# class ForgotPasswordRequest(BaseModel):
#     email: str


# # --------------------------------------------------------------------------
# # 2️⃣ API to send reset link via email
# # --------------------------------------------------------------------------
# @router.post("/forgot-password/request")
# async def request_password_reset(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == data.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="Email not found")

#     token_data = {"sub": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)}
#     token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

#     # 💡 Use your LAN IP so other devices can open it
#     reset_link = f"http://192.168.7.7:6500/forgot-password/reset?token={token}"
#     send_reset_email(user.email, reset_link)

#     return {"message": "✅ Reset link sent successfully! Check your email."}


# # --------------------------------------------------------------------------
# # 3️⃣ Show reset password HTML form (GET)
# # --------------------------------------------------------------------------
# @router.get("/forgot-password/reset")
# async def show_reset_form(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#     except JWTError:
#         return HTMLResponse("<h3>❌ Invalid or expired link</h3>")

#     # 🌟 Beautiful modern UI
#     html_content = f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8" />
#         <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#         <title>Reset Password</title>
#         <style>
#             body {{
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                 background: linear-gradient(135deg, #74ABE2, #5563DE);
#                 height: 100vh;
#                 margin: 0;
#                 display: flex;
#                 align-items: center;
#                 justify-content: center;
#             }}
#             .container {{
#                 background: white;
#                 border-radius: 15px;
#                 box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
#                 width: 400px;
#                 padding: 40px 35px;
#                 text-align: center;
#                 animation: fadeIn 0.5s ease-in;
#             }}
#             @keyframes fadeIn {{
#                 from {{ opacity: 0; transform: translateY(-20px); }}
#                 to {{ opacity: 1; transform: translateY(0); }}
#             }}
#             h2 {{
#                 color: #333;
#                 margin-bottom: 20px;
#             }}
#             label {{
#                 display: block;
#                 text-align: left;
#                 margin-bottom: 8px;
#                 font-weight: 500;
#                 color: #444;
#             }}
#             input {{
#                 width: 100%;
#                 padding: 10px;
#                 margin-bottom: 15px;
#                 border: 1px solid #ccc;
#                 border-radius: 6px;
#                 font-size: 14px;
#                 transition: border-color 0.2s;
#             }}
#             input:focus {{
#                 border-color: #5563DE;
#                 outline: none;
#             }}
#             button {{
#                 background-color: #5563DE;
#                 color: white;
#                 border: none;
#                 padding: 12px 0;
#                 border-radius: 6px;
#                 width: 100%;
#                 font-size: 16px;
#                 font-weight: 600;
#                 cursor: pointer;
#                 transition: background-color 0.3s;
#             }}
#             button:hover {{
#                 background-color: #3e4ec4;
#             }}
#             .footer {{
#                 margin-top: 15px;
#                 font-size: 13px;
#                 color: #666;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h2>🔒 Reset Your Password</h2>
#             <form action="/forgot-password/reset" method="post">
#                 <input type="hidden" name="token" value="{token}">
#                 <label>Email</label>
#                 <input type="email" name="email" value="{email}" readonly>
#                 <label>New Password</label>
#                 <input type="password" name="new_password" placeholder="Enter new password" required>
#                 <label>Confirm Password</label>
#                 <input type="password" name="confirm_password" placeholder="Confirm password" required>
#                 <button type="submit">Reset Password</button>
#             </form>
#             <div class="footer">Your password will be securely updated 🔐</div>
#         </div>
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)


# # --------------------------------------------------------------------------
# # 4️⃣ Handle form submission and update password (POST)
# # --------------------------------------------------------------------------
# @router.post("/forgot-password/reset")
# async def reset_password(
#     token: str = Form(...),
#     email: str = Form(...),
#     new_password: str = Form(...),
#     confirm_password: str = Form(...),
#     db: Session = Depends(get_db),
# ):
#     if new_password != confirm_password:
#         return HTMLResponse("<h3>❌ Passwords do not match</h3>")

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email_from_token = payload.get("sub")
#         if email != email_from_token:
#             return HTMLResponse("<h3>❌ Email does not match token</h3>")
#     except JWTError:
#         return HTMLResponse("<h3>❌ Invalid or expired token</h3>")

#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         return HTMLResponse("<h3>❌ User not found</h3>")

#     # ✅ Correct field name for password hashing
#     user.hashed_password = pwd_context.hash(new_password)
#     db.commit()

#     return HTMLResponse(
#         "<h2 style='font-family:Segoe UI;text-align:center;margin-top:40px;color:green;'>✅ Password reset successful!<br>You can now log in with your new password.</h2>"
#     )


from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.database import get_db
from app.signup.models import User
from app.utils.email_service import send_reset_email
from passlib.context import CryptContext
from pydantic import BaseModel
import os

router = APIRouter(tags=["Forgot Password"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")
ALGORITHM = "HS256"


# --------------------------------------------------------------------------
# 1️⃣ Schema for forgot password request
# --------------------------------------------------------------------------
class ForgotPasswordRequest(BaseModel):
    email: str


# --------------------------------------------------------------------------
# 2️⃣ API to send reset link via email
# --------------------------------------------------------------------------
@router.post("/forgot-password/request")
async def request_password_reset(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    token_data = {"sub": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    reset_link = f"http://192.168.7.7:6500/forgot-password/reset?token={token}"
    send_reset_email(user.email, reset_link)

    return {"message": "✅ Reset link sent successfully! Check your email."}


# --------------------------------------------------------------------------
# 3️⃣ Show reset password HTML form (GET)
# --------------------------------------------------------------------------
@router.get("/forgot-password/reset")
async def show_reset_form(token: str, message: str = "", color: str = "black"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        return HTMLResponse("<h3>❌ Invalid or expired link</h3>")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Reset Password</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #74ABE2, #5563DE);
                height: 100vh;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .container {{
                background: white;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                width: 400px;
                padding: 40px 35px;
                text-align: center;
                animation: fadeIn 0.5s ease-in;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(-20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            h2 {{ color: #333; margin-bottom: 20px; }}
            label {{ display: block; text-align: left; margin-bottom: 8px; font-weight: 500; color: #444; }}
            input {{
                width: 100%; padding: 10px; margin-bottom: 15px;
                border: 1px solid #ccc; border-radius: 6px;
                font-size: 14px; transition: border-color 0.2s;
            }}
            input:focus {{ border-color: #5563DE; outline: none; }}
            button {{
                background-color: #5563DE; color: white;
                border: none; padding: 12px 0;
                border-radius: 6px; width: 100%;
                font-size: 16px; font-weight: 600;
                cursor: pointer; transition: background-color 0.3s;
            }}
            button:hover {{ background-color: #3e4ec4; }}
            .footer {{ margin-top: 15px; font-size: 13px; color: #666; }}
            .message {{ color: {color}; font-weight: 600; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔒 Reset Your Password</h2>
            <form action="/forgot-password/reset" method="post">
                <div class="message">{message}</div>
                <input type="hidden" name="token" value="{token}">
                <label>Email</label>
                <input type="email" name="email" value="{email}" readonly>
                <label>New Password</label>
                <input type="password" name="new_password" placeholder="Enter new password" required>
                <label>Confirm Password</label>
                <input type="password" name="confirm_password" placeholder="Confirm password" required>
                <button type="submit">Reset Password</button>
            </form>
            <div class="footer">Your password will be securely updated 🔐</div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# --------------------------------------------------------------------------
# 4️⃣ Handle form submission and update password (POST)
# --------------------------------------------------------------------------
@router.post("/forgot-password/reset")
async def reset_password(
    request: Request,
    token: str = Form(...),
    email: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    message = ""
    color = "red"

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_from_token = payload.get("sub")
        if email != email_from_token:
            message = "❌ Email does not match token"
            raise Exception()
    except JWTError:
        message = "❌ Invalid or expired token"
        raise Exception()

    if new_password != confirm_password:
        message = "❌ Passwords do not match"
        return await show_reset_form(token, message, "red")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        message = "❌ User not found"
        return await show_reset_form(token, message, "red")

    user.hashed_password = pwd_context.hash(new_password)
    db.commit()

    message = "✅ Password reset successful! You can now log in."
    return await show_reset_form(token, message, "green")
