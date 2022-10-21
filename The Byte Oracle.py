import requests
import json
import codecs
import sys
from binascii import hexlify
#IV for last ciphertext block is the previous ciphertext block Pi = DK(Ci) ⊕ Ci-1
#refer https://flast101.github.io/padding-oracle-attack-explained/

json_data = '{"ciphertext": "d6c88784f890d6a24c5bf2f090c0aec7","iv": "36a01e3bfa0d7a5b8a89631405bf4db9"}'
python_obj = json.loads(json_data)
b = json.dumps(python_obj)

string_ct = python_obj["iv"]

list_ct = list(string_ct)

my_list = [
  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e',
  'f'
]

Valid_Padding = 'Valid'
Invalid_Padding = 'Invalid'

i = 1  #change starting index accordingly

while (i >= 0):

  for j in my_list:
    for p in my_list:
      list_ct[i] = j
      list_ct[i - 1] = p
      print(j, end="")  #sending these hex
      print(p, end="")  #values as modified Ciphertext
      temp_ct = "".join(list_ct)
      r = requests.post('https://ineedrandom.com/paddingoracle',
                        json={
                          "ciphertext": "d6c88784f890d6a24c5bf2f090c0aec7",
                          "iv": temp_ct
                        })
      print("\n")
      print(temp_ct)
      #above statement prints c1||c2||c3 remove# to activate
      print("\n")
      print(r.text)
      #print("\n")
      if str(r.text) == "\"Valid\"":

        print(p, end="")
        print(j, end="")
        print("\n")
        sys.exit("Valid Pad-byte generated")
        exit()

  i = i - 1

#the program will output the ith byte of X, where x[i] is the
#IV or ciphertext that should be XOred with P’1[i] and Cj-1[i] to get the
# corresponding plaintext byte.
# Reference: https://flast101.github.io/padding-oracle-attack-explained/
#X[i+1] = P’1[i+1] ⊕ Cj-1[i+1] ⊕ Pj[i+1] = 0x02 ⊕ Cj-1[i+1] ⊕ Pj[i+1]
#where Cj-1[i+1] and Pj[i+1] are known.
#Pj[i] = P’1[i] ⊕ Cj-1[i] ⊕ X[i] = 0x02 ⊕ Cj-1[i] ⊕ X[i]
#where X[i] is the byte that satisfied the requirements of PKCS7.
#
#For example, for getting the first byte (modify 16th byte of IV)
#X = 10101010101010101010101010101010
#IV= 26d1634eca6a0222fcff1f6d7bc87ddd
#P' = 00616d652077686966666c696e672074
#then Plaintext byte =  10 (from X) XOR 26 (from IV) XOR output byte from Program
