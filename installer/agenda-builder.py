#!/usr/bin/env python

"""
Run agendabuilder from an installed bundle
"""

import sys

sys.dont_write_bytecode = True


from agendabuilder.commands import main

sys.exit(main())
