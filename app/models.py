import datetime
import decimal
import uuid
from typing import Any, List, Optional

from sqlalchemy import CheckConstraint, Date, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, \
    Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    Абстрактный класс модели
    """

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class Professors(Base):
    __tablename__ = 'professors'
    __table_args__ = (
        CheckConstraint("degree::text ~* '^[кКдД].+[а-яА-Я].+[н].+$'::text", name='professors_degree_check'),
        PrimaryKeyConstraint('professor_id', name='professors_pkey')
    )

    professor_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_name: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[str] = mapped_column(String(30))
    current_position: Mapped[str] = mapped_column(String(40))
    experience: Mapped[int] = mapped_column(Integer)
    patronymic: Mapped[Optional[str]] = mapped_column(String(30))
    degree: Mapped[Optional[str]] = mapped_column(String(15))
    academic_title: Mapped[Optional[str]] = mapped_column(String(40))
    salary: Mapped[Optional[Any]] = mapped_column(MONEY)

    employments: Mapped[List['Employments']] = relationship('Employments', back_populates='professor')
    fields: Mapped[List['Fields']] = relationship('Fields', back_populates='professor')


class StructuralUnits(Base):
    __tablename__ = 'structural_units'
    __table_args__ = (
        CheckConstraint("phone_number::text ~* '^[0-9]{2}-[0-9]{2}$'::text",
                        name='structural_units_phone_number_check'),
        PrimaryKeyConstraint('structural_unit_id', name='structural_units_pkey')
    )

    structural_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_title: Mapped[str] = mapped_column(Text)
    head_of_the_unit: Mapped[str] = mapped_column(String(40))
    abbreviated_title: Mapped[Optional[str]] = mapped_column(String(20))
    phone_number: Mapped[Optional[str]] = mapped_column(String(5))

    employments: Mapped[List['Employments']] = relationship('Employments', back_populates='structural_unit')
    fields: Mapped[List['Fields']] = relationship('Fields', back_populates='structural_unit')
    students_groups: Mapped[List['StudentsGroups']] = relationship('StudentsGroups', back_populates='structural_unit')


class Employments(Base):
    __tablename__ = 'employments'
    __table_args__ = (
        ForeignKeyConstraint(['professor_id'], ['professors.professor_id'], ondelete='CASCADE',
                             name='employments_professor_id_fkey'),
        ForeignKeyConstraint(['structural_unit_id'], ['structural_units.structural_unit_id'], ondelete='CASCADE',
                             name='employments_structural_unit_id_fkey'),
        PrimaryKeyConstraint('structural_unit_id', 'professor_id', name='employments_pkey')
    )

    structural_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    professor_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contract_number: Mapped[int] = mapped_column(Integer)
    wage_rate: Mapped[decimal.Decimal] = mapped_column(Numeric(3, 2))

    professor: Mapped['Professors'] = relationship('Professors', back_populates='employments')
    structural_unit: Mapped['StructuralUnits'] = relationship('StructuralUnits', back_populates='employments')


class Fields(Base):
    __tablename__ = 'fields'
    __table_args__ = (
        ForeignKeyConstraint(['professor_id'], ['professors.professor_id'], ondelete='CASCADE',
                             name='fields_professor_id_fkey'),
        ForeignKeyConstraint(['structural_unit_id'], ['structural_units.structural_unit_id'], ondelete='CASCADE',
                             name='fields_structural_unit_id_fkey'),
        PrimaryKeyConstraint('field_id', name='fields_pkey')
    )

    field_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    field_name: Mapped[str] = mapped_column(String(100))
    structural_unit_id: Mapped[int] = mapped_column(Integer)
    professor_id: Mapped[int] = mapped_column(Integer)
    zet: Mapped[int] = mapped_column(Integer)
    semester: Mapped[int] = mapped_column(Integer)

    professor: Mapped['Professors'] = relationship('Professors', back_populates='fields')
    structural_unit: Mapped['StructuralUnits'] = relationship('StructuralUnits', back_populates='fields')
    field_comprehensions: Mapped[List['FieldComprehensions']] = relationship('FieldComprehensions',
                                                                             back_populates='fields')


class StudentsGroups(Base):
    __tablename__ = 'students_groups'
    __table_args__ = (
        CheckConstraint("enrolment_status::text = ANY ('{Очная,Заочная,Очно-заочная}'::character varying[]::text[])",
                        name='students_groups_enrolment_status_check'),
        CheckConstraint("students_group_number::text ~* '^[А-Яа-я]+-[МВ0-9]+$'::text",
                        name='students_groups_students_group_number_check'),
        ForeignKeyConstraint(['structural_unit_id'], ['structural_units.structural_unit_id'], ondelete='CASCADE',
                             name='students_groups_structural_unit_id_fkey'),
        PrimaryKeyConstraint('students_group_number', name='students_groups_pkey')
    )

    students_group_number: Mapped[str] = mapped_column(String(7), primary_key=True)
    enrolment_status: Mapped[str] = mapped_column(String(12))
    structural_unit_id: Mapped[int] = mapped_column(Integer)

    structural_unit: Mapped['StructuralUnits'] = relationship('StructuralUnits', back_populates='students_groups')
    students: Mapped[List['Students']] = relationship('Students', back_populates='students_groups')


class Students(Base):
    __tablename__ = 'students'
    __table_args__ = (
        CheckConstraint("email::text ~* '^[A-Za-z0-9._+%%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'::text", name='email_cheak'),
        ForeignKeyConstraint(['students_group_number'], ['students_groups.students_group_number'], ondelete='CASCADE',
                             name='students_group_key'),
        PrimaryKeyConstraint('student_id', name='students_pkey'),
        UniqueConstraint('email', name='students_email_key')
    )

    student_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_name: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[str] = mapped_column(String(30))
    students_group_number: Mapped[str] = mapped_column(String(7))
    birthday: Mapped[datetime.date] = mapped_column(Date)
    patronymic: Mapped[Optional[str]] = mapped_column(String(30))
    email: Mapped[Optional[str]] = mapped_column(String(30))

    students_groups: Mapped['StudentsGroups'] = relationship('StudentsGroups', back_populates='students')
    field_comprehensions: Mapped[List['FieldComprehensions']] = relationship('FieldComprehensions',
                                                                             back_populates='student')


class FieldComprehensions(Base):
    __tablename__ = 'field_comprehensions'
    __table_args__ = (
        CheckConstraint('mark >= 2 AND mark <= 5', name='field_comprehensions_mark_check'),
        ForeignKeyConstraint(['field'], ['fields.field_id'], ondelete='CASCADE',
                             name='field_comprehensions_field_fkey'),
        ForeignKeyConstraint(['student_id'], ['students.student_id'], ondelete='CASCADE',
                             name='field_comprehensions_student_id_fkey'),
        PrimaryKeyConstraint('student_id', 'field', name='field_comprehensions_pkey')
    )

    student_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    mark: Mapped[Optional[int]] = mapped_column(Integer)

    fields: Mapped['Fields'] = relationship('Fields', back_populates='field_comprehensions')
    student: Mapped['Students'] = relationship('Students', back_populates='field_comprehensions')


class StudentIds(Students):
    __tablename__ = 'student_ids'
    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['students.student_id'], ondelete='CASCADE',
                             name='student_ids_student_id_fkey'),
        PrimaryKeyConstraint('student_id', name='student_ids_pkey')
    )

    student_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    issue_date: Mapped[datetime.date] = mapped_column(Date, server_default=text('CURRENT_DATE'))
    expiration_date: Mapped[datetime.date] = mapped_column(Date,
                                                           server_default=text("(CURRENT_DATE + '4 years'::interval)"))
