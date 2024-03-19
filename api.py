import datetime
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
    """
    Homepage
    """
    return templates.TemplateResponse(
        request=request,
        name='home.html',
        context={'isLogged': request.cookies.get("token") is not None}
    )


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

@app.get("/printURL_ALL", response_class=HTMLResponse)
async def print_all_urls(request: Request):
    # Récupérez toutes les URL raccourcies depuis la base de données
    theDatabase = databaseHandler.DatabaseHandler()
    shortened_urls, origined_urls = theDatabase.get_shortened_urls_from_database_all()

    # Créez le contenu du tableau HTML
    urls = []
    for url_Short, url_origne in zip(shortened_urls, origined_urls):
        urls.append({'url_Short': url_Short, 'url_origne': url_origne})  # Correction ici

    # Utilisez un template pour générer la page HTML
    return templates.TemplateResponse(
        request=request,
        name='print_URL_ALL.html',
        context={'urls': urls}
    )

@app.get("/printURL_USER", response_class=HTMLResponse)
async def print_all_urls(request: Request):
    # Récupérez toutes les URL raccourcies depuis la base de données
    theDatabase = databaseHandler.DatabaseHandler()
    shortened_urls, origined_urls = theDatabase.get_shortened_urls_from_database_user(request.cookies.get("token"))

    # Créez le contenu du tableau HTML
    urls = []
    for url_Short, url_origne in zip(shortened_urls, origined_urls):
        urls.append({'url_Short': url_Short, 'url_origne': url_origne})  # Correction ici

    # Utilisez un template pour générer la page HTML
    return templates.TemplateResponse(
        request=request,
        name='print_URL_ALL.html',
        context={'urls': urls}
    )


@app.get("/{shortName}", response_class=RedirectResponse)
async def redirect(shortName, request: Request):
    """
    reroute to the website linked or send an error response
    :param request: request Object
    :param shortName: the shortened name
    :return a redirection or the error response:
    """
    theDatabase = databaseHandler.DatabaseHandler()
    theDatabase.delete_old_links()
    link = theDatabase.get_link(shortName)
    if link:
        return RedirectResponse(url=link)
    return templates.TemplateResponse(request=request, name='not-found.html', status_code=404)


@app.post("/create", response_class=HTMLResponse)
async def create(request: Request, url: Annotated[str, Form()], duration: Annotated[int, Form()],
                 size: Annotated[int, Form()]):
    """
    Allows to create a short link by giving in the post the URL as a parameter

    :param request:
    :param url: the url to shorten
    :param duration: the time period before we can delete the URL in days
    :param size: the size of the shortened url requested
    :return the response:
    """
    myHasher = hasher.Hasher()
    hashed = myHasher.hash_string(url, size)
    if url != "" and hashed:
        theDatabase = databaseHandler.DatabaseHandler()
        try:
            if theDatabase.insert_link(url, hashed, duration=duration):
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
    token = theDatabase.create_user(login, hasher.hash_password(password))
    if token:
        max_age = 3600 * 24  # one day
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                             "%a, %d-%b-%Y %H:%M:%S GMT")

        theResponse = RedirectResponse(status_code=302, url="/")
        theResponse.set_cookie("token", str(token), max_age=max_age, expires=expires)
        return theResponse
    return templates.TemplateResponse(request=request, name='register.html')


@app.post("/authenticate", response_class=HTMLResponse)
async def authenticate(request: Request, login: Annotated[str, Form()], password: Annotated[str, Form()]):
    theDatabase = databaseHandler.DatabaseHandler()
    token = theDatabase.get_user(login, hasher.hash_password(password))
    print(token)
    if token:
        max_age = 3600 * 24  # one day
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                             "%a, %d-%b-%Y %H:%M:%S GMT")

        theResponse = RedirectResponse(status_code=302, url="/")
        theResponse.set_cookie("token", str(token), max_age=max_age, expires=expires)
        return theResponse
    return templates.TemplateResponse(request=request, name='login.html')
