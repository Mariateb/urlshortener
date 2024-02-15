from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

import hasher, databaseHandler



app = FastAPI()


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
        theDatabase = databaseHandler.DatabaseHandler()
        if theDatabase.insertLink(url,hashed):
            return HTMLResponse(content=hashed)
        return HTMLResponse(content="erreur avec la bdd", status_code=500)
    return HTMLResponse(content="c'est pas bon", status_code=422)