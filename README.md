This contains all that you (minimally) need to start a plugin. 
---
##NOTE: This plugin goes with my project at https://github.com/1egoman/qparser


All a plugin minimally has to have is an info.json:
```json
{
  "name": "Plugin Name",
  "desc": "Short Description, maybe a line or so",
  "author": "Your name, contact info",
  "main": "main_file.py:sample_plugin"
}
```

and a main_file.py (named accordingly in info.json):

```python
from base import *
class sample_plugin(parser):
  
  # wether to run the plugin based on the user's query
  def validate(self):
    # the query is available under self.query to test against
    return False
  
  # parse the query if it was validated
  def parse(self): 
    self.resp["text"] = "The Response"
    self.resp["status"] = STATUS_OK
    return self.resp
```

Put both those files in a folder inside the plugins folder, and you've made a small plugin (that does nothing)!
