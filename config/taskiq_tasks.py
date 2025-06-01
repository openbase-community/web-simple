import logging
from importlib import import_module

from config.app_packages import get_package_apps

logger = logging.getLogger(__name__)

# Add enabled site tasks
for app in get_package_apps():
    tasks_module = import_module(f"{app}.tasks")
