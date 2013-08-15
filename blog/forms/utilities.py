from blog.models import CodeType
from blog.forms import log


def code_types():
    types = CodeType.query.all()
    log.debug(types)
    return types
