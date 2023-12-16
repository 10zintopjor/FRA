import database as db, models as models, schemas as schemas
import sqlalchemy.orm as orm
import passlib.hash as hash
import jwt
import fastapi
import fastapi.security as security
 
oauth2schema = security.OAuth2AuthorizationCodeBearer(tokenUrl="/api/token")


def create_database():
    return db.Base.metadata.create_all(bind=db.engine)

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

async def get_user_by_email_from_db(email: str, db_session: orm.Session):
    return db_session.query(models.User).filter(models.User.email == email).first()

async def  create_user_in_db(user: schemas.UserCreate, db_session: orm.Session):
    user_obj = models.User(email=user.email, hashed_password=hash.bcrypt.hash(user.hashed_pwd))
    db_session.add(user_obj)
    db_session.commit()
    db_session.refresh(user_obj)
    return user_obj



async def authenticate_user(email:str,password:str,db:orm.Session):
    user = await get_user_by_email_from_db(email=email,db_session=db)
    if not user:
        return False
    
    if not user.verify_password(password):
        return False

    return user

JWT_SECRET="1234542t"

async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(),JWT_SECRET)
    return dict(access_token=token,token_type="bearer")


async def get_current_user(db:orm.Session,token:str = fastapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token,JWT_SECRET,algorithms=["HS256"])
        user = db.querry(model.User,)

