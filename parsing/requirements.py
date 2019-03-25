from .basic import *

require_key = Or([':strips', ':typing', ':negative-preconditions'])
require_def = lp + Suppress(':requirements') + OneOrMore(require_key) + rp
