# Padding-Oracle-Attack
#Cryptanalysis using the last byte oracle method
#Refer: https://flast101.github.io/padding-oracle-attack-explained/
#This program is made to output 1 byte at a time, in CBC mode the IV to the Nth ciphertext block
#is the previous (i.e N01th) ciphertext block. The ciphertext expansion is one block so for 
#getting the last plaintext block inject into the IV

#X[i+1] = P’1[i+1] ⊕ Cj-1[i+1] ⊕ Pj[i+1] = 0x02 ⊕ Cj-1[i+1] ⊕ Pj[i+1]
#where Cj-1[i+1] and Pj[i+1] are known.
#Pj[i] = P’1[i] ⊕ Cj-1[i] ⊕ X[i] = 0x02 ⊕ Cj-1[i] ⊕ X[i]
#where X[i] is the byte that satisfied the requirements of PKCS7.
  
#For example, for getting the first byte (modify 16th byte of IV)
#X = 10101010101010101010101010101010
#IV= 26d1634eca6a0222fcff1f6d7bc87ddd
#P' = 00616d652077686966666c696e672074
#then Plaintext byte =  10 (from X) XOR 26 (from IV) XOR output byte from Program
