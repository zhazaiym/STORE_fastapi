from fastapi import FastAPI
from mysite.admin.setup import setup_admin
from mysite.api import users, auth
import uvicorn

from mysite.api.category import category_router
from mysite.api.review import review_router
from mysite.api.product import product_router
from mysite.api.product_images import product_image_router
from mysite.api.subcategory import subcategory_router

shop_app = FastAPI(title='Shop Site')
shop_app.include_router(users.user_router)
shop_app.include_router(product_router)
shop_app.include_router(product_image_router)
shop_app.include_router(review_router)
shop_app.include_router(category_router)
shop_app.include_router(subcategory_router)
shop_app.include_router(auth.auth_router)
setup_admin(shop_app)
if __name__ == '__main__':
    uvicorn.run(shop_app, host='127.0.0.1', port=8000)

