from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


app = FastAPI()


@app.get("/favicon.ico")
async def get_favicon():
    raise HTTPException(status_code=404)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_all_users")
async def get_all_users():
    response = supabase.table("users").select("*").execute()
    return response


@app.get("/get_all_modules")
async def get_all_modules():
    response = supabase.table('modules').select("*").execute()
    return response


@app.get("/get_module")
async def get_module(id : int):
    response = supabase.table('modules').select("*").eq("module_id", id).execute()
    return response


@app.post("/create_module")
async def create_module(module_name : str, owner_id : int):

    if module_name == "":
        return HTTPException(status_code=404, detail="Valid username is required.")
    
    data, count = supabase.table('modules').insert({'name': module_name, 'owner_id': owner_id}).execute()
    return data


@app.post("/create_linkage")
async def generate_link(parent_id : int, child_id : int):

    if parent_id < 0 or child_id < 0:
        return HTTPException(status_code=404, detail="Valid parent and child are required.")

    query_string = f"module_id.eq.{parent_id},module_id.eq.{child_id}"
    response = supabase.table('modules').select("*").or_(query_string).execute()
    if len(response.data) != 2:
        return HTTPException(status_code=404, detail=f"Valid parent and child are required. Only {len(response.data)} / 2 items are found in database. Data found: {response.data}") 

    data, _ = supabase.table('linkages').insert({'parent': parent_id, 'child': child_id}).execute()

    return data


import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 4000)))
