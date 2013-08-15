import markdown
from jinja2 import Markup
from blog import log

PARSERS = {"None": Markup.escape,
           u"HTML": lambda x: x,
           u"Markdown": lambda x: markdown.markdown(x, html_format='html5')}


def parse(content, parser=None):
    if unicode(parser) in PARSERS:
        return Markup(PARSERS[unicode(parser)](content))
    else:
        log.error("Parser '%s' called", parser)
