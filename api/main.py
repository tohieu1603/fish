"""Main API setup with Django Ninja."""
from ninja import NinjaAPI
from api.router import router as main_router

api = NinjaAPI(
    title="Seafood Order Management API",
    version="1.0.0",
    description="API for managing seafood orders with 8-step process",
    docs_url="/docs",
)

# Include main router
api.add_router("", main_router)


@api.get("/health")
def health_check(request):
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}
