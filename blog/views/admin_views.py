from flask.ext.admin import BaseView
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.login import current_user
from blog import db, admin
from blog.models import User, Post, Category, CodeType
from blog.views import log


class AuthView(BaseView):
    def is_accessible(self):
        log.debug("Checking Authentication")
        return current_user.is_authenticated()


class DatabaseAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()


class UserAdmin(ModelView, AuthView):
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
        log.debug("Creating User View")
        super(UserAdmin, self).__init__(User, session)


class PostAdmin(ModelView, AuthView):
    column_sortable_list = ('title', ('author', User.username), 'created_at')
    column_searchable_list = ('title', 'content')

    def __init__(self, session):
        super(PostAdmin, self).__init__(Post, session)


class CategoryAdmin(ModelView, AuthView):
    def __init__(self, session):
        super(CategoryAdmin, self).__init__(Category, session)


class CodeTypeAdmin(ModelView, AuthView):
    def __init__(self, session):
        super(CodeTypeAdmin, self).__init__(CodeType, session)


#class BlogFileAdmin(FileAdmin, AuthView):
#    def __init__(self, directory, url, *args, **kwargs):
#        super(BlogFileAdmin, self).__init__(directory,
#                                            url,
#                                            *args,
#                                            **kwargs)


admin.add_view(UserAdmin(db.session))
admin.add_view(PostAdmin(db.session))
admin.add_view(CategoryAdmin(db.session))
admin.add_view(CodeTypeAdmin(db.session))
#admin.add_view(BlogFileAdmin('static', '', name="Static Files"))
