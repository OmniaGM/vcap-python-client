'''
Created on Sep 28, 2011

@author: arefaey
'''
import constants
import re
import simplejson
from httplib2 import Http
import base64

class VPC(object):        
# Initialize new client to the target_uri with optional auth_token
    def __init__(self, target_url=constants.DEFAULT_TARGET, auth_token=None):
        self.version = constants.VERSION
        self.target = None
        self.host = None
        self.user = None
        self.proxy = None
        self.auth_token = None
        if not target_url:
            raise Exception("Invalid target URL")
        if not (re.match('^https?', target_url)):
                target_url = "http://%s" %target_url
        re.sub('/\/+$/', '', target_url)
        self.target =  target_url
        self.auth_token = auth_token
        self.http = Http()
        
    def info(self):
        content = self.json_get(constants.INFO_PATH)
        return content


    ############################################################################################
    ##### Login #####
    
    ###########################################################################################
    
    def login(self, user, password):
        path =  '%s/%s/tokens' % (constants.USERS_PATH, user)
        _, _, content = self.request('POST', path, content_type=constants.DEFAULT_CONTENT_TYPE, params={'password':password})
        content = simplejson.loads(content)
        if 'token' in content:
            self.auth_token = content['token'] if content else None
            self.user = user
        else:
            self.auth_token = None
            self.user = None
        return self.auth_token
    
    def logged_in(self):
        return (self.user , self.auth_token)
    
    def check_login_status(self):
        if not self.auth_token:
            return False
        return True
    
    def change_password(self, new_password):
        if self.check_login_status():
            path = '%s/%s' %(constants.USERS_PATH , self.user)
            user_info = self.json_get(path)
            if user_info:
                user_info['password'] = new_password
                self.json_put(path, user_info)
                
############################################################
###request ###
###########################################################
    def perform_http_request(self, req):
        body = simplejson.dumps(req['params']) if req['params'] else ''
        response, content = self.http.request(req['url'], req['method'], body, req['headers'])
        return (response['status'], response, content)

    def request(self, method, path, content_type = None, params = None, headers = {} ):
        if self.auth_token:    headers['AUTHORIZATION'] = self.auth_token
        if self.proxy:    headers['PROXY-USER'] = self.proxy 
        if content_type:
            headers['Content-Type'] = content_type
            headers['Accept'] = content_type
            headers['X-VCAP-Trace'] = '22'
        req = {
          'method':method,
          'url': '%s%s' % (self.target, path),
          'headers' : headers,
          'params':params,
        }
        status, response, content = self.perform_http_request(req)
        return (status, response, content)
    
########################################################
###APPLICATION###
#######################################################
    def apps(self):
        if self.check_login_status():
            content =  self.json_get(constants.APPS_PATH) 
            return content
        
    def create_apps(self, name, manifest={}, instances = 1):
        if self.check_login_status():
            app = manifest.copy()
            app['name'] = name
            if not instances > 0:
                raise Exception('Number of instances must be > 0')
            else:
                app['instances'] = instances 
            return self.json_post(constants.APPS_PATH, app)
        
    def update_app(self, name, manifest):
        if self.check_login_status():
            path = '%s/%s' %(constants.APPS_PATH, name)
            return self.json_put(path, manifest)
        
    def delete_app(self,path):
        if self.check_login_status():
            status, _, _ = self.request('DELETE', path)
            return status
    
    def upload_app(self, name, zip_file, resource_manifest = []):
        if self.check_login_status():
            upload_data = {'method':'PUT'}
            upload_file = zip_file.read()
            upload_data['application'] = base64.b64encode(upload_file)
#            upload_data['application'] = upload_file
            upload_data['resources'] = simplejson.dumps(resource_manifest) 
            path = '%s/%s/application' %(constants.APPS_PATH, name)
#            upload using VMC Request method
            return self.request('POST', path, constants.DEFAULT_CONTENT_TYPE, upload_data)
#            upload using requestslib
#            import requests
#            r =  requests.post(url = '%s/%s' %(constants.DEFAULT_TARGET, path),
#                                data = {'method':'PUT', 'resources':upload_data['resources']},
#                                files =  {'application': upload_file})
#            return r.status_code, r.headers

#            upload using posterlib
#            import poster, urllib2, cookielib
#            opener = poster.streaminghttp.register_openers()
#            opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar())) # Add cookie handler
#            datagen, headers = poster.encode.multipart_encode(upload_data)
#            request = urllib2.Request('%s/%s' %(constants.DEFAULT_TARGET, path), datagen, headers)
#            result = urllib2.urlopen(request) 
#            return result 

#            upload using MultipartPostHandler lib
#            import MultipartPostHandler, urllib2
#            opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
#            urllib2.install_opener(opener)
#            request = urllib2.Request('%s%s' %(constants.DEFAULT_TARGET, path), upload_data)
#            response = urllib2.urlopen(request)
#            return response 

        
    def app_info(self, name):
        if self.check_login_status():
            return self.json_get('%s/%s' %(constants.APPS_PATH, name))
    
    def app_update_info(self, name):
        if self.check_login_status():
            return self.json_get('%s/%s/update' %(constants.APPS_PATH, name))
                
    def app_instances(self, name):
        if self.check_login_status():
            return self.json_get('%s/%s/instances' %(constants.APPS_PATH, name))
    
    def app_crashes(self, name):
        if self.check_login_status():
            return self.json_get('%s/%s/crashes' %(constants.APPS_PATH, name))
    
    def app_files(self, name, path, instance = 0):
        if self.check_login_status():
            url='/%s/%s/instances/%s/files/%s'%(constants.APPS_PATH,name,instance,path)
            url = url.replace('//','/')
            _, _, content = self.request('GET', url, constants.DEFAULT_CONTENT_TYPE)
            return content 
                        
######################################################
###Services###
#####################################################
    def services_info(self):
        if self.check_login_status():
            return self.json_get(constants.GLOBAL_SERVICES_PATH)
    
######################################################
###Admin###
#####################################################
    def users(self):
        if self.check_login_status():
            return self.json_get(constants.USERS_PATH)

######################################################
###JSON HELPER###
#####################################################
    def json_get(self, url):
        _, _, content = self.request('GET', url, constants.DEFAULT_CONTENT_TYPE)
        return simplejson.loads(content)

    def json_post(self, url, params):
        return self.request('POST', url, constants.DEFAULT_CONTENT_TYPE, params)
        
    def json_put(self, url, params):
        status, response, content = self.request('PUT', url, constants.DEFAULT_CONTENT_TYPE, params)
        return (status, response, content)