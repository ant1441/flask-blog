from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.login import current_user
from app import db, admin
from models import User, Post, Category


class DatabaseAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()


class UserAdmin(ModelView):
    column_exclude_list = ['about_me', 'salt', 'password']
    column_sortable_list = ('username',
                            'email',
                            'role',
                            'created_at',
                            'first_name',
                            'last_name',
                            'last_modified',
                            'active')
    column_searchable_list = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, session):
        super(UserAdmin, self).__init__(User, session)


class PostAdmin(ModelView):
    column_sortable_list = ('title', ('author', User.username), 'created_on')

    def __init__(self, session):
        super(PostAdmin, self).__init__(Post, session)


class CategoryAdmin(ModelView):

    def __init__(self, session):
        super(CategoryAdmin, self).__init__(Category, session)

admin.add_view(UserAdmin(db.session))
admin.add_view(PostAdmin(db.session))
admin.add_view(CategoryAdmin(db.session))
