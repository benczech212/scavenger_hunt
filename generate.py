from translate import Translator
import qrcode
import binascii

url_qr1 = f"https://drive.google.com/file/d/1PMGamqCFdzp3lni1azUNQh-zIfyAztnC/view?usp=sharing"
photo_clue = f"https://drive.google.com/file/d/1CKsVG9fDSFH-AqBxombvKMqNJMBGgUE6/view?usp=sharing"



instructions_english = "Can you find this tree? Your next clue will be hiding by the trunk. Yep, that's right, you'll have to go outside. *queue Ben smirk*"

translator = Translator(to_lang="es")
instructions_spanish = translator.translate(instructions_english)
instructions_spanish += f"\n{photo_clue}"
instructions_hex = instructions_spanish.encode().hex()
instructions_hex_with_spaces = ' '.join([instructions_hex[i:i+2] for i in range(0, len(instructions_hex), 2)])
instructions_binary = ''.join(format(ord(char), '08b') for char in instructions_hex_with_spaces)
instructions_substituted = instructions_binary.replace('1', 'one').replace('0', 'zero')

with open('qr1.txt', 'w') as file:
    file.write(url_qr1)

with open('encrypted_clue.txt', 'w') as file:
    file.write(instructions_substituted)



qr1 = qrcode.make(url_qr1)
qr1.save('qr1.png')



# Print URLs for QR codes
print(f"URL for the first QR code: {url_qr1}")

