from typing import Annotated

from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import databaseHandler
import hasher

app = FastAPI()
templates = Jinja2Templates('templates')


def get_logged_user(cookie: Cookie):
    theDatabase = databaseHandler.DatabaseHandler()

    if cookie is not None:
        return theDatabase.get_user(cookie)

    return None


@app.get('/')
async def home(request: Request):
    """
    Homepage
    """
    return templates.TemplateResponse(
        request=request,
        name='home.html',
        context={'isLogged': request.cookies.get('Authorization') is not None}
    )


@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')


@app.get('/register')
async def register(request: Request):
    return templates.TemplateResponse(request=request, name='register.html')


@app.get('/disconnect')
async def disconnect():
    theResponse = RedirectResponse(url='/')
    theResponse.delete_cookie('Authorization')
    return theResponse


@app.get('/urls', response_class=HTMLResponse)
async def get_all_urls(request: Request):
    theDatabase = databaseHandler.DatabaseHandler()
    urls = theDatabase.get_all_urls()

    return templates.TemplateResponse(
        request=request,
        name='urls.html',
        context={'urls': urls}
    )


@app.get("/user/urls", response_class=HTMLResponse)
async def get_user_urls(request: Request):
    theDatabase = databaseHandler.DatabaseHandler()
    urls = theDatabase.get_user_urls(get_logged_user(request.cookies.get('Authorization')))

    return templates.TemplateResponse(
        request=request,
        name='user-urls.html',
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
        if not link.startswith("https://") and not link.startswith("http://"):
            link = "https://" + link
        return RedirectResponse(url=link)
    return templates.TemplateResponse(request=request, name='not-found.html', status_code=404)


@app.post("/create", response_class=HTMLResponse)
async def create(request: Request, url: Annotated[str, Form()], duration: Annotated[int, Form()], size: Annotated[int, Form()]):
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
    user = get_logged_user(request.cookies.get('Authorization'))
    print(user, request.cookies.get('Authorization'))
    if url != "" and hashed:
        theDatabase = databaseHandler.DatabaseHandler()
        if theDatabase.insert_link(url, hashed, user, duration=duration):
            return templates.TemplateResponse(
                request=request, name='shortened-url.html', context={'url': 'http://localhost:8000/' + hashed})
    return HTMLResponse(content="c'est pas bon", status_code=422)


@app.post("/login")
def login(request: Request, login: Annotated[str, Form()], password: Annotated[str, Form()]):
    theDatabase = databaseHandler.DatabaseHandler()

    user = theDatabase.get_user(login)
    if user is None:
        return templates.TemplateResponse(request=request, name='login.html', status_code=404, context={
            'message': "L'utilisateur n'existe pas"
        })

    if theDatabase.get_password(login)[0] != hasher.hash_password(password):
        return templates.TemplateResponse(request=request, name='login.html', status_code=401, context={
            'message': "Mot de passe incorrect"
        })

    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="Authorization", value=login)

    return response


@app.post("/register")
def register(request: Request, login: Annotated[str, Form()], password: Annotated[str, Form()]):
    theDatabase = databaseHandler.DatabaseHandler()
    if theDatabase.get_user(login) is not None:
        return templates.TemplateResponse(request=request, name='register.html', context={
            'message': "Identifiant déjà pris"
        })
    theDatabase.create_user(login, hasher.hash_password(password))
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="Authorization", value=login)

    return response

@app.post("/delete")
def delete(request: Request, url: Annotated[str, Form()]):
    theDatabase = databaseHandler.DatabaseHandler()
    if theDatabase.delete_link(url):
        return RedirectResponse(url="/user/urls", status_code=302)
    return HTMLResponse(content="c'est pas bon", status_code=422)