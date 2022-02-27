"""
Automatically generated module for loading configuration
"""

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="CORE_API",
    settings_files=['settings.toml', '.secrets.toml'],
)
