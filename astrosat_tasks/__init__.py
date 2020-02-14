"""
   _____            __                               __
  /  _  \   _______/  |________  ____  ___________ _/  |_
 /  /_\  \ /  ___/\   __\_  __ \/  _ \/  ___/\__  \\   __\
/    |    \\___ \  |  |  |  | \(  <_> )___ \  / __ \|  |
\____|__  /____  > |__|  |__|   \____/____  >(____  /__|
        \/     \/                         \/      \/
___________              __
\__    ___/____    _____|  | __  ______
  |    |  \__  \  /  ___/  |/ / /  ___/
  |    |   / __ \_\___ \|    <  \___ \
  |____|  (____  /____  >__|_ \/____  >
               \/     \/     \/     \/
"""

APP_NAME = "astrosat_tasks"

VERSION = (0, 0, 1)

__title__ = "django-astrosat-users"
__author__ = "Allyn Treshansky"
__version__ = ".".join(map(str, VERSION))

default_app_config = f"{APP_NAME}.apps.AstrosatTasksConfig"
