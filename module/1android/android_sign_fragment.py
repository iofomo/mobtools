# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.08.03 23:32:52

import os
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from framework.resource import Resource
from framework.FragmentBase import FragmentBase
from ui.uikit import LayoutItem, UiKit, RadioItem
from utils.utils_cmn import CmnUtils
from utils.utils_logger import LoggerUtils

RID_CHOOSER_FILE = 'chooser-file-label'
RID_CHOOSER_KEYSTORE = 'chooser-keystore-label'
RID_CHOOSER_PATH = 'chooser-path-label'

RID_ACTION = 'btn-sign'

RID_EDIT_ALIAS = 'edit-alias'
RID_EDIT_ALIAS_HINT = 'edit-alias-hint'
RID_EDIT_PASSWORD = 'edit-password'
RID_EDIT_PASSWORD_HINT = 'edit-password-hint'
RID_EDIT_STORE_PASSWORD = 'edit-store-password'
RID_EDIT_STORE_PASSWORD_HINT = 'edit-store-password-hint'

RID_CHECKBOX_TITLE = 'text-sign-version'
# RID_CHECKBOX_TYPE_V1 = 'V1'
RID_CHECKBOX_TYPE_V2 = 'V2'
RID_CHECKBOX_TYPE_V3 = 'V3'
RID_CHECKBOX_TYPE_V4 = 'V4'

# --------------------------------------------------------------------------------------------------------------------
def createFragment(module):
    return AndroidSignFragment(module)


class AndroidSignFragment(FragmentBase):
    def __init__(self, module):
        FragmentBase.__init__(self, module)

    def onCreate(self, winRoot):
        FragmentBase.onCreate(self, winRoot)
        self.__initView__()
        self.__initData__()

    def __initView__(self):
        _, __, self.lbFile = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString("text-choose"),
            lambda s=self, t=RID_CHOOSER_FILE: s.doAction(t),
            Resource.getString(RID_CHOOSER_FILE)
        ))

        _, __, self.lbPath = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString("text-choose"),
            lambda s=self, t=RID_CHOOSER_PATH: s.doAction(t),
            Resource.getString(RID_CHOOSER_PATH)
        ))

        _, __, self.lbKeystore = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString("text-choose"),
            lambda s=self, t=RID_CHOOSER_KEYSTORE: s.doAction(t),
            Resource.getString(RID_CHOOSER_KEYSTORE)
        ))

        self.editAlias = StringVar()
        UiKit.createLabelEditor(self.mWindow, Resource.getString(RID_EDIT_ALIAS), self.editAlias, Resource.getString(RID_EDIT_ALIAS_HINT))

        self.editPwd = StringVar()
        UiKit.createLabelEditorPassword(self.mWindow, Resource.getString(RID_EDIT_PASSWORD), self.editPwd, Resource.getString(RID_EDIT_PASSWORD_HINT))

        self.editStorePwd = StringVar()
        UiKit.createLabelEditorPassword(self.mWindow, Resource.getString(RID_EDIT_STORE_PASSWORD), self.editStorePwd, Resource.getString(RID_EDIT_STORE_PASSWORD_HINT))

        self.radioType = StringVar()
        rItems = [
            # RadioItem(RID_CHECKBOX_TYPE_V1, RID_CHECKBOX_TYPE_V1, lambda s=self, t=RID_CHECKBOX_TYPE_V1: s.doAction(t)),
            RadioItem(RID_CHECKBOX_TYPE_V2, RID_CHECKBOX_TYPE_V2, lambda s=self, t=RID_CHECKBOX_TYPE_V2: s.doAction(t)),
            RadioItem(RID_CHECKBOX_TYPE_V3, RID_CHECKBOX_TYPE_V3, lambda s=self, t=RID_CHECKBOX_TYPE_V3: s.doAction(t)),
            RadioItem(RID_CHECKBOX_TYPE_V4, RID_CHECKBOX_TYPE_V4, lambda s=self, t=RID_CHECKBOX_TYPE_V4: s.doAction(t)),
        ]
        UiKit.createRadio(self.mWindow, self.radioType, rItems, Resource.getString(RID_CHECKBOX_TITLE), 'h')

        # do gap
        UiKit.createGap(self.mWindow)

        # do action
        rightButtons = [
            LayoutItem(Resource.getString(RID_ACTION), lambda s=self, t=RID_ACTION: s.doAction(t))
        ]
        FragmentBase.createConsoleLayoutButtons(self, rightButtons)

        # results
        self.consoleCreate(self.mWindow)
        self.consoleSetText(Resource.getString('console-info'))

    def __initData__(self):
        val = self.mModule.getCache(RID_EDIT_ALIAS, '')
        if not CmnUtils.isEmpty(val): self.editAlias.set(val)
        val = self.mModule.getCache(RID_CHECKBOX_TITLE, '')
        self.radioType.set(RID_CHECKBOX_TYPE_V2 if CmnUtils.isEmpty(val) else val)

    def saveCache(self):
        self.mModule.setAlias(self.editAlias.get())
        self.mModule.setCache(RID_EDIT_ALIAS, self.editAlias.get())
        self.mModule.setPassword(self.editPwd.get(), self.editStorePwd.get())
        self.mModule.setVersion(self.radioType.get())
        self.mModule.setCache(RID_CHECKBOX_TITLE, self.radioType.get())

    def doAction(self, id):
        FragmentBase.doAction(self, id)
        if id == RID_ACTION:
            self.doAsyncActionCall(AndroidSignFragment.doAsyncAction, self)
        elif id == RID_CHOOSER_FILE:
            ff = UiKit.showAskFile(self.mModule.getCache(id, ''))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setFile(ff)
            self.mModule.setCache(id, ff)
            self.lbFile['text'] = UiKit.getUiFileName(ff)
        elif id == RID_CHOOSER_KEYSTORE:
            ff = UiKit.showAskFile(self.mModule.getCache(id, ''))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setKeyStoreFile(ff)
            self.mModule.setCache(id, ff)
            self.lbKeystore['text'] = UiKit.getUiFileName(ff)
        elif id == RID_CHOOSER_PATH:
            ff = UiKit.showAskDir(self.mModule.getCache(id, ''))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setPath(ff)
            self.mModule.setCache(id, ff)
            self.lbPath['text'] = UiKit.getUiFileName(ff)

    @staticmethod
    def doAsyncAction(argSelf):
        try:
            argSelf.saveCache()
            argSelf.mModule.doAction()
        except Exception as e:
            LoggerUtils.exception(e)
