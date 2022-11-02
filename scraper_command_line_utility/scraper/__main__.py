import sys

from .main import main

# If main() exits with an Exception, a string, or a non-zero integer, then sys.exit will produce an error on the
# command line.
sys.exit(main())
