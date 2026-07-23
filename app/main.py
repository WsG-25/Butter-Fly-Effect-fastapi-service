from fastapi import FastAPI

#Creating a class instance for fastapi

app = FastAPI()

#Creating a root route

@app.get("/")
def root():
    return {"message": "Hello World"}

#Creating a hello route
#This route will take a name as a parameter and return a message with the name


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}

# FastAPI will convert the language to Postman for JSON formatting.