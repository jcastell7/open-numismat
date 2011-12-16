from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

class _InvalidDatabaseError(Exception):
    pass

class _DatabaseServerError(Exception):
    pass

class _Import(QtCore.QObject):
    def __init__(self, parent=None):
        super(_Import, self).__init__(parent)

        self.progressDlg = QtGui.QProgressDialog(self.parent(), Qt.WindowSystemMenuHint)
        self.progressDlg.setWindowModality(Qt.WindowModal)
        self.progressDlg.setMinimumDuration(250)
        self.progressDlg.setCancelButtonText(self.tr("Cancel"))
        self.progressDlg.setWindowTitle(self.tr("Importing"))
    
    def importData(self, src, model):
        try:
            connection = self._connect(src)
            if self._check(connection):
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
                rows = self._getRows(connection)
                QtGui.QApplication.restoreOverrideCursor();
                
                self.progressDlg.setMaximum(len(rows))
                self.progressDlg.setWindowTitle(self.tr("Importing from %s") % src)
                
                for progress, row in enumerate(rows):
                    self.progressDlg.setValue(progress)
                    if self.progressDlg.wasCanceled():
                        break
                    
                    record = model.record()
                    self._setRecord(record, row)
                    model.appendRecord(record)
                
                self.progressDlg.setValue(len(rows))
            else:
                self.__invalidDbMessage(src)
            
            self._close(connection)
        
        except _InvalidDatabaseError as error:
            self.__invalidDbMessage(src, error.__str__())
        except _DatabaseServerError as error:
            self.__serverErrorMessage(error.__str__())
    
    def _connect(self, src):
        raise NotImplementedError
    
    def _check(self, connection):
        return True
    
    def _getRows(self, connection):
        pass
    
    def _setRecord(self, record, row):
        pass
    
    def _close(self, connection):
        pass
    
    def __errorMessage(self, message, text):
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, self.tr("Importing"),
                                   message,
                                   parent=self.parent())
        if text:
            msgBox.setDetailedText(text)
        msgBox.exec_()
    
    def __invalidDbMessage(self, src, text=''):
        self.__errorMessage(self.tr("'%s' is not a valid database") % src, text)
    
    def __serverErrorMessage(self, text=''):
        self.__errorMessage(self.tr("DB server connection problem. Check additional software."), text)

from Collection.Import.Numizmat import ImportNumizmat
from Collection.Import.Cabinet import ImportCabinet
from Collection.Import.CoinsCollector import ImportCoinsCollector

__all__ = ["ImportNumizmat", "ImportCabinet", "ImportCoinsCollector"]