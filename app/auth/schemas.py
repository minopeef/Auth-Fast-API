import re
from typing import Self
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator, computed_field
from app.auth.utils import get_password_hash

class EmailModel(BaseModel):
    email: EmailStr = Field(description="Email address")
    model_config = ConfigDict(from_attributes=True)

class UserBase(EmailModel):
    phone_number: str = Field(description="Phone number in international format starting with '+'")
    first_name: str = Field(min_length=3, max_length=50, description="First name, 3 to 50 characters")
    last_name: str = Field(min_length=3, max_length=50, description="Last name, 3 to 50 characters")

    @field_validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Phone number must start with "+" and contain 5 to 15 digits')
        return value

class SUserRegister(UserBase):
    password: str = Field(min_length=5, max_length=50, description="Password, 5 to 50 characters")
    confirm_password: str = Field(min_length=5, max_length=50, description="Confirm password")

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        self.password = get_password_hash(self.password)  # Hash password before saving to database
        return self

class SUserAddDB(UserBase):
    password: str = Field(min_length=5, description="Password in HASH string format")

class SUserAuth(EmailModel):
    password: str = Field(min_length=5, max_length=50, description="Password, 5 to 50 characters")

class RoleModel(BaseModel):
    id: int = Field(description="Role identifier")
    name: str = Field(description="Role name")
    model_config = ConfigDict(from_attributes=True)

class SUserInfo(UserBase):
    id: int = Field(description="User identifier")
    role: RoleModel = Field(exclude=True)

    @computed_field
    def role_name(self) -> str:
        return self.role.name

    @computed_field
    def role_id(self) -> int:
        return self.role.id
