import ctypes
import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from EricCorePy.UsbCmder.BaseUi import Ui_Dialog
from EricCorePy.UsbCmder.CmderCtrller import CmderCtrller
from EricCorePy.UsbCmder.CmderView import CmderView

from DataParser import DataParser
from KeyPassCtrlExt import KeyPassCtrlExt
from ExtendCmd import ExtendCmd

KEY_EVENT_PAGE_UP = 16777238
KEY_EVENT_PAGE_DOWN = 16777239


class MyDlg(QDialog):
    def __init__(self):
        super(MyDlg, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Lambda(λ) debugger Tool by EricWang")

        view = CmderView()
        self.init_view(view, self.ui)
        self.m_ctrller = CmderCtrller(view)
        self.m_ctrller.m_dataParser = DataParser()
        self.m_ctrller.m_keyPassCtrlExt = KeyPassCtrlExt()

        extCmd = ExtendCmd()
        self.m_ctrller.m_extCmdColls = extCmd.get_cmd_colls()
        self.m_ctrller.bind_cmd_set()

        self.make_event()

    def init_view(self, view, ui):
        view.m_mainMsg = ui.txtMainMsg
        view.m_secondMsg = ui.txtAscii
        view.m_cmdSel = ui.cboCmdSel
        view.m_cdb = [ui.txtCdb_00, ui.txtCdb_01, ui.txtCdb_02, ui.txtCdb_03, ui.txtCdb_04, ui.txtCdb_05,
                      ui.txtCdb_06, ui.txtCdb_07, ui.txtCdb_08, ui.txtCdb_09, ui.txtCdb_10, ui.txtCdb_11,
                      ui.txtCdb_12, ui.txtCdb_13, ui.txtCdb_14, ui.txtCdb_15]

        view.m_dataLen = ui.txtDataLen
        view.m_dataIn = ui.rdoDataIn
        view.m_dataOut = ui.rdoDataOut
        view.m_driveSel = ui.cboDriveSel
        view.m_qtMsgBox = QMessageBox()

    def make_event(self):
        self.ui.btnExecute.clicked.connect(self.execute)
        self.ui.btnRefresh.clicked.connect(self.refresh)
        self.ui.cboCmdSel.currentIndexChanged.connect(self.cmd_idx_change)

        self.ui.keyPressEvent = self.keyPressEvent

    def refresh(self):
        self.m_ctrller.refresh()

    def execute(self):
        self.m_ctrller.execute()

    def cmd_idx_change(self, idx):
        self.m_ctrller.cmd_select_change(idx)

    def keyPressEvent(self, event):
        res = self.m_ctrller.key_press_event(event)
        if res == False:
            super(MyDlg, self).keyPressEvent(event)


def main_start():
    app = QApplication(sys.argv)
    window = MyDlg()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main_start()
