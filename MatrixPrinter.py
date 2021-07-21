from datetime import datetime
from os import makedirs

class MatrixPrinter:

  types = {
    'varchar': 'string',
    'int': 'integer',
    'smallint': 'smallInteger',
    'tinyint': 'tinyInteger',
    'bool': 'boolean',
    'datetime': 'dateTime',
  }
  
  def __init__(self, matrix):
    output_path = './output/%s' % self.get_timestamp()
    makedirs(output_path, exist_ok=True)

    for table_name, fields in matrix.items():
      
      fields = self.get_field_print_lines(fields)
      self.print_table(table_name, "\n".join(fields))

      with open('./template.php', 'r') as file:
        template = file.read()

      
      date = self.get_timestamp()
      filename = "%s_create_%s_table.php" % (date, table_name)
      
      with open("%s/%s" % (output_path, filename), 'w') as file:
        template = template.replace("$TABLE_NAME$", table_name)

        class_name = "Create%sTable" % table_name.capitalize()
        template = template.replace("$CLASS_NAME$", class_name)
        
        table_fields = "\n".join(map(lambda x: '            ' + x, fields))
        template = template.replace("$TABLE_FIELDS$", table_fields)
        
        file.write(template)
  
  def get_timestamp(self):
    return datetime.today().strftime("%Y_%m_%d_%H%M%S")
  
  def print_table(self, table_name, content):
    title = ' %s ' % table_name
    print(''.center(45, '='))
    print(title.upper().center(45, '='))
    print(''.center(45, '='))
    print(content)
    print(''.center(45, '='))
    print()
    print()

  
  
  def get_field_print_lines(self, fields):
    fields = self.process_fields(fields)
    lines = []
    for field in fields:
      name = field.get('name', '')
      type = field.get('type', 'string')
      name = "'%s'" % name if name else ''
      lines.append(
        "$table->%s(%s);" % (type, name)
      )
    return lines
  
  def process_fields(self, fields):
    
    # Timestamps
    matches = [x for x in fields if x.get('name') in ['created_at', 'updated_at'] ]
    if len(matches) >= 2:
      for x in matches:
        fields.remove(x)
      fields.append({
        "type": 'timestamps',
      })
    
    for field in fields:
      
      # Soft deletes
      if field.get('name') == 'deleted_at':
        field['name'] = ''
        field['type'] = 'softDeletes'
      
      # Unsigned big integers
      elif field.get('name', '').endswith('_id'):
        field['type'] = 'unsignedBigInteger'
      
      # Increments
      elif field.get('name') == 'id':
        field['type'] = 'increments'
      
      else:
        field['type'] = self.types.get(field['type'].lower(), field['type'])
    
    return fields