from . import logprocess
from decouple import config

STORE = 'STORE'
TOSERVER = 'TOSERVER'

LOG_TYPE = config('LOG_TYPE')

STORE_CONF = {
            "filename": config('LOG_STORE')
} 


SERVER_CONF = {
        "protocol": config('LOG_PROTOCOL'),
        "address": config('LOG_ADDRESS'),
        "port": config('LOG_PORT'),
        "use_proxy": config('LOG_USE_PROXY', cast=bool),
    } 


SERVER_CONF["proxies"] = {}

SERVER_CONF["proxy_auth"] = {}

COMMON_FIELDS = {
    "user-agent": logprocess.process_user_agent,
    "ip-address": logprocess.process_host_ip,
    "server-host": logprocess.process_server_host,
    "referer": logprocess.process_referer,
    "accept-language": logprocess.process_accept_language,
    "session-id": logprocess.process_session_id,
    "path-info": logprocess.process_path_info,
    "time-stamp": logprocess.process_time_stamp,
    "event-source": logprocess.proces_attach_event_source,
    "user-id": logprocess.process_user_info,
}

CONTEXT_SPECIFIC_FIELDS = {    
        #stock specific events
        "event.stock.view": {
            "stock-id": logprocess.process_stock_info,
            "stock-name": logprocess.process_stock_name,
        },

        "event.stock.predict": {
            "stock-id": logprocess.process_stock_predict_info,
            "stock-name": logprocess.process_stock_name,
        },

        "event.blog.view":{},
        "event.portfolio.view":{},
        "event.portfolio.add":{},

        #login event
        "event.user.login":{
            "username": logprocess.process_username_from_request
        },

        #logout event
        "event.user.logout":{
             "user-id": logprocess.process_user_info
        },
}