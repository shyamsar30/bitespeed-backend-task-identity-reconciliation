from marshmallow import Schema, ValidationError, post_load
from marshmallow.fields import Email, String

class UserValidator(Schema):
    email = Email(allow_none=True)
    phoneNumber = String(allow_none=True)

    @post_load
    def validates_input_data(self, input_data, *args, **kwargs):
        phone = input_data.get('phoneNumber')
        email = input_data.get('email')
        if (not phone) and (not email):
            raise ValidationError("PhoneNumber or Email is required.")
        if phone:
            try:
                assert int(phone) > 0
            except Exception as e:
                raise ValidationError("Invalid PhoneNumber")
        
        return input_data