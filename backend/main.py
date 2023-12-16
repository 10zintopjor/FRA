import fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
import services
import schemas

app = fastapi.FastAPI()

@app.post("/api/users")
async def create_user(
    user: schemas.UserCreate,
    db: orm.Session = fastapi.Depends(services.get_db),
):
    db_user = await services.get_user_by_email_from_db(user.email, db)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email Already Exists")
    return await services.create_user_in_db(user, db)


@app.post("/api/token")
async def generate_token(
    form_data:security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: orm.Session = fastapi.Depends(services.get_db)
):
    user = await services.authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise fastapi.HTTPException(status_code=401,detail="Invalid Transaction")
    
    return await services.create_token(user)

