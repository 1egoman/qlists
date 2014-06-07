from base import *
import os
import datetime
import json


# to-do list words
todo_words = ["todo", "to do", "to-do", "reminder", "remind", "list"]
remove_words = ["check", "remove", "cross", "crossout", "checkoff", "delete"]
remove_preps = ["on", "from", "at"]

"""
Main todo class
"""
class todo_handler(parser):


  def validate(self):
    x = len([1 for i in todo_words if i in self.query]) 
    y = len([1 for i in remove_words if i in self.query]) 
    return x or ("add" in self.query and x) or (y and x)


  def parse(self, parent): 

    # open the reminder file
    rmds = None
    with open( os.path.join(self.get_plugin_dir(__file__), "reminders.json") ) as r:
      rmds = json.loads( r.read() )


    # remove an item from a list
    words = [i for i in remove_words if i in self.query]
    if len(words):

      # find out which list was asked
      for lists,contents in rmds.items():
        if lists in self.query:
          # found it!
          data = {}
  
          for p in remove_preps:
            if p in self.query:

              # remove from list
              data["name"] = ' '.join( self.query[ self.query.index(words[0])+1:self.query.index(p) ] )
              try:
                rmds[lists].remove(data)
              except ValueError:
                # not in list
                self.resp["text"] = "%s isn't in %s" % (data['name'], lists)
                self.resp["status"] = STATUS_OK
                self.resp["type"] = "todo"
                return self.resp

              # add back into file
              with open( os.path.join(self.get_plugin_dir(__file__), "reminders.json"), 'w') as r:
                r.write( json.dumps(rmds, indent=2) )

              # status
              self.resp["text"] = "removed %s" % data["name"]


    # add an item to a list
    elif "add" in self.query:

      # add list item
      # find out which list was asked
      for lists,contents in rmds.items():
        if lists in self.query:

          # add list item
          data = {}
          data["name"] = ' '.join( self.query[ self.query.index("add")+1:self.query.index("to") ] )
          rmds[lists].append(data)

          self.resp["text"] = "added %s" % data["name"]
          self.resp["status"] = STATUS_OK
          self.resp["type"] = "todo"
          return self.resp

      # otherwise, add a whole new list

      list_name = ' '.join( self.query[ self.query.index("add")+1: ] )

      rmds[list_name] = []
      self.resp["text"] = "added new list %s" % list_name

      # update file
      with open( os.path.join(self.get_plugin_dir(__file__), "reminders.json"), 'w') as r:
        r.write( json.dumps(rmds, indent=2) )




    # user asked for a todo list?
    elif len([1 for i in todo_words if i in self.query]):
      # find out which one
      for lists,contents in rmds.items():
        if lists in self.query:
          # found it!
          lst = []
          for item in contents:

            if item.has_key("name") and item.has_key("when") and item.has_key("where"):
              when = datetime.datetime.strptime(item["when"], "%c")
              lst.append( "%s on %s, at %s" % (item["name"], when.strftime("%A, %B %d"), item["where"]) )

            elif item.has_key("name") and item.has_key("when"):
              when = datetime.datetime.strptime(item["when"], "%c")
              lst.append( "%s on %s" % (item["name"], when.strftime("%A, %B %d")) )

            elif item.has_key("name") and item.has_key("where"):
              lst.append( "%s at %s" % (item["name"], item["where"]) )

            elif item.has_key("name"):
              lst.append( item["name"] )

          self.resp["return"] = lst
          self.resp["text"] = "; ".join(lst)





    # return
    self.resp["status"] = STATUS_OK
    self.resp["type"] = "todo"
    return self.resp



