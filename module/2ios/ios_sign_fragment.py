# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.08.03 23:32:52
from ui.xdialog import XDialog

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from framework.resource import *
from framework.FragmentBase import FragmentBase
from ui.uikit import LayoutItem, UiKit, RadioItem
from utils.utils_cmn import CmnUtils
from utils.utils_logger import LoggerUtils

RID_CHOOSER_IN = 'chooser-in-label'
RID_CHOOSER_OUT = 'chooser-out-label'
RID_BUTTON_SIGN = 'btn-sign'
RID_CHOOSER_MAIN_PROVISION = 'text-main-provision'
RID_CHOOSER_PLUGIN_PROVISION = 'text-plugin-provision'
RID_BUNDLE_ID = 'text-bundle-id'
RID_BUNDLE_ID_1='bundle-id-1'
RID_BUNDLE_ID_2='bundle-id-2'


# --------------------------------------------------------------------------------------------------------------------
def createFragment(module):
    return IosSignFragment(module)


class IosSignFragment(FragmentBase):
    def __init__(self, module):
        FragmentBase.__init__(self, module)

    def onCreate(self, winRoot):
        FragmentBase.onCreate(self, winRoot)
        self.__initView__()
        self.__initData__()

    def __initView__(self):
        _, __, self.lbIn = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString("text-choose"),
            lambda s=self, t=RID_CHOOSER_IN: s.doAction(t),
            Resource.getString(RID_CHOOSER_IN)
        ))
        _, __, self.lbOut = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString('text-choose'),
            lambda s=self, t=RID_CHOOSER_OUT: s.doAction(t),
            Resource.getString(RID_CHOOSER_OUT)
        ))

        values = self.getCertNames()
        self.combox = UiKit.createLabelCombox(self.mWindow, values, Resource.getString('text-label-cert'))

        self.radioType = StringVar()
        rItems = [
            RadioItem(Resource.getString(RID_BUNDLE_ID_1), RID_BUNDLE_ID_1, lambda s=self, t=RID_BUNDLE_ID_1: s.doAction(t)),
            RadioItem(Resource.getString(RID_BUNDLE_ID_2), RID_BUNDLE_ID_2, lambda s=self, t=RID_BUNDLE_ID_2: s.doAction(t)),
        ]
        UiKit.createRadio(self.mWindow, self.radioType, rItems, Resource.getString(RID_BUNDLE_ID), 'h')

        _, __, self.lbMainProvision = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString("text-choose"),
            lambda s=self, t=RID_CHOOSER_MAIN_PROVISION: s.doAction(t),
            Resource.getString(RID_CHOOSER_MAIN_PROVISION)
        ))

        _, __, self.lbPluginProvision = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString("text-choose"),
            lambda s=self, t=RID_CHOOSER_PLUGIN_PROVISION: s.doAction(t),
            Resource.getString(RID_CHOOSER_PLUGIN_PROVISION)
        ))

        UiKit.createGap(self.mWindow)

        # do action
        rightButtons = [
            LayoutItem(Resource.getString(RID_BUTTON_SIGN), lambda s=self, t=RID_BUTTON_SIGN: s.doAction(t)),
        ]
        FragmentBase.createConsoleLayoutButtons(self, rightButtons)

        # results
        self.consoleCreate(self.mWindow)
        self.consoleSetText(Resource.getString('console-info'))

    def __initData__(self):
        val = self.mModule.getCache(RID_BUNDLE_ID)
        self.radioType.set(RID_BUNDLE_ID_1 if CmnUtils.isEmpty(val) else val)

    def getCertNames(self):
        cnn = []
        ret = CmnUtils.doCmd('security find-identity -v')
        for line in ret.split('\n'):
            line = line.strip()
            pos = line.find('"')
            if pos <= 0: continue
            line = line[pos+1:]
            pos = line.find('"')
            if pos <= 0: continue
            cnn.append(line[:pos])
        return cnn

    def saveCache(self):
        self.mModule.setCache(RID_BUNDLE_ID, self.radioType.get())
        self.mModule.setCertName(self.combox.getSelection())
        self.mModule.setBundleID(None if self.radioType.get() == RID_BUNDLE_ID_2 else '-keep-')

    def doAction(self, id):
        FragmentBase.doAction(self, id)
        if id == RID_BUTTON_SIGN:
            self.doAsyncActionCall(IosSignFragment.doAsyncAction, self)
        elif id == RID_CHOOSER_IN:
            ff = UiKit.showAskFile(self.mModule.getCache(id))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setInFile(ff)
            self.mModule.setCache(id, ff)
            self.lbIn['text'] = UiKit.getUiFileName(ff)
        elif id == RID_CHOOSER_OUT:
            ff = UiKit.showAskDir(self.mModule.getCache(id))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setOutpath(ff)
            self.mModule.setCache(id, ff)
            self.lbOut['text'] = UiKit.getUiFileName(ff)
        elif id == RID_CHOOSER_MAIN_PROVISION:
            ff = UiKit.showAskFile(self.mModule.getCache(id))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setMainProvision(ff)
            self.mModule.setCache(id, ff)
            self.lbMainProvision['text'] = UiKit.getUiFileName(ff)
        elif id == RID_CHOOSER_PLUGIN_PROVISION:
            PluginChooseDialog(['plugin1', 'plugin2', 'plugin3']).show()

    @staticmethod
    def doAsyncAction(argSelf):
        try:
            argSelf.saveCache()
            argSelf.mModule.doAction()
        except Exception as e:
            LoggerUtils.exception(e)


class PluginChooseDialog(XDialog):
    def __init__(self, plugins):
        XDialog.__init__(self)
        self.mEdit = None
        self.mText = None
        self.mItems = {}
        for plugin in plugins:
            self.mItems[plugin] = DialogItem(plugin)

    def getTitle(self): return Resource.getString('text-plugin-dialog-title')

    def getWindowSize(self): return 300, 200

    def onCreateDialog(self):
        XDialog.onCreateDialog(self)
        UiKit.createGap(self.mWindow)

        UiKit.createLabel(self.mWindow, Resource.getString('text-plugin-dialog-content'))
        for k, item in self.mItems.items():
            _, __, lb = UiKit.createLabelChooser(self.mWindow, LayoutItem(
                Resource.getString("text-choose"),
                lambda s=self, t=item.getProvision(): s.doAction(t),
                item.getProvision()
            ))
            item.setLabel(lb)

        UiKit.createGap(self.mWindow)
        rightButtons = [
            LayoutItem(Resource.getString(RID_TEXT_OK), lambda s=self, t=RID_TEXT_OK: s.doAction(t)),
            LayoutItem(Resource.getString(RID_TEXT_CANCEL), lambda s=self, t=RID_TEXT_CANCEL: s.doAction(t))
        ]
        UiKit.createLayoutButtons(self.mWindow, None, rightButtons)

    def doAction(self, id):
        XDialog.doAction(self, id)
        if id == RID_TEXT_OK:
            self.mText = self.mEdit.get()
            print('Got: ' + self.mText)
            self.close()
        elif id == RID_TEXT_CANCEL:
            self.close()
        else:
            ff = UiKit.showAskFile()
            if CmnUtils.isEmpty(ff): return
            self.mItems[id].setProvisionFile(ff)

    def getResults(self):
        return self.mText


class DialogItem:
    def __init__(self, plugin):
        self.mPlugin = plugin
        self.mLabel = None
        self.mFile = None

    def setLabel(self, lb):
        self.mLabel = lb

    def setProvisionFile(self, f):
        self.mFile = f
        self.mLabel['text'] = UiKit.getUiFileName(f)

    def getProvision(self):
        return self.mPlugin

    def getProvisionFile(self):
        return self.mFile
