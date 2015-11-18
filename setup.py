#!/usr/bin/env python
import sys
from distutils.core import setup



setup(name='termweather',
   version='0.1',
   description='displays the weather in the terminal',
   author='Olivia Schaefer',
   author_email='taygetea@gmail.com',
   url='https://github.com/taygetea/weather',
   packages=('termweather',),
   scripts=(
        'src/bin/weather',
   ),
   package_dir={'termweather':'src/lib'}
)
