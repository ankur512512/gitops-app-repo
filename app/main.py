from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.settings import settings
from app.db import db_ready, init_db, SessionLocal
from app.auth import DEMO_USER, verify_password, create_access_token, decode_token
from app.models import User
from sqlalchemy.exc import IntegrityError


app = FastAPI(title=settings.APP_NAME)
init_db()
bearer = HTTPBearer(auto_error=False)

class LoginIn(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class SignupIn(BaseModel):
    username: str
    password: str

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/meta")
def meta():
    return {
        "app": settings.APP_NAME,
        "env": settings.ENV,
        "git_sha": settings.GIT_SHA,
        "build_time": settings.BUILD_TIME,
        "image_tag": settings.IMAGE_TAG,
    }


@app.post("/signup")
def signup(body: SignupIn):
    with SessionLocal() as db:
        user = User(username=body.username, password=body.password)  # plain for now
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=409, detail="username already exists")
    return {"status": "created", "username": body.username}


@app.post("/login", response_model=TokenOut)
def login(body: LoginIn):
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == body.username).first()
        if not user or user.password != body.password:
            raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_access_token(sub=body.username, roles=["user"])
    return TokenOut(access_token=token)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "env": settings.ENV}

@app.get("/readyz")
def readyz():
    ok, msg = db_ready()
    if not ok:
        raise HTTPException(status_code=503, detail={"status": "not-ready", "db": msg})
    return {"status": "ready", "db": "ok"}

@app.post("/login", response_model=TokenOut)
def login(body: LoginIn):
    if body.username != DEMO_USER["username"]:
        raise HTTPException(status_code=401, detail="invalid credentials")
    if not verify_password(body.password):
        raise HTTPException(status_code=401, detail="invalid credentials")


    token = create_access_token(sub=body.username, roles=DEMO_USER["roles"])
    return TokenOut(access_token=token)

@app.get("/whoami")
def whoami(creds: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if creds is None:
        raise HTTPException(status_code=401, detail="missing bearer token")
    try:
        claims = decode_token(creds.credentials)
        return {"user": claims.get("sub"), "roles": claims.get("roles"), "issuer": claims.get("iss")}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
