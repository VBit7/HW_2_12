import sqlalchemy.orm as orm
import sqlalchemy as sqa

from datetime import date


class Base(orm.DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    first_name: orm.Mapped[str] = orm.mapped_column(sqa.String(50), index=True)
    last_name: orm.Mapped[str] = orm.mapped_column(sqa.String(50), index=True)
    email: orm.Mapped[str] = orm.mapped_column(sqa.String(50), index=True)
    phone_number: orm.Mapped[str] = orm.mapped_column(sqa.String(50))
    date_of_birth: orm.Mapped[date] = orm.mapped_column(sqa.Date)
    additional_data: orm.Mapped[str] = orm.mapped_column(sqa.String(250))
