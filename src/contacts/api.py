from datetime import datetime
from typing import List, Optional
from uuid import UUID

from django.http import Http404
from ninja import NinjaAPI, Schema, Field
from ninja.pagination import paginate

from contacts.models import Contact

api = NinjaAPI(title="Contacts API", urls_namespace='api')


class ContactIn(Schema):
    name: str
    email: str = Field(
        ...,
        pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        description="Валидный email адрес"
    )
    phone: Optional[str] = None


class ContactOut(Schema):
    id: UUID
    name: str
    email: str
    phone: Optional[str] = None
    date_created: datetime


@api.post("/", response={201: ContactOut})
def create_contact(request, payload: ContactIn):
    contact = Contact.objects.create(
        name=payload.name,
        email=payload.email,
        phone=payload.phone
    )
    return 201, contact


@api.get("/", response=List[ContactOut])
@paginate
def list_contacts(request, email: Optional[str] = None):
    queryset = Contact.objects.all()
    if email:
        queryset = queryset.filter(email__icontains=email)
    return queryset


@api.get("/{contact_id}", response=ContactOut)
def get_contact(request, contact_id: UUID):
    try:
        contact = Contact.objects.get(id=contact_id)
        return contact
    except Contact.DoesNotExist:
        raise Http404(f"Contact with id {contact_id} does not exist")


@api.put("/{contact_id}", response=ContactOut)
def update_contact(request, contact_id: UUID, payload: ContactIn):
    try:
        contact = Contact.objects.get(id=contact_id)
        contact.name = payload.name
        contact.email = payload.email
        contact.phone = payload.phone
        contact.save()
        return contact
    except Contact.DoesNotExist:
        raise Http404(f"Contact with id {contact_id} does not exist")


@api.delete("/{contact_id}", response={204: None})
def delete_contact(request, contact_id: UUID):
    try:
        contact = Contact.objects.get(id=contact_id)
        contact.delete()
        return 204, None
    except Contact.DoesNotExist:
        raise Http404(f"Contact with id {contact_id} does not exist")
