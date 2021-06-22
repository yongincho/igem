import encrypt
import encode_lee
import pandas as pd

print("ENCRYPT/DECRYPT")

key = 'secret'
message = "text"

aes = encrypt.AESCipher(key)

encrypt_text = aes.encrypt(message)
decrypt_text = aes.decrypt(encrypt_text)

print(encrypt_text)
print(decrypt_text)


print("LEE METHOD")

lee = encode_lee.Lee()

csv_path = input("Input your csv file: ")

print("TEST DATA")

lee.encodeStr("00010212")

hello_world = ["00010212","00110202","00211000","01011000","01111010","01201012",
                "02011102","02111010","02211020","10011000","10110201","10201020"]

for string in hello_world:
    print(string + " " + ''.join(lee.encodeStr(string)))

print("CSV DATA")

data = pd.read_csv(csv_path, sep=",", header=0,
    dtype={"template_ID":str,"match":int,"template":str,"strandC":str,"strandR":str,"strandR_len":int,"strandC_len":int,"template_align":str,"strand_align":str})

data["possiblehit"] = data.apply(lee.findpossiblehits,axis=1)

templates_to_decode = ['H01','H02','H03','H04','H05','H06','H07','H08','H09','H10','H11','H12']

for template in templates_to_decode: 
    lee.decoding(data,template)
