from flask_restx import Namespace, Resource, fields


namespace = Namespace(name="Identity Namespace", path='/')

@namespace.route('/identity')
class IdentityView(Resource):
    POST_DOC_MODEL = namespace.model(
        "Identity",
        {
            "email": fields.String(example="shyamsar30@gmail.com", description="Email Address"),
            "phoneNumber": fields.String(example="1234567898", description="Mobile Number")
        }
    )

    @namespace.expect(POST_DOC_MODEL)
    def post(self):
        return "hii"