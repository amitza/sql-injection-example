from dataclasses import dataclass
from flask_login import UserMixin


@dataclass
class User(UserMixin):
    name: str
    id: str
    password: str
    email: str
    balance: int
    contactno: int
