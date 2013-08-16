from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from blog.models import Post


class PostLogic(Post):
    """
    A layer class for the Post sqlalchemy class which will contain any
    relevant business logic.
    """
    @hybrid_property
    def visible(self):
        return ~self.hidden

    def date(self, format_="%d %b %y"):
        return datetime.strftime(self.created_at, format_)
