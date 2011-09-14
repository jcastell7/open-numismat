from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal

from Collection import Collection

class LatestCollectionAction(QtGui.QAction):
    latestTriggered = pyqtSignal(str)
    
    def __init__(self, key, parent=None):
        super(LatestCollectionAction, self).__init__(parent)

        settings = QtCore.QSettings()
        self.fileName = settings.value(key)
        self.setText(Collection.fileNameToCollectionName(self.fileName))
        self.triggered.connect(self.trigger)
    
    def trigger(self):
        self.latestTriggered.emit(self.fileName)

class LatestCollections(QtCore.QObject):
    DefaultCollectionName = "../db/demo.db"
    SettingsKey = 'collection/latest'
    LatestCount = 5

    def __init__(self, parent=None):
        super(LatestCollections, self).__init__(parent)

        self.settings = QtCore.QSettings()
    
    def actions(self):
        actions = []
        for i in range(LatestCollections.LatestCount):
            key = self.__key(i)
            if self.settings.value(key):
                actions.append(LatestCollectionAction(key, self))
        
        return actions

    def latest(self):
        fileName = self.settings.value('collection/latest')
        if not fileName:
            fileName = LatestCollections.DefaultCollectionName
        
        return fileName
    
    def setLatest(self, fileName):
        # Get stored latest collections
        values = []
        for i in range(LatestCollections.LatestCount):
            val = self.settings.value(self.__key(i))
            if val:
                values.append(val)
        
        values.insert(0, fileName)
        # Uniqify collections name (order preserving)
        checked = []
        for e in values:
            if e not in checked:
                checked.append(e)
        values = checked

        # Store updated latest collections
        for i in range(len(values)):
            self.settings.setValue(self.__key(i), values[i])

        # Remove unused settings entries
        for i in range(len(values), LatestCollections.LatestCount):
            self.settings.remove(self.__key(i))
        
        # Store latest collection for auto opening
        self.settings.setValue(LatestCollections.SettingsKey, fileName)
    
    def __key(self, i):
        return LatestCollections.SettingsKey + str(i+1)