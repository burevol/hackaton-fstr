from typing import Optional, List

from pydantic import BaseModel, EmailStr


class Error(BaseModel):
    status: str
    message: str


class Status(BaseModel):
    status: str


class SubmitDataResponse(BaseModel):
    status: str
    message: str
    id: str


class Coord(BaseModel):
    latitude: str
    longitude: str
    height: str


class Level(BaseModel):
    winter: str
    summer: str
    autumn: str
    spring: str


class Image(BaseModel):
    url: str
    title: str


class User(BaseModel):
    id: str
    email: EmailStr
    phone: Optional[str]
    fam: Optional[str]
    name: Optional[str]
    otc: Optional[str]


class Item(BaseModel):
    beautyTitle: str
    title: str
    other_titles: str
    connect: str
    add_time: Optional[str]
    coords: Coord
    type: str
    level: Level
    user: User
    images: List[Image]
