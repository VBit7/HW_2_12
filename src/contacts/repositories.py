from datetime import date, timedelta

from sqlalchemy import select, or_, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from contacts.models import Contact, User  # noqa
from contacts.schemas import ContactSchema  # noqa


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.date_of_birth = body.date_of_birth
        contact.additional_data = body.additional_data
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(query: str, db: AsyncSession, user: User):
    stmt = (
        select(Contact)
        .filter(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%"),
            )
        )
        .filter_by(user=user)
    )
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def congratulate(db: AsyncSession, user: User):
    current_date = date.today()
    end_date = current_date + timedelta(days=7)

    stmt = (
        select(Contact)
        .where(
            or_(
                and_(
                    extract('month', Contact.date_of_birth) == current_date.month,
                    extract('day', Contact.date_of_birth) >= current_date.day,
                    extract('day', Contact.date_of_birth) <= end_date.day,
                ),
                and_(
                    extract('month', Contact.date_of_birth) == end_date.month,
                    extract('day', Contact.date_of_birth) <= end_date.day,
                ),
                and_(
                    extract('month', Contact.date_of_birth) == current_date.month,
                    extract('day', Contact.date_of_birth) == current_date.day,
                ),
            )
        )
        .filter_by(user=user)
        .order_by(extract('day', Contact.date_of_birth))
    )

    contacts = await db.execute(stmt)
    return contacts.scalars().all()
