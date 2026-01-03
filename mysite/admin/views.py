from sqladmin import ModelView

from mysite.database.models import UserProfile, Category, SubCategory, Product, ProductImage, Review

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]


class SubCategoryAdmin(ModelView, model=SubCategory):
    column_list = [SubCategory.id, SubCategory.sub_category_name]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.product_name]

class ProductImageAdmin(ModelView, model=ProductImage):
    column_list = [ProductImage.id]

class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.text]

