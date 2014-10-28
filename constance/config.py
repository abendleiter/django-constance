from constance import settings, utils
import json


class Config(object):
    """
    The global config wrapper that handles the backend.
    """
    def __init__(self):
        super(Config, self).__setattr__('_backend',
            utils.import_module_attr(settings.BACKEND)())

    def __getattr__(self, key):
        try:
            default, help_text = settings.CONFIG[key]
        except KeyError:
            raise AttributeError(key)
        result = self._backend.get(key)
        if result is None:
            result = default
            setattr(self, key, default)
            return result
        # Try to convert to JSON, if it succeeds return the JSON object,
        # otherwise just return the normal value
        try:
            json_string = json.loads(result)
            result = json_string
        except Exception:
            pass
        return result

    def __setattr__(self, key, value):
        if key not in settings.CONFIG:
            raise AttributeError(key)
        self._backend.set(key, value)

    def __dir__(self):
        return settings.CONFIG.keys()
