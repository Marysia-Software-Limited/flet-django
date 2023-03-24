from typing import TypeVar

DESTINATION_CLASS = TypeVar('DESTINATION_CLASS', bound='Destiny')
CLIENT_CLASS = TypeVar('CLIENT_CLASS', bound='GenericClient')
VIEW_FACTORY = TypeVar('VIEW_FACTORY', bound='GenericViewFactory')
