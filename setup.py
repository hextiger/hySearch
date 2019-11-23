#! /usr/bin/env python
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

base = "Win32GUI"
# base = 'Console'
# base = 'ConsoleKeepPath'
# base = 'Win32GUI'
# base = 'Win32Service'
build_exe_options = {"packages": [], "excludes": ["tkinter"],"include_files": ["data.zip"]}

setup(
    name="hySearch",
    version="3.0",
    description="hySearch",
    options={"build_exe": build_exe_options},
    executables=[Executable("hySearch.pyw", base=base)],
)


# python setup.py build
