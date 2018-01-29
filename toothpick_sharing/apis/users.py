from flask_restplus import Namespace, Resource, fields
from ..dal import User, db

ns = Namespace('users')

user_model = ns.model('User', {
    'id': fields.Integer(description='user unique identifier', example='42'),
    'name': fields.String(description='user full name', example='Jack Daniels'),
})

@ns.route('/users/<int:user_id>')
class UserResource(Resource):

    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Retrieves user by ID"""
        return get_user_or_abort(user_id)

@ns.route('/users')
class UserCollectionResource(Resource):

    @ns.marshal_with(user_model, as_list=True)
    def get(self):
        """Retreives collection of all known users"""
        return User.query.all()

    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def post(self):
        """Creates new user"""
        user = User(**self.api.payload)
        db.session.add(user)
        db.session.commit()
        return user

def get_user_or_abort(id, api=ns):
    user = User.query.filter_by(id=id).first()

    if not user:
        api.abort(404, 'User with id=<%s> not found' % id)

    return user