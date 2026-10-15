try:
    import MySQLdb
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None
except (ImportError, ModuleNotFoundError):
    pass
