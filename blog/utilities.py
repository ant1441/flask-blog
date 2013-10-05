import datetime
import json
import markdown
from jinja2 import Markup
from blog import log

PARSERS = {"None": Markup.escape,
           u"HTML": lambda x: x,
           u"Markdown": lambda x: markdown.markdown(x,
                                                    html_format='html5',
                                                    extensions=['codehilite'])}


def parse(content, parser=None):
    if unicode(parser) in PARSERS:
        return Markup(PARSERS[unicode(parser)](content))
    else:
        log.error("Parser '%s' called", parser)


def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object.
    """
    json_data = {}
    json_data['fields'] = {}
    json_data['pk'] = getattr(model, 'id')

    for col in model._sa_class_manager.mapper.mapped_table.columns:
        field = getattr(model, col.name)
        if (isinstance(field, datetime.date)
                or isinstance(field, datetime.date)):
            field = field.isoformat()
        try:
            json.dumps(field)
        except TypeError:
            log.debug("%s not json serialisable", field)
            field = None
        json_data['fields'][col.name] = field

    return json.dumps([json_data])
