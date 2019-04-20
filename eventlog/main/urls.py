# This dictionary is used to map the url to the event names
EVENT_NAME_DICT={

    # maps community view event
    r'^stock-view/(?P<pk>\d+)/$':{
        'GET':{
               'event_name' : 'event.stock.view'
        }
    },

    r'^stock-predict/(?P<pk>\d+)/$':{
        'GET':{
               'event_name' : 'event.stock.predict'
        }
    },

    r'^portfolio/blog/$':{
        'GET':{
               'event_name' : 'event.blog.view'
        }
    },

    r'^portfolio/$':{
        'GET':{
               'event_name' : 'event.portfolio.view'
        }
    },

    r'^portfolio/manually/$':{
        'GET':{
               'event_name' : 'event.portfolio.add'
        }
    },

    #maps  login event
    r'^login/$':{
        'POST':{
             'event_name' : 'event.user.login',
        }
    },

    #maps logout event
    r'^logout/$':{
        'GET':{
             'event_name' : 'event.user.logout'
        }
    },

    #maps profile view event
    r'^userprofile/(?P<username>[\w.@+-]+)/$':{
        'GET':{
              'event_name' : 'event.profile.view'
        }
    },
}
