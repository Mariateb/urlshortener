from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

#import database, hasher TODO: mettre les bonnes importations

def databaseGet(name):#TODO: enlever ça dans la prod
    if name == "test":#TODO: enlever ça dans la prod
        return "https://www.youtube.com"#TODO: enlever ça dans la prod
    return None #TODO: enlever ça dans la prod


def hasherTest():#TODO: enlever ça dans la prod
    return True #TODO: enlever ça dans la prod

app = FastAPI()

###TODO: modifier variables hasher, database

@app.get("/{shortName}", response_class=RedirectResponse)
def reroute(shortName):
    """
    reroute to the website linked or send an error response
    :param shortName:
    :return a redirection or the error response:
    """
    if databaseGet(shortName) != None:
        return RedirectResponse(url=databaseGet(shortName))
    return HTMLResponse(content="c'est pas bon : "+shortName, status_code=500)#TODO: trouver un vrai code d'erreur

@app.post("/create", response_class=HTMLResponse)
def create():
    """
    allows to create a short link by giving in the post the URL as a parameter
    :return the response:
    """
    if hasherTest():#TODO: use the URL parameter
        return HTMLResponse(content="c'est ok")
    return HTMLResponse(content="c'est pas bon", status_code=500)#TODO: trouver un vrai code d'erreur


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, log_level="info", reload=True)