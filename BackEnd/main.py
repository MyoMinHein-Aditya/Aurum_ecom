"""
main.py
FastAPI entry point, mounts static files, registers routers, adds middlewares.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from BackEnd.middleware.security import SecurityHeadersMiddleware
from BackEnd.database.connection import Base, engine
import os

from BackEnd.routes.auth import router as auth_router
from BackEnd.routes.products import router as products_router
from BackEnd.routes.cart import router as cart_router
from BackEnd.routes.orders import router as orders_router
from BackEnd.routes.admin import router as admin_router

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Aurum",
    description="Luxury SaaS e-commerce platform API",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log exception here if using logging module
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "code": 500}
    )

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # Ensure FrontEnd directory exists so StaticFiles doesn't crash
    os.makedirs("FrontEnd", exist_ok=True)

# Register routers
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(products_router, prefix="/api/v1/products")
app.include_router(cart_router, prefix="/api/v1/cart")
app.include_router(orders_router, prefix="/api/v1/orders")
app.include_router(admin_router, prefix="/api/v1/admin")

# Mount FrontEnd
app.mount("/", StaticFiles(directory="FrontEnd", html=True), name="frontend")
