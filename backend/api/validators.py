from marshmallow import Schema, ValidationError, post_load
from marshmallow.fields import Email, Integer

class UserValidator(Schema):
    email = Email()
    phoneNumber = Integer()

    @post_load
    def validates_input_data(self, input_data, *args, **kwargs):
        phone = input_data.get('phoneNumber')
        email = input_data.get('email')
        if (not phone) and (not email):
            raise ValidationError("PhoneNumber or Email is required.")
        
        return input_data