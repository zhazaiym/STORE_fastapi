from .views import UserProfileAdmin, CategoryAdmin,SubCategoryAdmin, ProductAdmin, ProductImageAdmin, ReviewAdmin
from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine

def setup_admin(mysite_app: FastAPI):
    admin = Admin(mysite_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(SubCategoryAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ProductImageAdmin)
    admin.add_view(ReviewAdmin)

