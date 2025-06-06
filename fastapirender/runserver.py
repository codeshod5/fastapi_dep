import uvicorn
from fastapirender.src import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("runserver:app", host="127.0.0.1", port=8000, reload=True)
