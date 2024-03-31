import fastapi
import fastapi.responses

def item_not_found_error_handler(request, exc):
    return fastapi.responses.JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content={
            "code": exc.status_code,
            "message": exc.detail
        }
    )
