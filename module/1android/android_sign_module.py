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
    return AndroidSignModule(path)


class AndroidSignModule(ModuleBase):
    def __init__(self, path):
        ModuleBase.__init__(self, path)
        self.mAlias = None
        self.mFile = None
        self.mKeyStoreFile = None
        self.mPath = None
        self.mPassword, self.mStorePassword = None, None
        self.mVersion = None

    def setAlias(self, v):
        self.mAlias = v

    def setPassword(self, pwd, storepwd):
        self.mPassword = pwd
        self.mStorePassword = storepwd

    def setVersion(self, v):
        self.mVersion = v

    def setFile(self, ff):
        self.mFile = ff

    def setKeyStoreFile(self, ff):
        self.mKeyStoreFile = ff

    def setPath(self, ff):
        self.mPath = ff

    def isValid(self):
        if CmnUtils.isEmpty(self.mFile):
            print('Error: Invalid apk file !')
            return False
        if CmnUtils.isEmpty(self.mKeyStoreFile):
            print('Error: Invalid key store files !')
            return False
        if CmnUtils.isEmpty(self.mPath):
            print('Error: Invalid output path !')
            return False
        if CmnUtils.isEmpty(self.mPassword) or CmnUtils.isEmpty(self.mStorePassword):
            print('Error: Invalid password !')
            return False
        return True

    #
    # def runCmd1(self, outFile):
    #     fmt = 'jarsigner -verbose -keystore "%s" -signedjar "%s" "%s" %s -storepass %s -keypass %s -sigfile CERT'
    #     cmd = fmt % (self.mKeyStoreFile, outFile, self.mFile, self.mAlias, self.mStorePassword, self.mPassword)
    #     ret = CmnUtils.doCmd(cmd)
    #     if None != ret and 0 < len(ret): print(ret)


    def doZipalign(self):
        zipalign = Resource.getBinFile('zipalign')
        if CmnUtils.isEmpty(zipalign):
            print('Error: zipalign not exist !')
            return False

        print("do zipalign verify ...")
        ret = CmnUtils.doCmd('"%s" -c -v 4 "%s"' % (CmnUtils.formatArgument(zipalign), CmnUtils.formatArgument(self.mFile)))
        print(ret)
        if CmnUtils.isEmpty(ret): return False
        if 0 < ret.find('Verification succesful'): return True

        print("do zipalign ...")
        zlApkFile = self.mFile[:-4] + "-zl.apk"
        CmnUtils.doCmd('"%s" -p -f 4 "%s" "%s"' % (CmnUtils.formatArgument(zipalign), CmnUtils.formatArgument(self.mFile), CmnUtils.formatArgument(zlApkFile)))
        self.mFile = zlApkFile
        return True


    def runCmd2(self, jarFile, outFile):
        if self.mVersion == 'V1': ver = '--v1-signing-enabled true --v2-signing-enabled false --v3-signing-enabled false --v4-signing-enabled false'
        elif self.mVersion == 'V2': ver = '--v2-signing-enabled true --v3-signing-enabled false --v4-signing-enabled false'
        elif self.mVersion == 'V3': ver = '--v3-signing-enabled true --v4-signing-enabled false'
        elif self.mVersion == 'V4': ver = '--v4-signing-enabled true'
        else: assert 0, "Invalid sign version"

        fmt = 'java -jar "%s" sign --ks "%s" --ks-key-alias %s --key-pass pass:%s --ks-pass pass:%s --out "%s" %s "%s"'
        cmd = fmt % (CmnUtils.formatArgument(jarFile),
                     CmnUtils.formatArgument(self.mKeyStoreFile),
                     self.mAlias, self.mPassword, self.mStorePassword,
                     CmnUtils.formatArgument(outFile),
                     ver,
                     CmnUtils.formatArgument(self.mFile)
                     )
        ret = CmnUtils.doCmd(cmd)
        print(ret)


    def doAction(self):
        ModuleBase.doAction(self)
        if not self.isValid(): return

        if CmnUtils.getJavaVersion() is None:
            print('Error: Java runtime environment exception !')
            return

        jarFile = Resource.getBinFile('apksigner.jar')
        if CmnUtils.isEmpty(jarFile):
            print('Error: apksigner.jar not exist !')
            return

        CmnUtils.doCmd('chmod 0777 "%s"' % CmnUtils.formatArgument(jarFile))

        print('do sign ...')
        ret = CmnUtils.doCmd('keytool -list -v -keystore "%s" -storepass %s' % (CmnUtils.formatArgument(self.mKeyStoreFile), self.mStorePassword))
        print(ret)

        outFile = self.mPath + os.sep + os.path.basename(self.mFile)[:-4] + '-signed.apk'
        outFile = FileUtils.getUniqueFile(outFile)

        if not self.doZipalign(): return
        self.runCmd2(jarFile, outFile)
        if not os.path.isfile(outFile):
            print("Fail")
            return
        ret = CmnUtils.doCmd('keytool -printcert -jarfile "%s"' % (CmnUtils.formatArgument(outFile)))
        print(ret)

        ret = CmnUtils.doCmd('java -jar "%s" verify -v "%s"' % (CmnUtils.formatArgument(jarFile), CmnUtils.formatArgument(outFile)))
        print(ret)

        print('\n>>> ' + outFile)
        print('done.')
