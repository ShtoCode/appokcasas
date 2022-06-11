from models.entities.Usuario import Usuario


class ModelUsuario():
    @classmethod
    def login(self, con, usuario):
        try:
            cursor = con.cursor()
            sql = "SELECT * FROM usuario WHERE email = (:1)".format(usuario.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                usuario = Usuario(row[0], row[1], row[2], row[3], Usuario.check_password(row[4]), usuario.password)
                return usuario
            else:
                return None
        
        except Exception as ex:
            raise Exception(ex)

