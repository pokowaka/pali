#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os 
import shutil

"""
$PALI_DIR is the dir of git clone https://github.com/siongui/pali.git
Manual setup (for reference):
1. setup TongWen (deprecated):
```bash
  cd $PALI_DIR
  mkdir -p common/app/scripts/ext
  cd common/app/scripts/ext/
  wget http://tongwen.openfoundry.org/src/web/tongwen_core.js
  wget http://tongwen.openfoundry.org/src/web/tongwen_table_s2t.js
  wget http://tongwen.openfoundry.org/src/web/tongwen_table_t2s.js
  wget http://tongwen.openfoundry.org/src/web/tongwen_table_ps2t.js
  wget http://tongwen.openfoundry.org/src/web/tongwen_table_pt2s.js
```

2. setup jianfan (deprecated):
```bash
  wget https://python-jianfan.googlecode.com/files/jianfan-0.0.2.zip
  unzip jianfan-0.0.2.zip
  mv jianfan-0.0.2/jianfan $PALI_DIR/common/pylib/
  rm -rf jianfan-0.0.2
```

3. create symbolic links:
```bash
  cd $PALI_DIR/tipitaka
  ln -s ../common/ common

  cd $PALI_DIR/tipitaka/pylib
  ln -s ../../../data/tipitaka/translation/ translation
  ln -s ../../../data/tipitaka/romn/ romn

  cd $PALI_DIR/dictionary
  ln -s ../common/ common

  cd $PALI_DIR/common/pylib
  ln -s ../../../data/pylib/jianfan/ jianfan
```
"""


def ln(source, link_name):
  if os.path.islink(link_name):
    os.unlink(link_name)
  os.symlink(source, link_name)


def setupSymlinks():
  # enter tipitaka dir
  os.chdir(os.path.join(os.path.dirname(__file__), '../tipitaka'))
  ln('../common/', 'common')
  os.chdir('pylib')
  ln('../../../data/tipitaka/translation/', 'translation')
  ln('../../../data/tipitaka/romn/', 'romn')
  # enter dictionary dir
  os.chdir('../../dictionary')
  ln('../common/', 'common')
  # enter common dir
  os.chdir('../common/pylib')
  ln('../../../data/pylib/jianfan/', 'jianfan')


if __name__ == '__main__':
  # copy necessary css file to css directory of tipitaka webapp
  tipitakaLatnCssPath = os.path.join(os.path.dirname(__file__),
      '../../data/tipitaka/romn/cscd/tipitaka-latn.css')
  dstPath = os.path.join(os.path.dirname(__file__),
      '../tipitaka/app/css/tipitaka-latn.css')
  shutil.copyfile(tipitakaLatnCssPath, dstPath)

  setupSymlinks()

  # cannot import i18nUtils in the beginning of the file because symlink to
  # jianfan is not yet created
  from i18nUtils import doAll
  doAll()

