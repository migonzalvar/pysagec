from pysagec import base


def test_field():
    f = base.Field('tag')
    assert f.__get__(None, None) is f
    assert 'Field' in repr(f)


def test_model_as_dict():
    class MyModel(base.Model):
        root_tag = 'root'
        prop1 = base.Field('tag1')
        prop2 = base.Field('tag2')

    model = MyModel(prop1=42)
    model.prop2 = 'foo'

    assert model.prop1 == 42
    assert {'root': [{'tag1': 42}, {'tag2': 'foo'}]} == model.as_dict()


def test_model_default():
    class MyModel(base.Model):
        root_tag = 'root'
        prop = base.Field('tag', default='x')

    model = MyModel()
    assert model.prop == 'x'
