# # app/contact/crud.py
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from . import models, schemas

# # CONTACT CRUD (no user_id)
# def create_contact(db: Session, contact_in: schemas.ContactCreate,
#                    image_path: Optional[str] = None,
#                    center_photos: Optional[List[str]] = None,
#                    logo_path: Optional[str] = None,
#                    other_activities_path: Optional[str] = None) -> models.Contact:
#     contact = models.Contact(
#         **contact_in.dict(),
#         image_path=image_path,
#         center_photos=center_photos,
#         logo_path=logo_path,
#         other_activities_path=other_activities_path
#     )
#     db.add(contact)
#     db.commit()
#     db.refresh(contact)
#     return contact

# def get_contact_by_id(db: Session, contact_id: int) -> Optional[models.Contact]:
#     return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

# def list_contacts(db: Session) -> List[models.Contact]:
#     return db.query(models.Contact).all()


# # INAI CRUD (linked by user_id)
# def create_or_update_inai(db: Session, user_id: int, username: str, password_encrypted: str):
#     cred = db.query(models.InaiCredential).filter(models.InaiCredential.user_id == user_id).first()
#     if not cred:
#         cred = models.InaiCredential(user_id=user_id, username=username, password_encrypted=password_encrypted)
#         db.add(cred)
#     else:
#         cred.username = username
#         cred.password_encrypted = password_encrypted
#     db.commit()
#     db.refresh(cred)
#     return cred

# def get_inai_by_user(db: Session, user_id: int):
#     return db.query(models.InaiCredential).filter(models.InaiCredential.user_id == user_id).first()






# app/contact/crud.py
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

def create_contact(db: Session, contact_in: schemas.ContactCreate,
                   image_path: Optional[str] = None,
                   center_photos: Optional[str] = None,
                   logo_path: Optional[str] = None,
                   other_activities_path: Optional[str] = None,
                   inai_password_encrypted: Optional[str] = None) -> models.Contact:
    contact = models.Contact(
        first_name=contact_in.first_name,
        last_name=contact_in.last_name,
        address=contact_in.address,
        designation=contact_in.designation,
        phone_number=contact_in.phone_number,
        dob=contact_in.dob,
        image_path=image_path,
        center_photos=center_photos,
        logo_path=logo_path,
        other_activities_path=other_activities_path,
        inai_email=contact_in.inai_email,
        inai_password_encrypted=inai_password_encrypted
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def get_contact_by_id(db: Session, contact_id: int) -> Optional[models.Contact]:
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def list_contacts(db: Session) -> List[models.Contact]:
    return db.query(models.Contact).all()

def update_contact_inai(db: Session, contact: models.Contact, inai_email: Optional[str], inai_password_encrypted: Optional[str]):
    if inai_email is not None:
        contact.inai_email = inai_email
    if inai_password_encrypted is not None:
        contact.inai_password_encrypted = inai_password_encrypted
    db.commit()
    db.refresh(contact)
    return contact
