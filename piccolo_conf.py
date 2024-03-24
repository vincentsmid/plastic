from piccolo.conf.apps import AppRegistry
from piccolo.engine.sqlite import SQLiteEngine

DB = SQLiteEngine(path="main_app/fileinfo.sqlite")
APP_REGISTRY = AppRegistry(apps=["main_app.piccolo_app", "piccolo_admin.piccolo_app"])

DATABASES = {"default": DB}
