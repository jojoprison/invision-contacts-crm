from ninja import NinjaAPI, Schema, Path, Query
from ninja.pagination import paginate
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from contacts.models import Contact

api = NinjaAPI(title="Contacts API")


class ContactIn(Schema):
    name: str
    email: str
    phone: Optional[str] = None


class ContactOut(Schema):
    id: UUID
    name: str
    email: str
    phone: Optional[str] = None
    date_created: datetime


@api.post("/contacts", response={201: ContactOut})
def create_contact(request, payload: ContactIn):
    contact = Contact.objects.create(
        name=payload.name,
        email=payload.email,
        phone=payload.phone
    )
    return 201, contact


@api.get("/contacts", response=List[ContactOut])
@paginate
def list_contacts(request, email: Optional[str] = None):
    queryset = Contact.objects.all()
    if email:
        queryset = queryset.filter(email__icontains=email)
    return queryset


@api.get("/contacts/{contact_id}", response=ContactOut)
def get_contact(request, contact_id: UUID):
    contact = Contact.objects.get(id=contact_id)
    return contact


@api.put("/contacts/{contact_id}", response=ContactOut)
def update_contact(request, contact_id: UUID, payload: ContactIn):
    contact = Contact.objects.get(id=contact_id)
    contact.name = payload.name
    contact.email = payload.email
    contact.phone = payload.phone
    contact.save()
    return contact


@api.delete("/contacts/{contact_id}", response={204: None})
def delete_contact(request, contact_id: UUID):
    contact = Contact.objects.get(id=contact_id)
    contact.delete()
    return 204, None
