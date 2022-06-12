from marshmallow import Schema, fields

class InfoSchema(Schema):
    message = fields.String(required=None)
    score = fields.Integer()
    results = fields.List(fields.Dict(keys=fields.String(), values=fields.String(), required=False))