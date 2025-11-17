# # app/contact/routes.py
# import os
# from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime
# from typing import List, Optional
# from . import schemas, crud, utils
# from ..database import get_db

# router = APIRouter(tags=["Contact & INAI"])

# # NOTE: Do NOT read FERNET_KEY at module import time.
# # We'll fetch it when needed using utils.get_fernet_key() or utils.encrypt_password()/decrypt_password().

# # Create contact (multipart/form-data) — no user_id involved
# @router.post("/", response_model=schemas.ContactRead)
# async def create_contact(
#     first_name: str = Form(...),
#     last_name: Optional[str] = Form(None),
#     address: Optional[str] = Form(None),
#     designation: Optional[str] = Form(None),
#     phone_number: Optional[str] = Form(None),
#     dob: Optional[str] = Form(None),
#     email: Optional[str] = Form(None),

#     image: Optional[UploadFile] = File(None),
#     center_photos: Optional[List[UploadFile]] = File(None),
#     logo: Optional[UploadFile] = File(None),
#     other_activity: Optional[UploadFile] = File(None),

#     db: Session = Depends(get_db),
# ):
#     # save uploads
#     image_path = await utils.save_upload_file(image, f"contact_image_{image.filename}") if image else None
#     center_paths = await utils.save_multiple_files(center_photos) if center_photos else None
#     logo_path = await utils.save_upload_file(logo, f"contact_logo_{logo.filename}") if logo else None
#     other_activity_path = await utils.save_upload_file(other_activity, f"contact_other_{other_activity.filename}") if other_activity else None

#     # parse dob
#     dob_date = None
#     if dob:
#         try:
#             dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
#         except ValueError:
#             raise HTTPException(status_code=400, detail="dob must be YYYY-MM-DD")

#     contact_in = schemas.ContactCreate(
#         first_name=first_name,
#         last_name=last_name,
#         address=address,
#         designation=designation,
#         phone_number=phone_number,
#         dob=dob_date,
#         email=email
#     )

#     contact = crud.create_contact(
#         db,
#         contact_in,
#         image_path=image_path,
#         center_photos=center_paths,
#         logo_path=logo_path,
#         other_activities_path=other_activity_path
#     )
#     return contact

# # Get contact by contact id
# @router.get("/{contact_id}", response_model=schemas.ContactRead)
# def get_contact(contact_id: int, db: Session = Depends(get_db)):
#     contact = crud.get_contact_by_id(db, contact_id)
#     if not contact:
#         raise HTTPException(status_code=404, detail="Contact not found")
#     return contact

# # Optional: list all contacts
# @router.get("/", response_model=list[schemas.ContactRead])
# def list_all_contacts(db: Session = Depends(get_db)):
#     return crud.list_contacts(db)

# # INAI endpoints (use user_id)
# @router.post("/inai", response_model=schemas.InaiRead)
# def create_inai(inai: schemas.InaiCreate, db: Session = Depends(get_db)):
#     # Read key at runtime using utils helper (will raise if not set)
#     try:
#         encrypted = utils.encrypt_password(None, inai.password)  # pass None so utils uses env key
#     except Exception as e:
#         # Return a clear HTTP error so client sees useful message
#         raise HTTPException(status_code=500, detail=str(e))

#     cred = crud.create_or_update_inai(db, inai.user_id, inai.username, encrypted)
#     return schemas.InaiRead(user_id=cred.user_id, username=cred.username)

# @router.get("/inai/{user_id}", response_model=schemas.InaiRead)
# def get_inai(user_id: int, db: Session = Depends(get_db)):
#     cred = crud.get_inai_by_user(db, user_id)
#     if not cred:
#         raise HTTPException(status_code=404, detail="INAI credentials not found")
#     try:
#         password_plain = utils.decrypt_password(None, cred.password_encrypted)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return schemas.InaiRead(user_id=cred.user_id, username=cred.username, password=password_plain)





# app/contact/routes.py
import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from . import schemas, crud, utils
from ..database import get_db

router = APIRouter(tags=["Contact & INAI"])

@router.post("/", response_model=schemas.ContactRead)
async def create_contact(
    first_name: str = Form(...),
    last_name: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    designation: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    dob: Optional[str] = Form(None),

    inai_email: Optional[str] = Form(None),
    inai_password: Optional[str] = Form(None),

    image: Optional[UploadFile] = File(None),
    center_photos: Optional[List[UploadFile]] = File(None),
    logo: Optional[UploadFile] = File(None),
    other_activity: Optional[UploadFile] = File(None),

    db: Session = Depends(get_db),
):
    # save uploads
    image_path = await utils.save_upload_file(image, f"contact_image_{image.filename}") if image else None
    center_paths = await utils.save_multiple_files(center_photos) if center_photos else None
    logo_path = await utils.save_upload_file(logo, f"contact_logo_{logo.filename}") if logo else None
    other_activity_path = await utils.save_upload_file(other_activity, f"contact_other_{other_activity.filename}") if other_activity else None

    # parse dob
    dob_date = None
    if dob:
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="dob must be YYYY-MM-DD")

    # encrypt INAI password (if provided)
    encrypted_password = None
    if inai_password:
        try:
            encrypted_password = utils.encrypt_password(None, inai_password)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    contact_in = schemas.ContactCreate(
        first_name=first_name,
        last_name=last_name,
        address=address,
        designation=designation,
        phone_number=phone_number,
        dob=dob_date,
        inai_email=inai_email,
        inai_password=inai_password,
    )

    contact = crud.create_contact(
        db,
        contact_in,
        image_path=image_path,
        center_photos=center_paths,
        logo_path=logo_path,
        other_activities_path=other_activity_path,
        inai_password_encrypted=encrypted_password
    )
    return contact

@router.get("/", response_model=list[schemas.ContactRead])
def list_all_contacts(db: Session = Depends(get_db)):
    return crud.list_contacts(db)

@router.get("/{contact_id}", response_model=schemas.ContactRead)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.get("/{contact_id}/", response_model=schemas.InaiRead)
def get_contact_inai(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if not contact.inai_email or not contact.inai_password_encrypted:
        raise HTTPException(status_code=404, detail="INAI credentials not found for this contact")
    try:
        decrypted = utils.decrypt_password(None, contact.inai_password_encrypted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.InaiRead(inai_email=contact.inai_email, inai_password=decrypted)
