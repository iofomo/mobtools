#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Brief:  mk
# @Date: 2023.09.16 11:40:37

import sys, os

g_env_path = os.getcwd()
g_this_file = os.path.realpath(sys.argv[0])
g_this_path = os.path.dirname(g_this_file)
# --------------------------------------------------------------------------------------------------------------------------
# init project env
g_wing_path = os.path.expanduser("~") + os.sep + '.wing/wing' #  such as: /Users/${username}/.wing/wing
sys.path.append(g_wing_path)
from utils.utils_import import ImportUtils
g_space_path = ImportUtils.initSpaceEnv(g_env_path)

from utils.utils_cmn import CmnUtils
from utils.utils_zip import ZipUtils
from utils.utils_file import FileUtils
from utils.utils_logger import LoggerUtils
from basic.arguments import BasicArgumentsValue
# --------------------------------------------------------------------------------------------------------------------------


def run():
    zarg = BasicArgumentsValue()
    if 1 <= zarg.count():
        OUT_PATH = zarg.get(0)
    else: # build from local
        OUT_PATH = os.path.dirname(g_this_path) + '/out'

    try:
        ret = CmnUtils.doCmdCall('cd %s && python build.py %s all' % (g_this_path, OUT_PATH))
        assert ret, 'Error: gradlew clean'
    except Exception as e:
        LoggerUtils.println(e)
        raise SyntaxError(e)

if __name__ == "__main__":
    run()
