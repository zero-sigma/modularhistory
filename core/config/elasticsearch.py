from core.environment import DOCKERIZED
from decouple import config

ELASTICSEARCH_DSL = {
    'default': {'hosts': 'elasticsearch:9200' if DOCKERIZED else 'localhost:9200'},
}

# https://django-elasticsearch-dsl.readthedocs.io/en/latest/settings.html#elasticsearch-dsl-auto-refresh
ELASTICSEARCH_DSL_AUTO_REFRESH = False

# https://django-elasticsearch-dsl.readthedocs.io/en/latest/settings.html#elasticsearch-dsl-signal-processor
ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = 'core.signals.CelerySignalProcessor'

# https://django-elasticsearch-dsl.readthedocs.io/en/latest/settings.html#elasticsearch-dsl-parallel
ELASTICSEARCH_DSL_PARALLEL = config("USE_PARALLEL_INDEX_BUILDING", cast=bool, default=False)
