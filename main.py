# -*- coding: utf-8 -*-
"""
Google Translate in Flowlauncher.

This plugin allows translation using Google Translate and copy it.
"""

import os
import sys

# add plugin to local PATH
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from plugin.Translator import GoogTranslate

if __name__ == "__main__":
    GoogTranslate()
