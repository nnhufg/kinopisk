from dotenv import load_dotenv
from split_settings.tools import include


load_dotenv()

include(
    'components/database.py',
    'components/base.py',
    'components/apps.py',
    'components/auth.py',
    'components/middleware.py',
    'components/static.py',
    'components/templates.py',
    'components/drf.py',
) 

