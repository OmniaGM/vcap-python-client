'''
Created on Sep 28, 2011

@author: arefaey
'''
import unittest
from vpc.client import VPC
from vpc import constants
from uuid import uuid4
from lib.cli.ziputil import Zip_Util
from  lib.cli.fingerprint import Fingerprint

class TestClient(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test_initialize(self):
        client = VPC()
        self.assertEqual(constants.DEFAULT_TARGET, client.target)
        
    def test_info(self):
        client = VPC()
        info = client.info()
        self.assertEqual(info['name'], 'vcap')
        self.assertEqual(info['support'], 'http://support.cloudfoundry.com')
############################################
###Test Request###
###########################################        
    def test_perform_http_request(self):
        req = {'url':'http://www.google.com',
               'method':'get',
               'params':'',
               'headers':{}
               }
        client = VPC()
        status, _, _ = client.perform_http_request(req)
        self.assertEqual('302', status)
        
        req = {'url':'http://www.google.com',
               'method':'post',
               'params':{'x':'y'},
               'headers':{}
               }
        status, _, _ = client.perform_http_request(req)
        self.assertEqual('405', status)
        
    def test_request(self):
        client = VPC()
        status, _, _ = client.request('get', constants.INFO_PATH, constants.DEFAULT_CONTENT_TYPE)
        self.assertEqual('200', status)
############################################
###Test Login###
###########################################
    def test_login(self):       
        client = VPC()
        self.assertEqual(None, client.auth_token)
        token = client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        self.assertNotEqual(None, token)
        token = client.login('c9.cf.poc@gmail.com', 'cloud9er')
        self.assertEqual(None, token)
        
    def test_logged_in(self):
        client = VPC()
        user,token = client.logged_in()
        self.assertEqual(client.user, user )
        self.assertEqual(client.auth_token, token )
    
    def test_check_login_status(self):
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        self.assertEquanl(True, client.check_login_status())
        
    def test_change_password(self):
        client = VPC()
        client.login('omnia.gamal1988@gmail.com', 'cloud9ers')
        client.change_password('cloud9er')
        client.login('omnia.gamal1988@gmail.com', 'cloud9er')
        client.change_password('cloud9ers')
        client.login('omnia.gamal1988@gmail.com', 'cloud9ers')
#############################################
###Test Application###
############################################
    def test_app(self):
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        apps_info = client.apps()
        self.assertEqual(0, len(apps_info))
        name = 'test_%s' % uuid4()
        manifest = {
                    'name' : name,
                    'uris' : ['%s.cloudfoundry.com' % name],
                    'instances' : 1,
                    'runningInstances': 1,
                    'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
                    'resources' : { 'memory': 64 }
                    }
        #create app with instance = 1
        client.create_apps(name,manifest)
        apps_info = client.apps()
        self.assertEqual(1, len(apps_info))
        self.assertEqual(name, apps_info[-1]['name'])
        path =  '%s/%s' %(constants.APPS_PATH, apps_info[-1]['name'])
        client.delete_app(path)           
        apps_info = client.apps()
        self.assertEqual(0, len(apps_info))
        
    def test_create_app(self):
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        apps_info = client.apps()
        self.assertEqual(1, len(apps_info))
        name = 'test_%s' % uuid4()
        manifest = {"uris":['%s.cloudfoundry.com' % name],
                    "resources":{"memory":128},
                    "staging":{"framework":"sinatra"},
                    "instances":1,
                    "name":name}
        #create app with instance = 1
        status,_,_ = client.create_apps(name,manifest)
        apps_info = client.apps()
        self.assertEqual(2, len(apps_info))
        self.assertEqual(name, apps_info[0]['name'])
        self.assertEqual('302', status)        
        path =  '%s/%s' %(constants.APPS_PATH, apps_info[0]['name'])
        client.delete_app(path)           
        apps_info = client.apps()
        self.assertEqual(1, len(apps_info))
        
    def test_create_app_with_instances(self):
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        apps_info = client.apps()
        self.assertEqual(1, len(apps_info))
        name = 'test_%s' % uuid4()
        manifest = {
                    'name' : name,
                    'uris' : ['%s.cloudfoundry.com' % name],
                    'instances' : 3,
                    'runningInstances': 3,
                    'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
                    'resources' : { 'memory': 64 }
                    }
        #create app with instance = 3 
        status,_,_ = client.create_apps(name,manifest,3)
        self.assertEqual('302', status)
        apps_info = client.apps()
        self.assertEqual(2, len(apps_info))
        self.assertEqual(name, apps_info[-1]['name'])
        self.assertEqual(3, apps_info[-1]['instances'])
        path =  '/%s/%s' %(constants.APPS_PATH, apps_info[-1]['name'])
        client.delete_app(path)           
        apps_info = client.apps()
        self.assertEqual(1, len(apps_info))
        
    def test_delete_app(self):
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        apps_info = client.apps()
        self.assertEqual(0, len(apps_info))
        name = 'test_%s' % uuid4()
        manifest = {
                    'name' : name,
                    'uris' : ['%s.cloudfoundry.com' % name],
                    'instances' : 1,
                    'runningInstances': 1,
                    'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
                    'resources' : { 'memory': 64 }
                    }
        status, _, _ = client.create_apps(name, manifest)
        self.assertEqual('302', status)
        apps_info = client.apps()
        self.assertEqual(1, len(apps_info))
        self.assertEqual(name, apps_info[-1]['name'])
        path =  '%s/%s' %(constants.APPS_PATH, name)
        status = client.delete_app(path)
        self.assertEqual('200', status)
        apps_info = client.apps()
        self.assertEqual(0, len(apps_info))
        
    def test_update_app(self):
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        #self.assertEqual(1, len(client.apps()))
        #name = 'test_%s' % uuid4()
        #manifest = {
        #            'name' : name,
        #            'uris' : ['%s.cloudfoundry.com' % name],
        #            'instances' : 1,
        #            'runningInstances': 1,
        #            'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
        #            'resources' : { 'memory': 64 }
        #            }
        #status, _, _ = client.create_apps(name, manifest)
        #self.assertEqual('302', status)
        #self.assertEqual(2, len(client.apps()))
        name = 'ruby-foo-c9'
        manifest = {"env":[],
                    "uris":["ruby-foo-c9.cloudfoundry.com"],
                    "runningInstances":1,
                    "instances":3,
                    "name":"ruby-foo-c9"}
        status, _, _ = client.update_app(name, manifest)
        self.assertEqual('200', status)
        apps_info = client.apps() 
        self.assertEqual(3, apps_info[-1]['instances'])
        #path =  '%s/%s' %(constants.APPS_PATH, apps_info[-1]['name'])
        #client.delete_app(path)           
        #apps_info = client.apps()
        #self.assertEqual(1, len(apps_info))
        #upload not correct now 
    def test_upload_app(self):       
        import ipdb;ipdb.set_trace()
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        file_path = '/home/omnia/Desktop/ruby_foo'
        #get resources manifest
        fb = Fingerprint()
        resource_manifest = fb.files_fingerprint(file_path)
        #create zipfile
        zp = Zip_Util()
        zip_file = zp.pack(file_path,'app.zip')
#        zip_file = open('/home/omnia/Desktop/foo.zip','rb')
        #create app
        name = 'test_%s' % uuid4()
        manifest = {"uris":['%s.cloudfoundry.com' % name],
                    "resources":{"memory":128},
                    "staging":{"framework":"sinatra"},
                    "instances":1,
                    "name":name}
        client.create_apps(name,manifest)
        #upload files to app                
        status, _, _ = client.upload_app(name, zip_file,resource_manifest)
        self.assertEqual('200', status)        
        #delete zip_file
        import os
        os.remove(zip_file.name)
        #delete app
        path =  '/%s/%s' %(constants.APPS_PATH, name)
        client.delete_app(path)           
        apps_info = client.apps()
        self.assertNotEqual(name, apps_info[-1]['name'])
    
    def test_app_info(self):
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        name = 'test_%s' % uuid4()
        manifest = {
                    'name' : name,
                    'uris' : ['%s.cloudfoundry.com' % name],
                    'runningInstances': 1,
                    'instances' : 1,
                    'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
                    'resources' : { 'memory': 64 }
                    }
        status, _, _ = client.create_apps(name, manifest)
        apps_info = client.apps()
        self.assertEqual(1, len(apps_info))
        self.assertEqual('302', status)
        app_info = client.app_info(name)
        self.assertEqual(name, app_info['name'])
        self.assertEqual(1, app_info['instances'])
        self.assertEqual(1, len(apps_info))
        path =  '%s/%s' %(constants.APPS_PATH, apps_info[-1]['name'])
        client.delete_app(path)           
        apps_info = client.apps()
        self.assertEqual(0, len(apps_info))
        
    def test_update_info(self):
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        #name = 'test_%s' % uuid4()
        #manifest = {
        #            'name' : name,
        #            'uris' : ['%s.cloudfoundry.com' % name],
        #            'instances' : 1,
        #            'state': 'STARTED',
        #            'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
        #            'resources' : { 'memory': 128 }
        #            }
        #status, _, _ = client.create_apps(name, manifest)
        #apps_info = client.apps()
        #self.assertEqual(2, len(apps_info))
        #self.assertEqual('302', status)
        name = 'ruby-foo-c9'
        manifest = {
                    'name' : name,
                    'uris' : ['%s.cloudfoundry.com' % name],
                    'instances' : 3,
                    'runningInstances': 1,
                    'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
                    'resources' : { 'memory': 128 }
                    }
        status, _, _ = client.update_app(name, manifest)
        self.assertEqual('200', status)
        update_info = client.app_update_info(name)
        self.assertEqual('UPDATING', update_info['state'])
        #path =  '%s/%s' %(constants.APPS_PATH, apps_info[-1]['name'])
        #client.delete_app(path)           
        #apps_info = client.apps()
        #self.assertEqual(1, len(apps_info))
        manifest = {
                    'name' : name,
                    'uris' : ['%s.cloudfoundry.com' % name],
                    'instances' : 1,
                    'runningInstances': 1,
                    'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
                    'resources' : { 'memory': 128 }
                    }
        status, _, _ = client.update_app(name, manifest)
        self.assertEqual('200', status)
        update_info = client.app_update_info(name)
        self.assertEqual('SUCCEEDED', update_info['state'])     
   
    def test_app_instances(self):
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        #name = 'test_%s' % uuid4()
        #manifest = {
        #            'name' : name,
        #            'uris' : ['%s.cloudfoundry.com' % name],
        #            'instances' : 1,
        #            'runningInstances': 1,
        #            'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
        #            'resources' : { 'memory': 64 }
        #            }
        #status, _, _ = client.create_apps(name, manifest)
        #self.assertEqual('302', status)
        name = 'ruby-foo-c9'
        app_inst = client.app_instances(name)
        self.assertEqual(1, len(app_inst))
        self.assertEqual('RUNNING', app_inst['instances'][0]['state'])
        self.assertEqual(0, app_inst['instances'][0]['index'])
        #apps_info = client.apps()
        #self.assertEqual(1, len(apps_info))
        #path =  '%s/%s' %(constants.APPS_PATH, apps_info[-1]['name'])
        #client.delete_app(path)           
        #apps_info = client.apps()
        #self.assertEqual(0, len(apps_info))
        

    def test_app_crashes(self):
        import ipdb;ipdb.set_trace()
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        #name = 'test_%s' % uuid4()
        #manifest = {
        #            'name' : name,
        #            'uris' : ['%s.cloudfoundry.com' % name],
        #            'instances' : 1,
        #            'runningInstances': 1,
        #            'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
        #            'resources' : { 'memory': 64 }
        #            }
        #status, _, _ = client.create_apps(name, manifest)
        #self.assertEqual('302', status)
        name = 'ruby-foo-c9'
        crashes_info = client.app_crashes(name)
        self.assertEqual(0, len(crashes_info['crashes']))
        #apps_info = client.apps()
        #self.assertEqual(1, len(apps_info))
        #path =  '%s/%s' %(constants.APPS_PATH, apps_info[-1]['name'])
        #client.delete_app(path)           
        #apps_info = client.apps()
        #self.assertEqual(0, len(apps_info))
    
    def test_app_files(self):
        import re
        client = VPC()
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        #name = 'test_%s' % uuid4()
        #manifest = {
        #            'name' : name,
        #            'uris' : ['%s.cloudfoundry.com' % name],
        #            'instances' : 1,
        #            'runningInstances': 1,
        #            'staging' : { 'model' : 'sinatra', 'stack': 'ruby18' },
        #            'resources' : { 'memory': 64 }
        #            }
        #status, _, _ = client.create_apps(name, manifest)
        #self.assertEqual('302', status)
        name = 'ruby-foo-c9'
        files = client.app_files(name,'app')
        self.assertEqual('foo', re.search(r'foo',files).group())
        #apps_info = client.apps()
        #self.assertEqual(1, len(apps_info))
        #path =  '%s/%s' %(constants.APPS_PATH, apps_info[-1]['name'])
        #client.delete_app(path)           
        #apps_info = client.apps()
        #self.assertEqual(0, len(apps_info))
       
######################################################
###Test Services###
#####################################################
    def test_services(self):
        import ipdb;ipdb.set_trace()
        client = VPC() 
        client.login('c9.cf.poc@gmail.com', 'cloud9ers')
        services = client.services_info()
        self.assertEqual(True, services.has_key('generic'))
        
######################################################
###Test admin###
#####################################################

    def test_users(self):
        #just for admin
        pass
######################################################
###Test Json###
#####################################################
    def test_json_get(self):
        client = VPC() 
        value = client.json_get(constants.INFO_PATH)
        type_obj = type(value)
        self.assertEqual( 'dict', type_obj)
        self.assertEqual("vcap", value["name"])
        
    def test_json_post(self):
        client = VPC('http://www.')
        status, _, _ = client.json_post('posttestserver.com/post.php', {"id_usr" : 1})
        #note i use 200 because this http://posttestserver.com/ back 200 this not Rest
        #Rest post back => 201
        self.assertEqual('200', status)
            
    def test_json_put(self):
        client = VPC('http://www.')
        status, _, _ = client.json_put('posttestserver.com/post.php', {"id_usr" : 1})
        #note i use 200 because this http://posttestserver.com/ back 200 this not Rest
        #Rest put back => 201
        #this http://posttestserver.com not allow put
        #so status will return 405
        self.assertEqual('200', status)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()