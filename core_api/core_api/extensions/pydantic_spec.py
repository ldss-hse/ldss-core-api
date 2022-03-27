"""
A module for instantiating global validation of REST API endpoints
"""

from flask_pydantic_spec import FlaskPydanticSpec

PYDANTIC_VALIDATOR = FlaskPydanticSpec("flask", title="Demo API", version="v1.0", path="doc")
