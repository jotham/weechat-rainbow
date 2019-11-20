# -*- encoding: utf-8 -*-
#!/usr/bin/env python2

SCRIPT_NAME    = 'rainbow'
SCRIPT_AUTHOR  = 'jotham.read@gmail.com'
SCRIPT_VERSION = '0.2'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC    = 'Replaces ***text*** in input buffer with rainbow text'

# Hook configuration:
#
#    MESSAGE. Doesn't modify buffer history, wont fire on all commands?
#    INPUT. Modifies buffer history, captures commands like /me /msg etc.

MODE='INPUT'

import re

glitter_pat = re.compile('(?:\*{3}([^*].*?)\*{3})')
def glitter_it(input_re):
   lut = ('13','04','08','09','11','12') # len=6
   text = input_re.group(1).decode('utf-8')
   characters = []
   for i, character in enumerate(text):
      if character == ' ' or character == ',':
         characters.append(character)
      else:
         characters.append('\x03'+lut[i%6]+character)
   return "".join(characters).encode('utf-8') + '\x0399' + '\x0F'

def command_input_text_for_buffer(data, modifier, modifier_data, input):
   return glitter_pat.sub(glitter_it, input)

def command_run_input(data, buffer, command):
   if command == '/input return':
      input = weechat.buffer_get_string(buffer, 'input')
      if input.startswith('/set '): # Skip modification of settings
         return weechat.WEECHAT_RC_OK
      input = glitter_pat.sub(glitter_it, input)
      weechat.buffer_set(buffer, 'input', input)
   return weechat.WEECHAT_RC_OK

try:
   import weechat
except ImportError:
   # Assume commandline mode
   import sys
   cc ={
      # couple of these translate to the nearest
      "00": "\033[97m", # white
      "01": "\033[30m", # black
      "02": "\033[34m", # blue
      "03": "\033[32m", # green
      "04": "\033[91m", # red -> light red
      "05": "\033[31m", # brown -> red
      "06": "\033[35m", # purple
      "07": "\033[33m", # orange -> yellow
      "08": "\033[93m", # yellow -> light yellow
      "09": "\033[92m", # light green
      "10": "\033[36m", # cyan
      "11": "\033[96m", # light cyan
      "12": "\033[94m", # light blue
      "13": "\033[95m", # pink -> light magenta
      "14": "\033[90m", # grey -> dark grey
      "15": "\033[37m", # light grey
      "99": "\033[0m",  # reset
   }
   if len(sys.argv) > 1:
      input = ' '.join(sys.argv[1:])
   else:
      input = 'Hello ***wor*ld!***'
   glit = glitter_pat.sub(glitter_it, input)
   pat = re.findall("\\x03(\d{2})", glit)
   for color in pat:
      glit = glit.replace(color, cc[color])
   print(glit)

else:
   if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, '', ''):
      if MODE == 'MESSAGE':
         weechat.hook_modifier('input_text_for_buffer', 'command_input_text_for_buffer', '')
      else:
         weechat.hook_command_run('/input return', 'command_run_input', '')

