# Middlewares

# Middleware registration is done in app.py using dp.message.middleware(...)
# This file is intentionally minimal

from .throttling import ThrottlingMiddleware
from .admin_middleware import AdminMiddleware

__all__ = ['ThrottlingMiddleware', 'AdminMiddleware']
