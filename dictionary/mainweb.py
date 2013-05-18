#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
from localeUtil import getLocale
from localeUtil import parseAcceptLanguage
from misc import isCompiledJS
from misc import isTrack
import i18n
import web

sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from url import isValidPrefixAndWord
from url import getPrefixHtml
from url import getWordHtml
from url import getHtmlTitle

import jinja2
import json

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
      [os.path.join(os.path.dirname(__file__), 'app'),
       os.path.join(os.path.dirname(__file__), 'app/css'),
       os.path.join(os.path.dirname(__file__), 'app/partials')]),
    extensions=['jinja2.ext.i18n'],
    variable_start_string='{$',
    variable_end_string='$}')

jinja_environment.install_gettext_translations(i18n)

urls = (
  r"/browse/noSuchWord", "RedirectPage",
  r"/", "MainPage",
  r"/about", "MainPage",
  r"/(en_US|zh_TW|zh_CN)/", "MainPage",
  r"/(en_US|zh_TW|zh_CN)/browse/([^/]+)/([^/]+)", "WordPage2",
  r"/browse/([^/]+)/([^/]+)", "WordPage",
  r"/(en_US|zh_TW|zh_CN)/browse/([^/]+)", "PrefixPage2",
  r"/browse/([^/]+)", "PrefixPage",
)

def commonTemplateValues(urlLocale, reqHandlerName, prefix=None, word=None):
  userLocale = getLocale(urlLocale, web.ctx.env.get('HTTP_ACCEPT_LANGUAGE'))
  i18n.setLocale(userLocale)
  template_values = {
    'htmlTitle': getHtmlTitle(userLocale, reqHandlerName, i18n, prefix, word),
    'userLocale': userLocale,
    'langQs': json.dumps(parseAcceptLanguage(web.ctx.env.get('HTTP_ACCEPT_LANGUAGE'))),
    'urlLocale': urlLocale,
    'isCompiledJS': isCompiledJS(web.input(js=None).js),
    'isTrack': isTrack(web.input(track=None).track),
  }
  return template_values

class MainPage:
  def GET(self, urlLocale=None):
    template_values = commonTemplateValues(urlLocale, self.__class__.__name__)
    template = jinja_environment.get_template('index.html')
    return template.render(template_values)

def commonPage(prefix, word, reqHandlerName, urlLocale=None):
  prefix = prefix.encode('utf-8')
  if word: word = word.encode('utf-8')
  if not isValidPrefixAndWord(prefix, word):
    raise web.notfound()

  template_values = commonTemplateValues(
      urlLocale, reqHandlerName, prefix, word)

  if reqHandlerName == 'WordPage':
    pageHtml = getWordHtml(prefix, word, urlLocale)
  elif reqHandlerName == 'PrefixPage':
    pageHtml = getPrefixHtml(prefix, urlLocale)
  else:
    raise Exception('invalid reqHandlerName: %s' % reqHandlerName)

  if pageHtml is None: raise web.notfound()
  template_values['pageHtml'] = pageHtml
  template = jinja_environment.get_template('index.html')
  return template.render(template_values)

class WordPage:
  def GET(self, prefix, word):
    return commonPage(prefix, word, self.__class__.__name__)

class WordPage2:
  def GET(self, urlLocale, prefix, word):
    return commonPage(prefix, word, 'WordPage', urlLocale)

class PrefixPage:
  def GET(self, prefix):
    return commonPage(prefix, None, self.__class__.__name__)

class PrefixPage2:
  def GET(self, urlLocale, prefix):
    return commonPage(prefix, None, 'PrefixPage', urlLocale)

class RedirectPage:
  def GET(self):
    raise web.seeother('/')


app = web.application(urls, globals())
app = app.gaerun()