
import re

re_table = re.compile(r'^table ([\w_]+)')
re_field = re.compile(r'^([\w_]+)\s([\w_]+)')

class FileReader:

  index = 'default'
  matrix = {}

  def __init__(self, lines):
    for line in lines:
      self.process_line(line)
    
  
  def process_line(self, raw):
    if self.line_is_table(raw):
      table = self.extract_table_name(raw)
      self.index = table
      
    
    elif self.line_is_table_close(raw):
      self.index = None
    
    elif self.index == None:
      return
    
    elif self.line_is_field(raw):
      field = self.extract_field_values(raw.strip())
      self.put(self.index, field)
      
  def put(self, key, value):
    if not key in self.matrix:
      self.matrix[key] = []
    
    self.matrix[self.index].append(value)
  
  def line_is_table_close(self, line):
    return line.strip() == "}"

  def line_is_table(self, line):
    return re_table.match(line)
  
  def extract_table_name(self, line):
    return re_table.match(line).group(1)
  
  def line_is_field(self, line):
    return re_field.match(line.strip())
  
  def extract_field_values(self, line):
    result = re_field.match(line.strip())
    return {
      "name": result.group(1),
      "type": result.group(2),
    }