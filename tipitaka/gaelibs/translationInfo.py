#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json

# See setTranslationData.py
with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  translationInfo = json.loads(f.read())


def isValidTranslation(xmlFilename, translationLocale, translator):
  if translationLocale in translationInfo:
    if xmlFilename in translationInfo[translationLocale]['canon']:
      for localeXmlTranslation in translationInfo[translationLocale]['canon'][xmlFilename]:
        if translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0] == translator.decode('utf-8'):
          return True

  return False