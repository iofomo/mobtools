# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.08.03 23:32:52

import os

from framework.ModuleBase import ModuleBase
from utils.utils_cmn import CmnUtils
from utils.utils_file import FileUtils
from utils.utils_logger import LoggerUtils
from utils.utils_adb import AdbUtils
from utils.utils_adb_dumper import ADBDumper
from tool_screen import ToolScreen

# --------------------------------------------------------------------------------------------------------------------
def createModule(path):
    return AndroidToolboxModule(path)


class AndroidToolboxModule(ModuleBase):
    def __init__(self, path):
        ModuleBase.__init__(self, path)
        self.mPath = None

    def setPath(self, ff):
        self.mPath = ff

    def setPackageName(self, pkg):
        self.mPackageName = pkg

    def isValid(self):
        if CmnUtils.isEmpty(self.mPath):
            print('Error: Invalid output path !')
            return False
        return True

    def doTopInfo(self):
        AdbUtils.printlnDump()

    def doPullPackage(self, pkg):
        if CmnUtils.isEmpty(pkg):
            LoggerUtils.println('Error: Invalid commands')
            LoggerUtils.println('The command is: "wing -adb pull {package name}"')
            return

        pkgFile = AdbUtils.getApkFile(pkg)
        if CmnUtils.isEmpty(pkgFile):
            LoggerUtils.println('Error: ' + pkg + ' not found')
            return
        outFile = self.mPath + os.sep + pkg + '.apk'
        if not AdbUtils.pull(pkgFile, outFile):
            LoggerUtils.println('Error: pull ' + pkgFile + ' Failed')
            return
        LoggerUtils.println('>>> ' + outFile)

    def doAction(self, typ):
        ModuleBase.doAction(self)
        if not self.isValid(): return

        if typ == 'top':
            LoggerUtils.println('parse top app ...')
            AdbUtils.printlnDump()
        elif typ == 'pull':
            if CmnUtils.isEmpty(self.mPackageName):
                LoggerUtils.println('Invalid package name')
                return
            LoggerUtils.println('pull app ...')
            self.doPullPackage(self.mPackageName)
        else:
            ADBDumper(self.mPath).collect(typ)
        print('\ndone.\n\n')

    def doScreen(self):
        LoggerUtils.println('Get device screen ...')
        ToolScreen.doScreen()
