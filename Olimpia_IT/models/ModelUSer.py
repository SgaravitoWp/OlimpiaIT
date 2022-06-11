from .entities.user import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            session = db.session()
            sql = f" SELECT username, password FROM Users WHERE username = '{user.username}'"
            cursor = session.execute(sql).cursor
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], User.check_password(row[1], user.password))
                return user
            else:
                return None

        except Exception as e:
            raise Exception(e)