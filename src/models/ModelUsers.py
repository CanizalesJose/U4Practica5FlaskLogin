from .entities.users import User

class ModelUsers():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute(
                "call sp_verifyIdentity(%s, %s)",
                (user.username, user.password)
            )
            row = cursor.fetchone()
            if row[0] != None:
                user = User(row[0], row[1], row[2], row[4], row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    # Crear método que retorna a partir del id, los datos en una instancia User desde la base de datos
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select id, username, usertype, fullname from users where id = %s", (id))
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
