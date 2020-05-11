"""Schema for the BOE database"""

from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BoeDiarySection(Base):
    __tablename__ = 'boe_diary_section'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class BoeDiaryEntryReference(Base):
    __tablename__ = 'boe_diary_entry_reference'

    source_id = Column(String, ForeignKey('boe_diary_entry.id'))
    referenced_id = Column(String, ForeignKey('boe_diary_entry.id'))
    reference_type = Column(String)
    reference_type_code = Column(String)
    text = Column(String)

    entry = relationship(BoeDiaryEntry, back_populates='references')


class BoeDiaryEntryLabel(Base):
    __tablename__ = 'boe_diary_entry_label'

    name = Column(String, nullable=False)
    entry_id = Column(String, ForeignKey('boe_diary_entry.id'))


class BoeDiaryEntry(Base):
    __tablename__ = 'boe_diary_entry'

    id = Column(String, primary_key=True)
    date = Column(Date)
    fetch_date = Column(Date)
    title = Column(String)
    section = Column(String, ForeignKey('boe_diary_section.id'))
    department = Column(String)
    epigraph = Column(String)
    pdf_url = Column(String)
    xml_url = Column(String)
    htm_url = Column(String)
    has_economic_impact = Column(String)


class BoeSubscription(Base):
    __tablename__ = 'boe_subscription'

    subscription_hash = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    search_string = Column(String, nullable=False)
    search_type = Column(String, nullable=False)
