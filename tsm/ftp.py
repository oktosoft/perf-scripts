from ftplib import FTP

class DLP4D (object):
    
    def __init__(self, version, rootDir, filename):
        self.filename = filename
        self.version = version
        self.rootDir = rootDir
        print rootDir + "<<<<ROOT DIR"
        
    def connect(self):
        try:    
            ftp = FTP('ftp.perforce.com')
            print ftp.login()
            directory = 'perforce/r' + self.version[2:4] + '.'+self.version[4:] + '/bin.ntx86'
            print 'Changing to ' + directory
            ftp.cwd(directory)
        except Exception as e:
            print e
        else:
            self.getFile(ftp)

    def getFile(self, ftp):   
        def handleDownload(block):
            file.write(block)
            print ".",     
            
        try:
            print 'Opening local file ' + self.rootDir + '/' + self.filename
            file = open(self.rootDir + '/' + self.filename, 'wb')
    
            print 'Getting ' + self.filename
            ftp.retrbinary('RETR ' + self.filename, handleDownload)
    
            print 'Closing file ' + self.filename
            file.close()
    
            print 'Closing FTP connection'
            print ftp.close()
        except Exception as e:
            print e