import datetime
import time
from sqlite3 import IntegrityError, OperationalError
from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import databaseHandler
import hasher

app = FastAPI()
templates = Jinja2Templates('templates')


@app.get('/')
async def home(request: Request):
    if request.cookies.get("token"):
        return templates.TemplateResponse(request=request, name='home-connected.html')
    return templates.TemplateResponse(request=request, name='home.html')

@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')

@app.get('/register')
async def login(request: Request):
    return templates.TemplateResponse(request=request, name='register.html')

@app.get('/disconnect')
async def disconnect():
    theResponse = RedirectResponse(url='http://localhost:8000/')
    theResponse.delete_cookie("token")
    return theResponse

@app.get("/{shortName}", response_class=RedirectResponse)
async def redirect(shortName):
    """
    reroute to the website linked or send an error response
    :param shortName: the shortened name
    :return a redirection or the error response:
    """
    theDatabase = databaseHandler.DatabaseHandler()
    link = theDatabase.getLink(shortName)
    if link:
        return RedirectResponse(url=link)
    return HTMLResponse(content="c'est pas bon : " + shortName, status_code=404)


@app.post("/create", response_class=HTMLResponse)
async def create(request: Request, url: Annotated[str, Form()], size: Annotated[int, Form()]):
    """
    allows to create a short link by giving in the post the URL as a parameter
    :param request:
    :param url: the url to shorten
    :param size: the size of the shortened url requested
    :return the response:
    """
    myHasher = hasher.Hasher()
    hashed = myHasher.hashString(url, size)
    if request.cookies.get("token"):
        return HTMLResponse(content="oui ! ton cookie token est : " + request.cookies.get("token"))
    if url != "" and hashed:
        theDatabase = databaseHandler.DatabaseHandler()
        try:
            if theDatabase.insertLink(url,hashed):
                return templates.TemplateResponse(
                    request=request,
                    name='shortened-url.html',
                    context={'url': 'http://localhost:8000/' + hashed}
                )
        except IntegrityError:
            return templates.TemplateResponse(
                    request=request,
                    name='shortened-url.html',
                    context={'url': 'http://localhost:8000/' + hashed}
                )
        except OperationalError:
            return templates.TemplateResponse(request=request, name='home.html', status_code=500)
        return HTMLResponse(content="erreur avec la bdd", status_code=500)
    return HTMLResponse(content="c'est pas bon", status_code=422)

@app.post("/registerUser", response_class=HTMLResponse)
async def registerUser(request: Request, login: Annotated[str, Form()], password: Annotated[str, Form()]):
    theDatabase = databaseHandler.DatabaseHandler()
    ##TODO: securiser mdp
    token = theDatabase.register(login, password)
    if token:
        max_age = 3600 * 24  # one day
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                             "%a, %d-%b-%Y %H:%M:%S GMT")

        theResponse = templates.TemplateResponse(request=request, name='home-connected.html')
        theResponse.set_cookie("token", str(token), max_age=max_age, expires=expires)
        return theResponse
    return templates.TemplateResponse(request=request, name='register.html')

@app.post("/authenticate", response_class=HTMLResponse)
async def authenticate(request: Request, login: Annotated[str, Form()], password: Annotated[str, Form()]):
    theDatabase = databaseHandler.DatabaseHandler()
    ##TODO: securiser mdp
    token = theDatabase.authenticate(login, password)
    if token:
        max_age = 3600 * 24 #one day
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")

        theResponse = templates.TemplateResponse(request=request, name='home-connected.html')
        theResponse.set_cookie("token",str(token), max_age=max_age, expires=expires)
        return theResponse
    return templates.TemplateResponse(request=request, name='login.html')