from collections import OrderedDict as odict


class Empty:
    pass


def filter_empty(iterable):
    return list(item for item in iterable if item is not Empty)


class Field:
    def __init__(self, tag_name, *, default=None, ignore_if_none=False):
        self.tag_name = tag_name
        self.value = None
        self.default = default
        self.ignore_if_none = ignore_if_none

        # This value will be set by metaclass
        self.name = None

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        else:
            return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        self.value = value
        obj.__dict__[self.name] = value

    def as_dict(self, obj):
        value = self.__get__(obj)
        if self.ignore_if_none and value is None:
            return Empty
        return {self.tag_name: value}


class String(Field):
    def __repr__(self):
        return '<String name={!r}>'.format(self.name)


class Nested(Field):
    def __init__(self, tag_name, model, default=None,
                 unwrap=False, many=False, **kwargs):
        super().__init__(tag_name, default=default, **kwargs)

        assert not (many and unwrap), ('If `many` is `True `unwrap` must be '
                                       'set to `False`')

        self.model = model
        self.unwrap = unwrap
        self.many = many
        self.default = [model()] if many else model()

    def as_dict(self, obj):
        data = self.__get__(obj)
        if data is None:
            return Empty if self.ignore_if_none else None

        if self.many:
            return {
                self.tag_name: filter_empty([item.as_dict() for item in data])
            }

        value = data.as_dict()
        if self.unwrap:
            return {self.tag_name: value[self.model.root_tag]}

        return {self.tag_name: value}

    def __repr__(self):
        return '<Nested name={!r} model={!r}>'.format(self.name, self.model)


class ModelMeta(type):
    def __new__(mcs, clsname, bases, clsdict):
        fields = []
        for name, value in clsdict.items():
            if isinstance(value, Field):
                value.name = name  # Init `Field.name`
                fields.append(value)
        clsdict['fields'] = fields
        return type.__new__(mcs, clsname, bases, clsdict)

    @classmethod
    def __prepare__(mcs, clsname, bases):
        # By returning an OrderedDict instead of a normal dictionary,
        # the resulting definition order is easily captured.
        # See Python Cookbook, Third Edition. Chapter 9
        return odict()


class Model(metaclass=ModelMeta):
    root_tag = 'root'

    @classmethod
    def from_dict(cls, data):
        kwargs = {}
        for el in data[cls.root_tag]:
            kwargs.update(el)
        return cls(**kwargs)

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def as_dict(self):
        return {
            self.root_tag: filter_empty([f.as_dict(self) for f in self.fields])
        }

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()
