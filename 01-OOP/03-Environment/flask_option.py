# pylint: disable=missing-docstring

import os

def start():
    a=os.environ.get("FLASK_ENV")
    if a=="development":
        return "Starting in development mode..."
    elif a=="production":
        return "Starting in production mode..."
    else:
        return "Starting in production mode..."

if __name__ == "__main__":
    print(start())
