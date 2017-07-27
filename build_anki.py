__author__ = 'Pavel'

from PyQt4 import QtCore, QtGui
import os
directory = QtCore.QDir("D:\\LocalProjects\\anki\\anki-master\\designer")
fileList = directory.entryList(QtCore.QStringList("*.ui"))
for x in fileList:
    print "import "+x.toLocal8Bit()
    process = QtCore.QProcess()
    file = QtCore.QString(os.getcwd()) + QtCore.QDir.separator() + "uic" + QtCore.QDir.separator() + "pyuic.py"
    process.execute("python " + file + " " + directory.path() + QtCore.QDir.separator() + x + " -o " + directory.path() + QtCore.QDir.separator()+"forms"  + QtCore.QDir.separator()+  QtCore.QString(os.path.splitext(str(x))[0])+".py" )
    #+ directory.path() + QtCore.QDir.separator() +  QtCore.QString(os.path.splitext(str(x))[0])