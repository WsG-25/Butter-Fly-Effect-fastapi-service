from fastapi import FastAPI
<<<<<<< HEAD

=======
>>>>>>> WsG
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}