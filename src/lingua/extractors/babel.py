from . import EXTENSIONS
from . import EXTRACTORS
from . import Message

DEFAULT_KEYWORDS = {
        '_': None,
        'gettext': None,
        'ngettext': (1, 2),
        'ugettext': None,
        'ungettext': (1, 2),
        'dgettext': (2,),
        'dngettext': (2, 3),
        'N_': None,
        'pgettext': ((1, 'c'), 2)
        }


def babel_wrapper(extractor):
    def wrapper(filename, options):
        fileobj = open(filename, 'rb')
        for (lineno, _, msgid, comment) in extractor(fileobj, DEFAULT_KEYWORDS.keys(), (), None):
            yield Message(None, msgid, u'', [], comment, None, (filename, linno))
    wrapper.__doc__ = extractor.__doc__
    return wrapper


def register_babel_plugins():
    try:
        from pkg_resources import working_set
    except ImportError:
        return
    for entry_point in working_set.iter_entry_points('babel.extractors'):
        extractor = babel_wrapper(entry_point.load(require=True))
        EXTRACTORS['babel-%s' % entry_point.name] = extractor
