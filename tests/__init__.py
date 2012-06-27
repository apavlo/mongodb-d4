# -*- coding: utf-8 -*-

# Third-Party Dependencies
import os, sys
basedir = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, "../libs"))
sys.path.append(os.path.join(basedir, "../src"))

from mongodbtestcase import MongoDBTestCase