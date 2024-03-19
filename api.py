from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import databaseHandler
import hasher
import randomGenerator

app = FastAPI()
templates = Jinja2Templates('templates')


@app.get('/')
async def home(request: Request):
    """
    Homepage
    """
    return templates.TemplateResponse(request=request, name='home.html')


@app.get("/{shortName}", response_class=RedirectResponse)
async def reroute(request: Request, shortName):
    """
    reroute to the website linked or send an error response
    :param request: request Object
    :param shortName: the shortened name
    :return a redirection or the error response:
    """
    theDatabase = databaseHandler.DatabaseHandler()
    theDatabase.deleteOldLinks()
    link = theDatabase.getLink(shortName)
    if link:
        theDatabase.addVisitor(shortName)
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

    myGenerator = randomGenerator.RandomGenerator()
    shortened = myGenerator.generate(size)
    if url != "" and shortened:
        theDatabase = databaseHandler.DatabaseHandler()
        if theDatabase.insertLink(url, shortened, duration=duration):
            return templates.TemplateResponse(
                request=request, name='shortened-url.html', context={'url': 'http://localhost:8000/' + shortened})
    return HTMLResponse(content="c'est pas bon", status_code=422)
