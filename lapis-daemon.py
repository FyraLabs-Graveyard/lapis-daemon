## Lapis builder daemon
#
# import basic modules
import copy
import glob
import grp
import io
import json
import logging
import logging.handlers
import os
import pwd
import random
import re
import shutil
import signal
import smtplib
import socket
import subprocess
import sys
import time
import traceback
import xml.dom.minidom
import zipfile
from fnmatch import fnmatch
from gzip import GzipFile
from optparse import SUPPRESS_HELP, OptionParser