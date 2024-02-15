from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

import hasher


def databaseGet(name):#TODO: enlever ça dans la prod
    if name == "test":#TODO: enlever ça dans la prod
        return "https://www.youtube.com"#TODO: enlever ça dans la prod
    return None #TODO: enlever ça dans la prod


app = FastAPI()


@app.get("/{shortName}", response_class=RedirectResponse)
async def reroute(shortName):
    """
    reroute to the website linked or send an error response
    :param shortName: the shortened name
    :return a redirection or the error response:
    """
    if databaseGet(shortName):
        return RedirectResponse(url=databaseGet(shortName))
    return HTMLResponse(content="c'est pas bon : "+shortName, status_code=404)

@app.post("/create", response_class=HTMLResponse)
async def create(url: str = "", size: int = 8):
    """
    allows to create a short link by giving in the post the URL as a parameter
    :param url: the url to shorten
    :param size: the size of the shortened url requested
    :return the response:
    """
    myHasher = hasher.Hasher()
    hashed = myHasher.hashString(url, size)
    if url != "" and hashed:
        return HTMLResponse(content=hashed)
    return HTMLResponse(content="c'est pas bon", status_code=422)