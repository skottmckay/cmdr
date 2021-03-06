#!/usr/bin/env python3

import sys
from collections import defaultdict
 
from yapu.imports.internal import * 
 
"""

# Todo: improve this tool 


correct sequence: IN
 Deck comon
 track deck
 remix deck
 mixer
 fx unit
 browser
 preview player
 loop recorder
 audio recorder
 master clock
 global 
 layout
 modifier
 
 """ 
 
 
 
def print_line(line):
    print("|%s|" % (line))
    
def  remove_parentheses(key):
  if "(" in key:
    key = key.split("(")[0].strip()
  return key
  
def print_entry(value, file):
    print("%s\n%s\n\n" % (value[0], value[1]), file=file)

def entry_to_real(line):
  return line[0].split(',')[1].strip()[1:-1]

  
def real_ignore_list(real):
  """ Ignore common commands
  """
  items = ['slot ', 'slice trigger ', 'midi ']
  for item in items:
    if real.lower().startswith(item):
      return True
  return False

  

file_in_sorted   = 'sorted_commands/traktor_commands_sorted.txt'
file_in_unsorted = '2_cmdr_commands_unsorted.txt'
file_out_sorted  = '3_cmdr_commands_sorted.txt'
file_out_reference = '4_traktor_commands_final.txt'
file_out_rotates = '5_traktor_rotates.txt'

file_in_conditions = '8_cmdr_conditions.txt'
file_out_conditions = '9_cmdr_conditions_out.txt'

file_out_csharp  = 'KnownCommands.cs'

with open(file_in_sorted) as f:
  print("Opening: %s" % (file_in_sorted))
  traktor_order = f.readlines()
  
with open(file_in_unsorted) as f:
  print("Opening: %s" % (file_in_unsorted))
  cmdr_list = f.readlines()

  
  
def read_traktor(cmdr_list):    
  c2 = defaultdict(list)
  i=1
  for line in cmdr_list:
      #print_line(line)
      line = line.strip();
      #line = line.strip();
      #print_line(line)
      
      # ignore comments
      if line.startswith("//"):
          continue
          
      if line.startswith("#"):
          continue
          
      if line == "":
          continue
          
      #print("__", line)
      #sys.exit(0)
          
      if "Analysis" in line:
          #print(line)
          pass
          
          
      if i == 1:
          line1 = line
          i = i+1
          continue
          
      else:
          i = 1
          line2 = line
          
          #print_line(line1)
          #print("_", line1)
          #print("_", line)
          key = line1.split('"')[1].lower()
          #key = remove_parentheses(key)  
            
          
          #print(line, key)
          ret = (line1, line2)
          
          # hack!
          #while key in c2:
          #  key = key + "."
          
          if key in c2.keys():
            print("duplicate keys: %s" % (key) )
          
          c2[key].append(ret) #= ret
         
  return c2
        
def hasNumbers(inputString):
  return any(char.isdigit() for char in inputString)

  
## generate rotatevalues 



def get_enums(c2):

  enum_list = set()
  onoff_list = set()
  for v1 in c2.values():
    v2 = v1[0][0]
    #//print(v2)
    v3 = v2.split(',')[3]
    #print(v3)
    if ("typeof" in v3) and ('<' in v3):
      if "float" in v3.lower():
        continue
      
      v4 = v3.split('<')[1]
      v5 = v4.split('>')[0]
      #print(v5)
      enum_list.add(v5)
    else:
      onoff_list.add(v3)
      
  return (enum_list, onoff_list)

'''
c2 = read_traktor(cmdr_list)
(enum_list, onoff_list) = get_enums(c2)
  
""""
print("rotate (non-enums)")
for v in onoff_list:
  print(v)
"""
      
enum_list = sorted(list(enum_list))

    
with open(file_out_rotates, "w") as f_out:
  print('////// Start of Auto generated code', file=f_out)
  for v5 in enum_list:
    print('} else if (type_name.Contains("Enums.%s")) {' % ( v5) , file=f_out)
    print('   var command2 = (EnumInCommand<%s>)command;' % ( v5), file=f_out)
    print('   var cur_value = command2.Value;', file=f_out)
    print('   command2.Value = cur_value.EnumRotate(step);', file=f_out)
    print('', file=f_out)
    #break
    
  print('}', file=f_out)
  print('////// End of Auto generated code', file=f_out)

 
## conditions enums follows:
 
'''  

  
with open(file_in_conditions) as f:
  print("Opening: %s" % (file_in_conditions))
  conditions_list = f.readlines()


conditions_data = read_traktor(conditions_list)
(enum_list, onoff_list) = get_enums(conditions_data)
  
print("rotate (non-enums)")      
for v in onoff_list:
  print(v)
  
      
enum_list = sorted(list(enum_list))

    
with open(file_out_conditions, "w") as f_out:
  print('////// Start of Auto generated code', file=f_out)
  for v5 in enum_list:
    print('} else if (type_name.Contains("Enums.%s")) {' % ( v5) , file=f_out)
    print('   var command2 = (EnumCondition<%s>)command;' % ( v5), file=f_out)
    print('   var cur_value = command2.Value;', file=f_out)
    print('   command2.Value = cur_value.EnumRotate(step);', file=f_out)
    print('', file=f_out)
    #break
    
  print('}', file=f_out)
  print('////// End of Auto generated code', file=f_out)
  
        
        
        
  
sys.exit(0)
  
  
  
ranges = []  
for key in c2.keys():
  if hasNumbers(key):
    #print(key)
    ranges.append(key)


#data1 = open('2_cmdr_commands_unsorted.txt').readlines()
#data2 = [a for a in data if "Command" in a ]
#data3 = [ a.split('"')[1] for a in data2 ]
#data4 = [ a for a in data3 if "1" in a ]

# to generate list of rotatable commands
# cat 2_cmdr_commands_unsorted.txt | sort -u |  grep "=" |  awk '$1 ~ /[1]/{print "KnownCommands."$1}' | sort -V


# sys.exit(1)        

###########   
f_out = open(file_out_sorted, "w")    

c3 = c2.copy()
txt_not_matches = []
traktor_collisions = dict()
for line in traktor_order:
    line = line.strip();
    #print(line)
    if line == "":
        continue
        
    if line.startswith("//"):
        continue
        
    if line.startswith("#"):
        continue
         
        
    if ">" in line:
        line = line.split(">")[-1].strip()
        
    line = line.lower()    

    #if not "cup" in line:
    #  continue
    
    if line in traktor_collisions.keys():
      print("Traktor collision: %s" % (line))
    traktor_collisions[line] = 1
      
    if line in c3.keys():
        for result in c3[line]:
          print_entry(result, f_out)
        del c3[line]
    else:
        txt_not_matches.append(line)
        
        if "analysis" in line.lower():
          print(result)

        #print(c3.keys())
        #sys.exit(0)
        
# print remaining commands that did not match as-is" (ie, unsorted
print("\n\n//\n// remaining commands (unsorted). To sort them, add names to traktor_commands_sorted.txt\n//\n\n", file=f_out)
for line in c3:
  for result in c3[line]:
    print_entry(result, f_out)
    
f_out.close()
print("Wrote: %s" % (file_out_sorted) )



#########
# print out a file showing the shorthands and the C# commands that did not match
f_out = open(file_out_reference, "w")    

c_not_matches=[]
for line in c3:
  if(len(c3[line]) > 1):
    #print(line)
    pass
    
  for result in c3[line]:
    real = entry_to_real(result)
       
    if real_ignore_list(real):
      continue
  
    ret = entry_to_real(result)
    
    
    if "analysis" in ret.lower():
        print("")
        print(ret)
        print(result)
        print("dede")
        #sys.exit(0)
        #sys.exit(0)
     
    c_not_matches.append(ret) 

sort_final_file = False
if sort_final_file:
  txt_not_matches = sorted(txt_not_matches)
  c_not_matches = sorted(c_not_matches)


def list_to_file(items, f_out):
  for item in items:
    print("%s" % (item) , file=f_out)


print("")

print("sort names not matched:\n",  file=f_out)
list_to_file(txt_not_matches, f_out)
  
print("\n\n\n******\n\n\n\n",  file=f_out)

print("c# names not matched:\n",  file=f_out)
list_to_file(c_not_matches, f_out)



 
f_out.close()
print("Wrote: %s" % (file_out_reference) )


#bp() 

#a = open('cmdr_commands_sorted.txt').readlines()
#data = open('cmdr_commands_sorted.txt').readlines()
#data2  = [a for a in data if "typeof" in a][:10]
#data3 = [a.split(',')[1].strip().strip()[1:-1] for a in data2]

    
print("All done. Copy-paste the contents of %s into %s, and remove last comma" % (file_out_sorted, file_out_csharp))
