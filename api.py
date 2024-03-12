from typing import Annotated, List, Tuple

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import databaseHandler
import hasher
import html

import sqlite3

app = FastAPI()
templates = Jinja2Templates('templates')

@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse(request=request, name='home.html')

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
    shortened_urls, origined_urls = theDatabase.get_shortened_urls_from_database_user()

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
async def reroute(shortName):
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
    if url != "" and hashed:
        theDatabase = databaseHandler.DatabaseHandler()
        if theDatabase.insertLink(url, hashed):
            return templates.TemplateResponse(
                request=request, name='shortened-url.html', context={'url': 'http://localhost:8000/' + hashed})
        return HTMLResponse(content="erreur avec la bdd", status_code=500)
    return HTMLResponse(content="c'est pas bon", status_code=422)



