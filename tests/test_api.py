
import unittest
import db
from . import User



class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            username='test'
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

if __name__ == '__main__':
    unittest.main()