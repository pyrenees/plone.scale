"""
Image storage
=============

Storage and retrieval of images is abstracted, allowing different
implementations to be used.

Scales can be retrieved using either their scaling parameters or via an
identification code generated by the storage.
"""

from zope.interface import Attribute
from zope.interface import Interface

class IImageScale(Interface):
    """A scaled image. This is a very simple wrapper around an image scale
    which gives access to its metadata.

    The `id` attribute is usually only guaranteed to be unique within the
    context of a specific original image. For certain storage implementations
    it may be globally unique as well.
    """

    id = Attribute("An identifier uniquely identifying this scale")
    dimensions = Attribute("A (width, height) tuple with the image dimensions.")
    url = Attribute("Absolute URL for this image.")
    mimetype = Attribute("The MIME-type of the image.")
    size = Attribute("The size of the image data in bytes.")



class IImageScaleStorage(Interface):
    """This is an adapter for an image which can store, retrieve and generate
    image scales. It provides a dictionary interface to existing image scales
    using the scale id as key. To find or create a scale based on its scaling
    parameters use the `:func:getScale` method.
    """

    def __init__(image):
        """Adapter constructor."""


    def getScale(width=None, height=None, direction=None, create=True):
        """Find a scale based on its parameters. The parameters can be anything
        supported by `:func:scaleImage`. If an existing scale is found it is
        returned in an `:obj:IImageScale` wrapper. If the scale does not exists
        it will be created, unless `create` is `False` in which case `None`
        will be returned instead.
        """

    def __getitem__(self, key):
        """Find a scale based on its id."""



class AnnotationStorage(object):
    """:obj:`IImageScaleStorage` implementation using annotations. Image data
    is stored as an annotation on the object container the image. This is
    needed since not all images are themselves annotatable.

    The image scales are stored as dictionaries in an annotation with
    `plone.scale.<field>.<id>` as key. Each image scale dictionary has the
    following keys:

    * dimensions: A (width, height) tuple with the image dimensions.
    * mimetype: the MIME type of the image
    * size: size of the image data in bytes
    * data: the raw image data

    In addition a list of all image scales and their parameters are maintained
    in an annotation with key `plone.scale.<field>`. This makes it possible to
    find an existing scale with specific parameters without having to iterate
    over all scales.
    """

    implements(IImageScaleStorage)