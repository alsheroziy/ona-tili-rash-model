from aiogram import Router
from .users import registration, test_handler, menu
from .admins import admin_panel


def setup_routers() -> Router:
    router = Router()

    # Admin handlers (higher priority)
    router.include_router(admin_panel.router)

    # User handlers
    router.include_router(registration.router)
    router.include_router(test_handler.router)
    router.include_router(menu.router)

    return router
