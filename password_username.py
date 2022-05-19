#--------------------------------------------------------------------------------
# Random Password Generator
#--------------------------------------------------------------------------------
import string
import random

# List of usable characters, ignoring commonly confused ones
CHARS = [x for x in string.ascii_letters+string.digits \
         if x not in ['i','I','l','L','o','O','0','1']]

def gen_password(size=8, chars=CHARS):
    return ''.join(random.choice(chars) for i in range(size))

#--------------------------------------------------------------------------------
# Basic Username convertor
#--------------------------------------------------------------------------------
def gen_username(name_in):
  # Generate a username based on supplied First and Last name
    if ',' in name_in:
        last, first = name_in.lower().split(',')
    elseif ' ' in name_in:
        first, last = in_data.lower().split(' ')
    last, first = last.strip(), first.strip()
    return first[0]+last

#--------------------------------------------------------------------------------
# 
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# 
#--------------------------------------------------------------------------------
