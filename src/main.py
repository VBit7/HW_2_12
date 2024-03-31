import fastapi
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

import contacts.routes
import contacts.exceptions
import database


app = fastapi.FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.routes.router, prefix='/api')


@app.get("/")
def index():
    return {"message": "Contacts Application"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = fastapi.Depends(database.get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise fastapi.HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise fastapi.HTTPException(status_code=500, detail="Error connecting to the database")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="localhost", port=8000, reload=True
    )
