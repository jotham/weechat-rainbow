#!/usr/bin/env python

SCRIPT_NAME    = "rainbow"
SCRIPT_AUTHOR  = "jotham.read@gmail.com"
SCRIPT_VERSION = "0.2"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Replaces ***text*** in input buffer with rainbow text"

# Hook configuration:
#
#    MESSAGE. Doesn't modify buffer history, wont fire on all commands?
#    INPUT. Modifies buffer history, captures commands like /me /msg etc.

MODE="INPUT"

import re

glitter_pat = re.compile("\*\*\*([^\*]+)\*\*\*")
def glitter_it(input_re):
   lut = ("13","04","08","09","11","12") # len=6
   text = input_re.group(1)
   characters = []
   for i, character in enumerate(text):
      if character == ' ' or character == ',':
         characters.append(character)
      else:
         characters.append("\x03"+lut[i%6]+character)
   return "".join(characters) + "\x0399"

def command_input_text_for_buffer(data, modifier, modifier_data, input):
   return glitter_pat.sub(glitter_it, input)

def command_run_input(data, buffer, command):
   if command == "/input return":
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
   if len(sys.argv) > 1:
      input = ' '.join(sys.argv[1:])
   else:
      input = 'Hello ***world!***'
   print(glitter_pat.sub(glitter_it, input).replace("\x03", "^C"))
else:
   if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
      if MODE == "MESSAGE":
         weechat.hook_modifier("input_text_for_buffer", "command_input_text_for_buffer", "")
      else:
         weechat.hook_command_run("/input return", "command_run_input", "")

