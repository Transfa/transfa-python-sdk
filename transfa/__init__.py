# Transfa Python bindings
# API docs at http://docs.transfapp.com
# Authors:
# Kolawole Mangabo <kolawole.mangabo@transfapp.com>
# Atinho Ruben <atinhoruben@transfapp.com>

# Configuration variables

api_key = None
private_secret = None
api_base = "https://api.transfapp.com"
verify_ssl = True
default_auth_header_bearer = "Api-Transfa-Key"


# API Resources

from transfa.api_resources import *

# Webhook

from transfa.webhook import *
