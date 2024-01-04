# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.08.03 23:32:52

import os

from framework.resource import Resource
from framework.ModuleBase import ModuleBase
from utils.utils_cmn import CmnUtils
from utils.utils_file import FileUtils


# --------------------------------------------------------------------------------------------------------------------
def createModule(path):
    return IosSignModule(path)


class IosSignModule(ModuleBase):
    def __init__(self, path):
        ModuleBase.__init__(self, path)
        self.mCertName = None
        self.mInFile = None
        self.mInMainProvision = None
        self.mOutpath = None
        self.mID = None

    def setCertName(self, v):
        self.mCertName = v

    def setBundleID(self, flag):
        self.mID = flag

    def setOutpath(self, v):
        self.mOutpath = v

    def setInFile(self, ff):
        self.mInFile = ff

    def setMainProvision(self, ff):
        self.mInMainProvision = ff

    def isValid(self):
        if CmnUtils.isEmpty(self.mInFile):
            print('Error: invalid ipa file !')
            return False
        if CmnUtils.isEmpty(self.mOutpath):
            print('Error: invalid output path !')
            return False
        if CmnUtils.isEmpty(self.mInMainProvision):
            print('Error: invalid main provision file !')
            return False
        if CmnUtils.isEmpty(self.mCertName):
            print('Error: invalid Certificate Name !')
            return False
        return True

    def doAction(self):
        ModuleBase.doAction(self)
        if not self.isValid(): return
        if not CmnUtils.isOsMac():
            print('Only supports MacOS.')
            return
        print('do sign ...')
        bin = Resource.getBinFile('resign')
        if CmnUtils.isEmpty(bin):
            print('Error: invalid resign bin file !')
            return False
        tempFile = self.mOutpath + os.sep + '_signerTemp.ipa'
        FileUtils.remove(tempFile)

        cmd = bin + \
            ' "' + self.mInFile + '"' + \
            ' "' + self.mCertName + '"' + \
            ' -p' + \
            ' "' + self.mInMainProvision + '"' + \
            ('' if CmnUtils.isEmpty(self.mID) else ' -b ' + self.mID) + \
            ' "' + self.mOutpath + '"'
        print(cmd)
        CmnUtils.doCmdCall(cmd)

        if not os.path.isfile(tempFile):
            print('Error: sign fail !')
            return False
        outFile = self.mOutpath + os.sep + os.path.basename(self.mInFile)[:-4] + '-signed.ipa'
        outFile = FileUtils.getUniqueFile(outFile)
        os.rename(tempFile, outFile)
        print('>>> ' + outFile)
