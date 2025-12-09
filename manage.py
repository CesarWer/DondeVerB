#!/usr/bin/env python
import os
import sys


def main():
    # Prefer an explicit env var; otherwise detect project package folder
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        # If the original package name exists, use it; otherwise try alternative
        if os.path.isdir(os.path.join(os.path.dirname(__file__), 'dondever')):
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dondever.settings')
        elif os.path.isdir(os.path.join(os.path.dirname(__file__), 'dondeverapp')):
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dondeverapp.settings')
        else:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dondever.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
