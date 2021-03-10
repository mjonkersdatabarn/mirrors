# coding=utf-8

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Table,
    ForeignKey,
    Boolean,
    Time, Enum,
)
from sqlalchemy.ext.declarative import declarative_base
from typing import (
    Dict,
    AnyStr,
    Union,
    List,
)

from sqlalchemy.orm import relationship

Base = declarative_base()
url_types = (
    'ftp',
    'https',
    'http',
    'rsync',
)


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, nullable=False, primary_key=True)
    url = Column(String, nullable=False)
    type = Column(Enum(*url_types, name='type'), nullable=False)

    def to_dict(self) -> Dict[AnyStr, AnyStr]:
        return {
            'url': self.url,
            'type': self.type,
        }


mirrors_urls = Table(
    'mirrors_urls',
    Base.metadata,
    Column(
        'mirror_id', Integer, ForeignKey(
            'mirrors.id',
            ondelete='CASCADE',
        ),
    ),
    Column(
        'url_id', Integer, ForeignKey(
            'urls.id',
            ondelete='CASCADE',
        )
    ),
)


class Mirror(Base):
    __tablename__ = 'mirrors'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    continent = Column(String, nullable=False)
    country = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_expired = Column(Boolean, nullable=False, default=False)
    update_frequency = Column(Time, nullable=False)
    sponsor_name = Column(String, nullable=False)
    sponsor_url = Column(String, nullable=False)
    email = Column(String, nullable=False)
    urls = relationship(
        'Url',
        secondary=mirrors_urls,
        passive_deletes=True,
    )

    def to_dict(self) -> Dict[AnyStr, Union[AnyStr, float, Dict, List]]:
        return {
            'name': self.name,
            'continent': self.continent,
            'country': self.country,
            'ip': self.ip,
            'location': {
                'lat': self.latitude,
                'lon': self.longitude,
            },
            'is_expired': self.is_expired,
            'update_frequency': self.update_frequency.strftime('%H'),
            'sponsor_name': self.sponsor_name,
            'sponsor_url': self.sponsor_url,
            'email': self.email,
            'urls': [url.to_dict() for url in self.urls],
        }