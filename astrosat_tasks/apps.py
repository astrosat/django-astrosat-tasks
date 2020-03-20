from django.apps import AppConfig

from astrosat_tasks import APP_NAME


class AstrosatTasksConfig(AppConfig):
    name = APP_NAME

    def ready(self):

        try:
            # register any checks...
            import astrosat_tasks.checks  # noqa
        except ImportError:
            pass

        try:
            # register any signals...
            import astrosat_tasks.signals  # noqa
        except ImportError as e:
            print(e)
            pass

        # register any tasks...
        import astrosat_tasks.celery
