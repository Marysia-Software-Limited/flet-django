from typing import TypeVar

DESTINATION_CLASS = TypeVar('DESTINATION_CLASS', bound='Fatum')
PAGE_CLASS = TypeVar('PAGE_CLASS', bound='GenericPage')
VIEW_FACTORY = TypeVar('VIEW_FACTORY', bound='GenericViewFactory')
