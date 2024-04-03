import fastapi
import database  # noqa

from sqlalchemy.ext.asyncio import AsyncSession

import contacts.models as models  # noqa
import contacts.schemas as schemas  # noqa
import contacts.repositories as repo  # noqa
from auth.services import auth_service   # noqa

from contacts.schemas import ContactSchema, ContactResponse  # noqa


router = fastapi.APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[schemas.ContactResponse])
async def get_contacts(
        limit: int = fastapi.Query(10, ge=10, le=500),
        offset: int = fastapi.Query(0, ge=0),
        db: AsyncSession = fastapi.Depends(database.get_db),
        user: models.User = fastapi.Depends(auth_service.get_current_user),
):
    contacts = await repo.get_contacts(limit, offset, db, user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
        contact_id: int = fastapi.Path(ge=1),
        db: AsyncSession = fastapi.Depends(database.get_db),
        user: models.User = fastapi.Depends(auth_service.get_current_user),
):
    contact = await repo.get_contact(contact_id, db, user)
    if contact is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponse, status_code=fastapi.status.HTTP_201_CREATED)
async def create_contact(
        body: ContactSchema,
        db: AsyncSession = fastapi.Depends(database.get_db),
        user: models.User = fastapi.Depends(auth_service.get_current_user),
):
    contact = await repo.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}")
async def update_contact(
        body: ContactSchema,
        contact_id: int = fastapi.Path(ge=1),
        db: AsyncSession = fastapi.Depends(database.get_db),
        user: models.User = fastapi.Depends(auth_service.get_current_user),
):
    contact = await repo.update_contact(contact_id, body, db, user)
    if contact is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def delete_contact(
        contact_id: int = fastapi.Path(ge=1),
        db: AsyncSession = fastapi.Depends(database.get_db),
        user: models.User = fastapi.Depends(auth_service.get_current_user),
):
    contact = await repo.delete_contact(contact_id, db, user)
    return contact


@router.get("/search/{query}", response_model=list[ContactResponse])
async def search_contacts(
        query: str,
        db: AsyncSession = fastapi.Depends(database.get_db),
        user: models.User = fastapi.Depends(auth_service.get_current_user),
):
    contacts = await repo.search_contacts(query, db, user)
    if contacts is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contacts


@router.get("/upcoming_birthdays/", response_model=list[ContactResponse])
async def upcoming_birthdays(
        db: AsyncSession = fastapi.Depends(database.get_db),
        user: models.User = fastapi.Depends(auth_service.get_current_user),
):
    contacts = await repo.congratulate(db, user)
    if contacts is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contacts


@router.get("/err")
async def test_err_route():
    raise fastapi.HTTPException(503, "Test error")
