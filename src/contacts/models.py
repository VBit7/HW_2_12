import enum
import sqlalchemy.orm as orm
import sqlalchemy as sqa

from datetime import date


class Base(orm.DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(sqa.String(50), index=True)
    email: orm.Mapped[str] = orm.mapped_column(sqa.String(250), unique=True, nullable=False)
    password: orm.Mapped[str] = orm.mapped_column(sqa.String(250), nullable=False)
    avatar: orm.Mapped[str] = orm.mapped_column(sqa.String(250), nullable=True)
    refresh_token: orm.Mapped[str] = orm.mapped_column(sqa.String(250), nullable=True)
    created_at: orm.Mapped[date] = orm.mapped_column('created_at', sqa.DateTime, default=sqa.func.now())
    updated_at: orm.Mapped[date] = orm.mapped_column('updated_at', sqa.DateTime, default=sqa.func.now(),
                                                     onupdate=sqa.func.now())


class Contact(Base):
    __tablename__ = 'contacts'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    first_name: orm.Mapped[str] = orm.mapped_column(sqa.String(50), index=True)
    last_name: orm.Mapped[str] = orm.mapped_column(sqa.String(50), index=True)
    email: orm.Mapped[str] = orm.mapped_column(sqa.String(50), index=True)
    phone_number: orm.Mapped[str] = orm.mapped_column(sqa.String(50))
    date_of_birth: orm.Mapped[date] = orm.mapped_column(sqa.Date)
    additional_data: orm.Mapped[str] = orm.mapped_column(sqa.String(250))
    created_at: orm.Mapped[date] = orm.mapped_column("created_at", sqa.DateTime, default=sqa.func.now(), nullable=True)
    updated_at: orm.Mapped[date] = orm.mapped_column("updated_at", sqa.DateTime, default=sqa.func.now(),
                                                     onupdate=sqa.func.now(), nullable=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sqa.Integer, sqa.ForeignKey("users.id"), nullable=True)
    user: orm.Mapped["User"] = orm.relationship("User", backref="contacts", lazy="joined")
