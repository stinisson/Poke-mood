import sys
import time

def delay_print(intro_text, s, a):
    print(intro_text)
    for i in s:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.3)
    print(a)
    time.sleep(0.5)

def atk_txt(attacker, reciver, text):
    print(f"{attacker} attackerar {reciver} ")
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.3)
    print('''
          |
O=========|>>>>>>>>>>>>>>>>>>>>>>>>>>
          |
    ''')
    time.sleep(0.5)

def successful_block(blocker):
    print(f"{blocker} försöker blockera")
    text = "Lyckad block!"
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)
    print('''
      |`-._/\_.-`|
      |    ||    |
      |___o()o___|
      |__((<>))__|
      \   o\/o   /
       \   ||   /
        \  ||  /
         '.||.'
    ''')

def unsuccessful_block(blocker):
    print(f"{blocker} försöker blockera")
    text = "Misslyckad block!"
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)
    print('''
      |`-._/<    <\_.-`|
      |    |>    >|    |
      |___o(<    <)o___|
      |__((<>    >>))__|
      \   o\>   > /o   /
       \   |<    <|   /
        \  |>    <|  /
          '.|>   <|.'
    ''')
