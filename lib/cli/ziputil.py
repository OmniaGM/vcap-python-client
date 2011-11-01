import os, zipfile, glob
#import base64, StringIO
#import codecs
class Zip_Util(object):
    def pack(self, files_dir,zip_file):
        os.chdir(files_dir)
        zip_file =zipfile.ZipFile(zip_file,'w', zipfile.ZIP_DEFLATED) 
        for each_file in glob.glob('*'):
            zip_file.write(each_file)
        zip_file.close()        
        return open('%s/%s' %(files_dir, zip_file.filename), 'rb')

    def unpack(self, zip_file, dest):
        os.mkdir(dest)
        for info in zip_file.infolist():
            fname = info.filename
            data = zip_file.read(fname)
            fileout_path = '%s/%s' %(dest, fname)
            fout = open(fileout_path, 'w')
            fout.write(data)
            fout.close()