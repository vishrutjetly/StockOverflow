from decouple import config
OUTTER_KEYS = [
        'server-host',
        'ip-address',
        'session-id',
        'path-info',
        'accept-language',
        'user-agent',
        'referer',
        'host',
        'event-source',
        'time-stamp',
        'event_name',
        '@version',
        'headers',
        '@timestamp',
        'user-id'
    ]

INNER_KEYS = [
        'stock-id',
        'username',
        'user-visited',
        'admin-username',
        'stock-name',
        'object-pk',
        ]

ES_INDEX = 'logs'

AGGREGATE_FUNCS = [
        'cardinality',
        'value_count',
        'terms'
        ]

SERVER_CONF = [config("ELASTICSEARCH_ADDRESS")]

PAGE_SIZE = config('PAGE_SIZE', cast=int)
MAX_PAGE_SIZE = config('MAX_PAGE_SIZE', cast=int)
