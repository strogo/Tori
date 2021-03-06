"""
:Author: Juti Noppornpitak <jnopporn@shiroyuki.com>
"""
import inspect
from tori.db.common    import PseudoObjectId
from tori.db.exception import LockedIdException

def entity(*args, **kwargs):
    """ Entity decorator

        :param collection_name: the name of the collection
        :type  collection_name: str
        :return: the decorated object
        :rtype:  object
    """
    # Get the first parameter.
    first_param = args[0]

    # If the first parameter is really a reference to a class, then instantiate
    # the singleton instance.
    if len(args) == 1 and inspect.isclass(first_param) and isinstance(first_param, type):
        class_reference = first_param

        return prepare_entity_class(class_reference)

    # Otherwise, use the closure to handle the parameter.
    def decorator(class_reference):
        return prepare_entity_class(class_reference, *args, **kwargs)

    return decorator

def prepare_entity_class(cls, collection_name=None):
    """ Create a entity class

    :param cls: the document class
    :type  cls: object
    :param collection_name: the name of the corresponding collection where the
                            default is the lowercase version of the name of the
                            given class (cls)
    :type  collection_name: str

    The object decorated with this decorator will be automatically provided with
    one additional attribute.

    =================== ======== =================== ==== ==============================
    Attribute           Access   Description         Read Write
    =================== ======== =================== ==== ==============================
    id                  Instance Document Identifier Yes  Yes, ONLY ``id`` is undefined.
    __collection_name__ Static   Collection Name     Yes  Yes, but NOT recommended.
    __relational_map__  Static   Relational Map      Yes  Yes, but NOT recommended.
    __session__         Static   DB Session          Yes  Yes, but NOT recommended.
    =================== ======== =================== ==== ==============================

    For example,

    .. code-block:: python

        @entity
        class Note(object):
            def __init__(self, content, title=''):
                self.content = content
                self.title   = title
                
    where the collection name is automatically defined as "note".
    
    .. tip::
    
        You can define it as "notes" by replacing ``@entity`` with ``@entity('notes')``.
    """
    if not cls:
        raise ValueError('Expecting a valid type')

    def get_id(self):
        return self.__dict__['_id'] if '_id' in self.__dict__ else None

    def set_id(self, id):
        """
        Define the document ID if the original ID is not defined.

        :param id: the ID of the document.
        """
        if '_id' in self.__dict__ and self.__dict__['_id']\
            and not isinstance(self.__dict__['_id'], PseudoObjectId):
            raise LockedIdException('The ID is already assigned and cannot be changed.')

        self._id = id

    cls.__collection_name__ = collection_name or cls.__name__.lower()
    cls.__relational_map__  = {}
    cls.__session__         = None

    cls.id = property(get_id, set_id)

    return cls

class Entity(object):
    """ Dynamic-attribute Base Document

        :param attributes: key-value dictionary
        :type  attributes: dict

        Here is an example on how to use this class.

        .. code-block:: python

            @entity
            class Note(Entity): pass

    """
    def __init__(self, **attributes):
        for name in attributes:
            self.__setattr__(name, attributes[name])

class BasicAssociation(object):
    """ Basic Association

        :param origin: The origin of the association
        :type  origin: object
        :param destination: The destination (endpoint) of the association
        :type  destination: object

        .. note:: This class is used automatically by the association mapper.
    """
    def __init__(self, origin, destination):
        self.origin      = origin
        self.destination = destination