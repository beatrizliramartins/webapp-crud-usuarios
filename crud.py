from pathlib import Path
from sqlalchemy import create_engine, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from werkzeug.security import generate_password_hash, check_password_hash


pasta_atual = Path(__file__).parent
PATH_TO_BD = 'bd_usuarios.sqlite'

class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = 'Usuario'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30))
    senha: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(30))
    acesso_gestor: Mapped[bool] = mapped_column(Boolean(), default=False)


    def __repr__(self):
        return f"Usuario({self.id=}, {self.nome=})"
    
    def define_senha(self, senha):
        self.senha = generate_password_hash(senha)
    
    def verifica_senha(self, senha):
        return check_password_hash(self.senha,senha)
    
engine = create_engine(f'sqlite:///{PATH_TO_BD}')    
Base.metadata.create_all(bind=engine)



### CRUD ###

def cria_usuarios(
        nome,
        senha,
        email, 
        **kwarges
):
    with Session(bind=engine) as session:
        usuario = Usuario(
            nome = nome, 
            email = email, 
            **kwarges
        )
        usuario.define_senha(senha)
        session.add(usuario)
        session.commit()

def le_todos_usuarios():
    with Session(bind=engine) as session:
        comando_sql = select(Usuario) 
        usuarios = session.execute(comando_sql).fetchall()
        usuarios = [user[0] for user in usuarios]
        return usuarios
    
def le_usuario_por_id(id):
    with Session(bind=engine) as session:
        comando_sql = select(Usuario).filter_by(id=id)
        usuarios = session.execute(comando_sql).fetchall()
        return usuarios[0][0]

def modifca_usuario(
        id, 
        **kwargs
    ):
    with Session(bind=engine) as session:
        comando_sql = select(Usuario).filter_by(id=id)
        usuarios = session.execute(comando_sql).fetchall()
        for usuario in usuarios:
            for key, value in kwargs.items():
                if key.strip() == 'senha':  
                    usuario[0].define_senha(value)
                else:
                    setattr(usuario[0], key, value)
        session.commit()    

def deleta_usuario(id):
    with Session(bind=engine) as session:
        comando_sql = select(Usuario).filter_by(id=id)
        usuarios = session.execute(comando_sql).fetchall()
        for usuario in usuarios:
            session.delete(usuario[0])
        session.commit()
        

if __name__ == '__main__':
     cria_usuarios(
        'Arthur Martins da Silva Junior',
        senha='biazinha3',
        email='arturcross43@gmail.com',
     ) 

    # usuarios = le_todos_usuarios()
    # usuario_1 = usuarios[1]
    # print(usuario_1)
    # print(usuario_1.nome, usuario_1.email, usuario_1.senha)

