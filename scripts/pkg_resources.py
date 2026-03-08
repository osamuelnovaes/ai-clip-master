# Shim for pkg_resources using importlib.metadata
# This fixes the ModuleNotFoundError in Python 3.13+ for old libraries like MoviePy
import importlib.metadata

def resource_filename(package, resource):
    # Minimal implementation to avoid crashes
    return ""

def get_distribution(package):
    class Distribution:
        def __init__(self, version):
            self.version = version
    try:
        ver = importlib.metadata.version(package)
        return Distribution(ver)
    except:
        return Distribution("0.0.0")
