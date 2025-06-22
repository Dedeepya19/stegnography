#Least significant bit
import numpy as np # numerical operations and array manipulations
import cv2 # image processing
import matplotlib.pyplot as plt # visualization

# dictionaries for ascii to char and char to ascii
d = {chr(i): i for i in range(255)}
c = {i: chr(i) for i in range(255)}

#message and encryption key
text = input("Text: ")
key = input("Key: ")

#reading the image
x = cv2.imread('blue_car.jpg')
# for visualization converting into bgr to rgb
x_rgb = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
plt.imshow(x_rgb)
plt.axis('off')
plt.title('Original Image')
plt.show()

# Encryption 

#copying the original image
x_enc = x.copy()
n = 0 #row index
m = 0 #column index
z = 0 #color channel index
l = len(text) # length of the text to be embedded
kl = 0 # key index

#iterate over the text
for i in range(l):
    #applying xor between text and key ascii values
    char_val = d[text[i]] ^ d[key[kl]]
    #iterate over 8 bits of char_val
    for bit_pos in range(8):
        #shift right for accessing the least significant bit
        bit = (char_val >> (7-bit_pos)) & 1
        org_val = x_enc[n,m,z]
        x_enc[n,m,z] = np.uint8((org_val & 0XFE ) | bit) # 0XFE is 11111110 in binary 
        print(f"Embedding bit {bit} of '{text[i]}'at ({n}, {m}, {z}) original = {org_val} new = {x_enc[n,m,z]}")
        z = (z + 1) % 3
        if z == 0:
            m = m + 1
            if m == x_enc.shape[1]:
                m = 0
                n = n + 1
kl = (kl + 1) % len(key)

#saving the encrypted image
cv2.imwrite("encrypted_car.jpg", x_enc)
#visualization
rgb_enc = cv2.cvtColor(x_enc, cv2.COLOR_BGR2RGB)
plt.imshow(rgb_enc)
plt.axis('off')
plt.title('After Embedding')
plt.show()
 
#Decryption
n,m,z = 0, 0, 0
kl = 0
# new string for decrypted text
decrypt = ''
for i in range(l):
    val = 0
    for bit_pos in range(8):
        bit = x_enc[n,m,z] & 1
        # shift left 
        val = (val << 1) | bit
        print(f"Reading bit {bit} from ({n}, {m}, {z})") 
        z = (z + 1) % 3
        if z == 0:
            m = m + 1
            if m == x_enc.shape[1]:
                m = 0
                n = n + 1
    #xor with ascii of key and value
    orig_char = c[val ^ d[key[kl]]]
    decrypt += orig_char 
    print(f"Decrypted byte: {val} XOR {d[key[kl]]} = {val ^ d[key[kl]]} -> '{orig_char}'")
kl = (kl + 1)  % len(key)
#printing the decrypted text
print("Decrypted text: ", decrypt)