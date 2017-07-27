# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from anki_google_image_loaderUI import Ui_Form
from PyQt4 import QtCore, QtGui

import os
import sys
import time
from urllib import FancyURLopener
from urllib import quote
import urlparse

import urllib2
import simplejson

class ImageButton(QtGui.QPushButton):
    def __init__(self, parent=None, image_name=""):
        super(ImageButton, self).__init__(parent)
        self.setObjectName(image_name)
        self.image_name = image_name
        self.setFixedSize(150, 150)
        #self.setText(image_name)

        img = QtGui.QImage(image_name)
        pixmap = QtGui.QPixmap(image_name)
        pixmap = pixmap.fromImage(img.scaled(150, 150, QtCore.Qt.KeepAspectRatio,  QtCore.Qt.SmoothTransformation))
        file = QtCore.QFile(image_name)
        file.open(QtCore.QIODevice.WriteOnly)
        pixmap.save(file, "jpg", 80)
        file.close()
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(QtCore.QSize(140, 140))
        self.connect_activated()

    def connect_activated(self):
        self.clicked.connect(self.handle_int)

    def handle_int(self, index):
        app.exit()
        print "activated signal passed integer", self.image_name

class AgilForm(QtGui.QWidget):
    closed = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(AgilForm, self).__init__(parent)
        self.n_buttons = 0
        self.max_buttons = 5
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.button_layouts = self.ui.horizontalImageButtonsLayout

    def load_images(self):
        directory = QtCore.QDir()
        fileList = directory.entryList(QtCore.QStringList(["*.jpg", "*.gif", "*.png", "*.jpeg"]))
        for x in fileList:
            self.load_image(x)

    def load_image(self, url):
        self.n_buttons += 1
        if self.n_buttons >= self.max_buttons:
            horizontalImageButtonsLayout = QtGui.QHBoxLayout()
            self.ui.verticalLayout_2.addLayout(horizontalImageButtonsLayout)
            self.button_layouts = horizontalImageButtonsLayout
            self.n_buttons = 0
        #print url.toLocal8Bit()
        ib = ImageButton(None, url)
        self.button_layouts.addWidget(ib)

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
myopener = MyOpener()
myopener.addheader('Accept-Language', 'lv')
if __name__ == '__main__':

    import sys
    QtCore.QCoreApplication.addLibraryPath("C://Softimage//Softimage 2014 SP2//Application//python//Lib//site-packages//PyQt4//plugins//")
    app = QtGui.QApplication(sys.argv)
    print QtGui.QImageReader.supportedImageFormats()
    agil = AgilForm()
    agil.show()
    #agil.load_images()

    searchTerm = 'virs'
    searchTerm += ' attēli'
    searchTerm = quote(searchTerm.encode('utf8'))
    count = 0

    for i in range(0,2):
        # Notice that the start changes for each iteration in order to request a new set of images for each loop
        url = ('http://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP&as_filetype=jpg')
        print url
        request = urllib2.Request(url, None, {'Referer': 'testing'})
        response = urllib2.urlopen(request)

        # Get results using JSON
        results = simplejson.load(response)
        data = results['responseData']
        dataInfo = data['results']

        # Iterate for each result and get unescaped url
        for myUrl in dataInfo:
            count = count + 1
            print myUrl['unescapedUrl']

            path = urlparse.urlparse(myUrl['unescapedUrl']).path
            ext = os.path.splitext(path)[1]
            #print ext
            if ext == "":
                ext = '.jpg'
            myopener.retrieve(myUrl['unescapedUrl'], str(count)+ext)
            #agil.load_image(QtCore.QString(str(count)) + QtCore.QString(ext))
            print myUrl['unescapedUrl']
            agil.load_image(QtCore.QString(str(count)+ext))
        # Sleep for one second to prevent IP blocking from Google
        time.sleep(1)


    sys.exit(app.exec_())