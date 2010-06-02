#!/usr/bin/env python

import sys, os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import skameyka
    
skameyka.app.run(port=5001, debug=True)