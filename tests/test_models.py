from pysagec import models


def test_field():
    f = models.Field('tag')
    assert f.__get__(None, None) is f
    assert 'Field' in repr(f)


def test_model_as_dict():
    class MyModel(models.Model):
        root_tag = 'root'
        prop1 = models.Field('tag1')
        prop2 = models.Field('tag2')

    model = MyModel(prop1=42)
    model.prop2 = 'foo'

    assert model.prop1 == 42
    assert {'root': [{'tag1': 42}, {'tag2': 'foo'}]} == model.as_dict()


def test_model_default():
    class MyModel(models.Model):
        root_tag = 'root'
        prop = models.Field('tag')

    model = MyModel()
    assert model.prop is None
