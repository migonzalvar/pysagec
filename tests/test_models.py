from pysagec import models


def test_models_are_instantiable():
    a = models.AuthInfo()
    assert isinstance(a, models.Model)
