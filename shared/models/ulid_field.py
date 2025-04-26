from django.db import models
import ulid

def generate_ulid():
  return ulid.new().str

class ULIDField(models.CharField):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault("max_length", 26)
    kwargs.setdefault("default", generate_ulid)
    kwargs.setdefault("editable", False)
    kwargs.setdefault("unique", True)
    super().__init__(*args, **kwargs)
