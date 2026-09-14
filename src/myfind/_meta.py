from importlib.metadata import version, PackageNotFoundError

try:
    VERSION = version('myfind')
except PackageNotFoundError:
    VERSION = "0.0.0-dev"
MATCHED_FILE_NAME = '.patterns'
