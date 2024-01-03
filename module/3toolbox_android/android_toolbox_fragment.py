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

RID_CHOOSER_PATH = 'chooser-path-label'

RID_ACTION_LOG = 'btn-collect-log'
RID_ACTION_SHOT = 'btn-collect-shot'
RID_ACTION_SVR = 'btn-collect-svr'
RID_ACTION_UI = 'btn-collect-ui'
RID_ACTION_PROP = 'btn-collect-prop'
RID_ACTION_APP = 'btn-collect-app'
RID_ACTION_ALL = 'btn-collect-all'
RID_ACTION_TOP_PKG = 'btn-collect-top'
RID_ACTION_PULL_PKG = 'btn-collect-pull'
RID_ACTION_SCREEN = 'btn-tool-screen'

# --------------------------------------------------------------------------------------------------------------------
def createFragment(module):
    return AndroidToolboxFragment(module)


class AndroidToolboxFragment(FragmentBase):
    def __init__(self, module):
        FragmentBase.__init__(self, module)

    def onCreate(self, winRoot):
        FragmentBase.onCreate(self, winRoot)
        self.__initView__()
        self.__initData__()

    def __initView__(self):
        _, __, self.lbPath = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString("text-choose"),
            lambda s=self, t=RID_CHOOSER_PATH: s.doAction(t),
            Resource.getString(RID_CHOOSER_PATH)
        ))

        leftButtons = [
            LayoutItem(Resource.getString(RID_ACTION_LOG), lambda s=self, t=RID_ACTION_LOG: s.doAction(t)),
            LayoutItem(Resource.getString(RID_ACTION_SHOT), lambda s=self, t=RID_ACTION_SHOT: s.doAction(t)),
            LayoutItem(Resource.getString(RID_ACTION_SVR), lambda s=self, t=RID_ACTION_SVR: s.doAction(t)),
            LayoutItem(Resource.getString(RID_ACTION_UI), lambda s=self, t=RID_ACTION_UI: s.doAction(t))
        ]
        rightButtons = [
            LayoutItem(Resource.getString(RID_ACTION_PROP), lambda s=self, t=RID_ACTION_PROP: s.doAction(t)),
            LayoutItem(Resource.getString(RID_ACTION_APP), lambda s=self, t=RID_ACTION_APP: s.doAction(t)),
            LayoutItem(Resource.getString(RID_ACTION_TOP_PKG), lambda s=self, t=RID_ACTION_TOP_PKG: s.doAction(t)),
            LayoutItem(Resource.getString(RID_ACTION_ALL), lambda s=self, t=RID_ACTION_ALL: s.doAction(t))
        ]
        UiKit.createLayoutButtonsWithFrame(self.mWindow, Resource.getString('btn-collect-title'), leftButtons, rightButtons)

        UiKit.createButtonLabel(self.mWindow,
                                LayoutItem(
                                    Resource.getString(RID_ACTION_SCREEN),
                                    lambda s=self, t=RID_ACTION_SCREEN: s.doAction(t)
                                ),
                                Resource.getString('btn-tool-screen-hint')
                                )

        self.pullPackage = StringVar()
        UiKit.createButtonEditorLabel(
            self.mWindow,
            LayoutItem(
                Resource.getString(RID_ACTION_PULL_PKG),
                lambda s=self, t=RID_ACTION_PULL_PKG: s.doAction(t)
            ),
            self.pullPackage,
            Resource.getString('btn-collect-pull-hint'),
        )

        # do gap
        UiKit.createGap(self.mWindow)

        # do action
        FragmentBase.createConsoleLayoutButtons(self, None)

        # results
        self.consoleCreate(self.mWindow)
        self.consoleSetText(Resource.getString('console-info'))

    def __initData__(self):
        pass

    def saveCache(self):
        self.mModule.setPackageName(self.pullPackage.get())

    def doAction(self, id):
        FragmentBase.doAction(self, id)
        self.collectType = id
        if id in [RID_ACTION_LOG,RID_ACTION_SHOT,RID_ACTION_SVR,RID_ACTION_UI,
                  RID_ACTION_PROP,RID_ACTION_APP,RID_ACTION_TOP_PKG,
                  RID_ACTION_PULL_PKG,RID_ACTION_ALL,RID_ACTION_SCREEN
                  ]:
            self.doAsyncActionCall(AndroidToolboxFragment.doAsyncAction, self)
        elif id == RID_CHOOSER_PATH:
            ff = UiKit.showAskDir(self.mModule.getCache(id, ''))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setPath(ff)
            self.mModule.setCache(id, ff)
            self.lbPath['text'] = UiKit.getUiFileName(ff)

    @staticmethod
    def getCmnType(typ):
        if typ == RID_ACTION_LOG: return 'log'
        if typ == RID_ACTION_SHOT: return 'shot'
        if typ == RID_ACTION_SVR: return 'svr'
        if typ == RID_ACTION_UI: return 'ui'
        if typ == RID_ACTION_PROP: return 'prop'
        if typ == RID_ACTION_APP: return 'app'
        if typ == RID_ACTION_TOP_PKG: return 'top'
        if typ == RID_ACTION_PULL_PKG: return 'pull'
        return ''

    @staticmethod
    def doAsyncAction(argSelf):
        try:
            argSelf.saveCache()
            if argSelf.collectType == RID_ACTION_SCREEN:
                argSelf.mModule.doScreen()
            else:
                argSelf.mModule.doAction(AndroidToolboxFragment.getCmnType(argSelf.collectType))
        except Exception as e:
            LoggerUtils.exception(e)
