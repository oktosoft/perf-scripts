'''
Created on 4 Nov 2010
@version: 2.1.1a
@author: bbates
'''

import os, subprocess
from optparse import OptionParser
from ftp import DLP4D


class Main(object):  
      
    
    def __init__(self): 
        self.optDict = {}
        def callBack(option, opt, value, parser):
            self.optDict[opt] = value     
            
        parser = OptionParser()    
        parser.add_option("-v", "--version",
                  action="callback", callback=callBack, type="string", default="20102",
                  help="Set up a VERSION NUMBER server", metavar="VERSION NUMBER")
        parser.add_option("-p", "--port",
                  action="callback", callback=callBack, type="string", dest="port", 
                  help="Host:port values", metavar="HOST:PORT")
        parser.add_option("-x",
                  action="callback", callback=callBack, dest="i18n", default=False,
                  help="Start in i18n mode")
        parser.add_option("-r", "--root",
                  action="callback", callback=callBack,  type="string", dest="root", 
                  help="Set the servers root directory", metavar="ROOT DIR")
        parser.add_option("-J", "--journal",
                  action="callback", callback=callBack,  type="string", dest="journal", default="journal",
                  help="Set the servers journal file", metavar="JOURNAL FILE")
        parser.add_option("-L", "--log",
                  action="callback", callback=callBack,  type="string", dest="log", default="log",
                  help="Set the servers log file", metavar="LOG FILE")
        parser.add_option("-c", "--client",
                  action="callback", callback=callBack,  type="string", dest="client", 
                  help="Set the clients root", metavar="CLIENT ROOT")
        parser.add_option("-S", "--service",
                  action="callback", callback=callBack,  dest="service", default=False,
                  help="Start as a service")      
        parser.add_option("-u", "--user",
                  action="callback", callback=callBack,  type="string", dest="user", default="brett",
                  help="Set the user for p4config.txt", metavar="USER")
        parser.add_option("-A", "--audit",
                  action="callback", callback=callBack,  type="string", dest="audit", default="audit",
                  help="Set the audit file", metavar="AUDIT FILE")
        parser.add_option("-P", "--proxy",
                  action="callback", callback=callBack,  dest="proxy", default=False,
                  help="If true DL's the proxy NOT IMPLEMENTED", metavar="AUDIT FILE")
        parser.add_option("-V",
                  action="callback", callback=callBack,  type="string", dest="tunables",
                  help="Set tunables", metavar="KEY=VALUE,KEY=VALUE")
        parser.add_option("-3", "--server3", callback=callBack, default=False, dest="minus3",
                  action="callback", help="Sets -v server=3")
        (self.options, self.args) = parser.parse_args()
        self.addDefaults()
        
        self.run()
        
    def addDefaults(self):
        
        if '-v' in self.optDict.keys():
            pass
        else:
            self.optDict['-v'] = '20102'
        
        defaultDict = {
                            '-p' : self.optDict['-v'],
                            '-r' : ("c:\\servers\\" + self.optDict['-v']),
                            '-J' : "Journal",
                            '-L' : "Log",
                            '-u' : 'brett',
                            '-A' : 'Audit',
                            '-3' : False 
                       }
        
        
        
        for opt in defaultDict.keys():
            if opt in self.optDict:
                pass
            else:
                self.optDict[opt] = defaultDict[opt]
        
    def writeP4Config(self):
        try:
            FILE = open(("c:\\workspaces\\" + self.optDict['-v']) + '\\p4config.txt', 'w')
            FILE.write("P4PORT=" + self.optDict['-p'] + '\n')
            FILE.write("P4CLIENT=" + self.optDict['-v'] + '_ws' + '\n')
            FILE.write("P4USER=" + self.optDict['-u'] + '\n')
            FILE.close()
        except Exception:
            'Failed to write p4config.txt'
            
    def run(self):
        
        if(os.path.isdir(self.optDict['-r']) != True):
            try:
                os.mkdir(self.optDict['-r'])
            except Exception:
                pass
            
        if(os.path.isdir(("c:\\workspaces\\" + self.optDict['-v'])) != True):
            try:
                os.mkdir(("c:\\workspaces\\" + self.optDict['-v']))
                self.writeP4Config()
            except Exception:
                pass
            
        if(os.path.isfile(self.optDict['-r']+'/'+'p4d.exe') != True):
            download = DLP4D(self.optDict['-v'], self.optDict['-r'],'p4d.exe')
            download.connect()
        
        if(os.path.isfile(("c:\\workspaces\\" + self.optDict['-v'])+'/'+'p4.exe') != True):
            download = DLP4D(self.optDict['-v'], ("c:\\workspaces\\" + self.optDict['-v']), 'p4.exe')
            download.connect()
           
        try:
            self.startServer()
        except Exception as e:
            print e
        
    def stringBuild(self, dict):
        outList = [self.optDict['-r'] + '/' + 'p4d.exe']
        notAllowed = ['-u', '-3', '-P', '-v']
        for x in dict.keys():
            if x not in notAllowed:
                outList.append(x)
                outList.append(dict[x])
            elif x == '-3':
                outList.append("-v server=3")  
        return outList
     
    def startServer(self):
        string = self.stringBuild(self.optDict)
        print "BUILT STRING::: " + str(string)
        subprocess.Popen(string)
       
if __name__ == '__main__':
    run = Main()