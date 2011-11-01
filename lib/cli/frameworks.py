class FRAMEWORK(object):
    def __init__(self):
        DEFAULT_FRAMEWORK = "http://b20nine.com/unknown"
        DEFAULT_MEM = '256M'
        FRAMEWORKS = {
                      'Rails':['rails3', 
                               { 'mem' : '256M',
                                'description': 'Rails Application'}],
                      'Spring':['spring', 
                                { 'mem': '512M',
                                 'description': 'Java SpringSource Spring Application'}],
                      'Grails':['grails', 
                                { 'mem': '512M',
                                 'description': 'Java SpringSource Grails Application'}],
                      'Lift' : ['lift', 
                                { 'mem': '512M',
                                 'description': 'Scala Lift Application'}],
                      'JavaWeb':['spring',
                                  { 'mem': '512M',
                                   'description': 'Java Web Application'}],
                      'Sinatra':['sinatra', 
                                 { 'mem': '128M',
                                  'description': 'Sinatra Application'}],
                      'Node'   : ['node',
                                  { 'mem': '64M',
                                   'description': 'Node.js Application'}],
                      'PHP'    : ['php',  
                                  { 'mem': '128M',
                                   'description': 'PHP Application'}],
                      'Erlang/OTP Rebar': ['otp_rebar',
                                           { 'mem': '64M',
                                            'description': 'Erlang/OTP Rebar Application'}],
                      'WSGI'    : ['wsgi',
                                   { 'mem': '64M',  
                                    'description': 'Python WSGI Application'}],
                      'Django'  : ['django',
                                   { 'mem': '128M', 
                                    'description': 'Python Django Application'}],
                      }
         
        def known_frameworks(self):
            return FRAMEWORKS.keys()
        
        def lookup(self, name):
            pass
        
        def detect(self, path):
            pass
        
