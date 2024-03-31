import fastapi
import database  # noqa

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

import contacts.models as models  # noqa
import contacts.schemas as schemas  # noqa
import contacts.repositories as repo  # noqa

from contacts.schemas import ContactSchema, ContactResponse  # noqa


router = fastapi.APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[schemas.ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(database.get_db)):
    contacts = await repo.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(database.get_db)):
    contact = await repo.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(database.get_db)):
    contact = await repo.create_contact(body, db)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1),
                         db: AsyncSession = Depends(database.get_db)):
    contact = await repo.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(database.get_db)):
    contact = await repo.delete_contact(contact_id, db)
    return contact


@router.get("/search/{query}", response_model=list[ContactResponse])
async def search_contacts(query: str, db: AsyncSession = Depends(database.get_db)):
    contacts = await repo.search_contacts(query, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contacts


@router.get("/upcoming_birthdays/", response_model=list[ContactResponse])
async def upcoming_birthdays(db: AsyncSession = Depends(database.get_db)):
    contacts = await repo.congratulate(db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contacts


@router.get("/err")
async def test_err_route():
    raise fastapi.HTTPException(503, "Test error")
