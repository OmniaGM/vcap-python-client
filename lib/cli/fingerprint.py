import hashlib, os, glob
class Fingerprint(object):
    def fingerprint(self, your_file):
        m = hashlib.md5()
        upload_file = your_file
        upload_file = open(upload_file, 'rb')
        m.update(upload_file.read())
        resource_dict = {}
        resource_dict['sha1'] = m.hexdigest()
        resource_dict['size'] = os.path.getsize(upload_file.name)
        resource_dict['fn'] = your_file
        return resource_dict
    
    def files_fingerprint(self, file_path):
        os.chdir(file_path)
        upload_files = glob.glob('*')
        resource_manifest = []
        for upload_file in upload_files:
            resource_manifest.append(self.fingerprint(upload_file))
        return resource_manifest
