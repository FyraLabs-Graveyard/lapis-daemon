#!/usr.bin/env python
## Lapis builder daemon
#
# import all modules in lapisd/ as lapisd.module
#
import os
import sys
import time
import signal
import logging
import logging.handlers
import argparse
import traceback
import threading
import lapisd.config