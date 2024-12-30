from datetime import datetime, timedelta, timezone

from typing import Annotated, Union
import sqlite3
import jwt

from fastapi import Depends, FastAPI, HTTPException, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jwt.exceptions import InvalidTokenError

from passlib.context import CryptContext

from pydantic import BaseModel

from db_handler import init_db, get_user_from_email,get_all_trackers,get_tracker_details



# to get a string like this run:

# openssl rand -hex 32

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30



init_db()





class Token(BaseModel):

    access_token: str

    token_type: str





class TokenData(BaseModel):

    email: Union[str, None] = ""





class User(BaseModel):

    id: int

    email: Union [str, None] = ""

    password: Union [str, None] = ""

    disabled: Union [bool, None] = ""





class UserInDB(User):

    id: int

    email: str

    password: str





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



app = FastAPI()





def verify_password(plain_password, hashed_password):

    return pwd_context.verify(plain_password,hashed_password)





def get_password_hash(password):

    return pwd_context.hash(password)





def get_user(email: str):

    user_dict = get_user_from_email(email)

    if user_dict:

        return UserInDB(**user_dict)

    return None





def authenticate_user(email: str, password: str):

    user = get_user(email)

    if not user:

        return False

    if not verify_password(password, user.password):

        return False

    return user





def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):

    to_encode = data.copy()

    if expires_delta:

        expire = datetime.now(timezone.utc) + expires_delta

    else:

        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt





async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    credentials_exception = HTTPException(

        status_code=status.HTTP_401_UNAUTHORIZED,

        detail="Could not validate credentials",

        headers={"WWW-Authenticate": "Bearer"},

    )

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("sub")

        if email is None:

            raise credentials_exception

        token_data = TokenData(email=email)

    except InvalidTokenError:

        raise credentials_exception

    user = get_user(email=token_data.email)

    if user is None:

        raise credentials_exception

    return user





async def get_current_active_user(

    current_user: Annotated[User, Depends(get_current_user)],

):

    if current_user.disabled:

        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user





@app.post("/token")

async def login_for_access_token(

    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],

) -> Token:

    print(form_data)

    user = authenticate_user(form_data.username, form_data.password)

    if not user:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Incorrect username or password",

            headers={"WWW-Authenticate": "Bearer"},

        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(

        data={"sub": user.email}, expires_delta=access_token_expires

    )

    return Token(access_token=access_token, token_type="bearer")




@app.get("/users/me/", response_model=User)

async def read_users_me(

    current_user: Annotated[User, Depends(get_current_active_user)],  # Mettre demain cette partie dans toutes les autres fonctionns pour ue mon application soit securisée

):

    return current_user



# Protection par JWT
@app.get("/trackers")
async def get_trackers(
    current_user: Annotated[User, Depends(get_current_active_user)]):

    """
    Endpoint pour récupérer tous les trackers et leur dernière heure de ping.
    """
    try:
        return get_all_trackers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/trackers/{imei}")
async def get_tracker(imei: str):
    """
    Endpoint pour récupérer les détails d'un tracker spécifique.
    """
    try:
        tracker = get_tracker_details(imei)
        if tracker is None:
            raise HTTPException(status_code=404, detail="Tracker non trouvé")
        return tracker
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Il faudrait que lorsque je clique sur une date non existante pour la trace erreur est  a enlever puisue jeen peux toujours pas envoyer  a qui que ce soit

@app.get("/traces")
async def get_traces(imei: str,
                     date: str,
                     current_user: Annotated[User, Depends(get_current_active_user)]):

    """
    Endpoint pour récupérer les traces d'un tracker spécifique à une date donnée.
    """
    try:
        # Conversion de la date au format YYMMDD
        query_date = date[2:4] + date[5:7] + date[8:10]  # Transforme YYYY-MM-DD en YYMMDD

        # Requête pour récupérer les données
        conn = sqlite3.connect("tracking_data.db")
        cursor = conn.cursor()
        query = """
        SELECT latitude, longitude, date
        FROM tracking_data
        WHERE imei = ? AND date = ?
        """
        cursor.execute(query, (imei, query_date))
        rows = cursor.fetchall()
        conn.close()

        # Transformer les résultats en liste de dictionnaires
        traces = [{"lat": row[0], "lng": row[1], "datetime": row[2]} for row in rows]

        # Retourne une liste vide si aucune trace n'est trouvée
        return traces

    except ValueError:
        # Gère une date invalide
        raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez 'YYYY-MM-DD'.")
    except Exception as e:
        # Retourne une erreur interne si une exception inattendue survient
        raise HTTPException(status_code=500, detail="Erreur serveur: " + str(e))







