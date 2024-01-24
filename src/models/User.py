from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_name: str
    user_email: str
    user_password: str
    user_id: Optional[str] = None

    # @property
    # def set_user_id(self, value: str):
    #     self.user_id = value
    
    @property
    def user_id(self):
        return self.user_id
    
    @property
    def user_email(self):
        return self.user_email
    
    @property
    def user_password(self):
        return self.user_password
    