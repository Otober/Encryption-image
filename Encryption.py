import cv2
import numpy as np

cap1 = cv2.VideoCapture("/home/kimdoyoung/Downloads/videoplayback1.mp4")
cap2 = cv2.VideoCapture("/home/kimdoyoung/Downloads/videoplayback2.mp4")

print(int(cap1.get(cv2.CAP_PROP_FRAME_COUNT)))
print(int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH)))
print(int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print(cap1.get(cv2.CAP_PROP_FPS))

print("\n")
print(int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)))
print(int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH)))
print(int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print(cap2.get(cv2.CAP_PROP_FPS))

key1 = np.random.randint(0, 256, size=(360, 640, 3),  dtype=np.uint8)
key2 = key1

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fps = 60.0
out = cv2.VideoWriter("/home/kimdoyoung/Downloads/Result.mp4",
                      fourcc, fps, frameSize=(1920, 720))

while True:
    ret1, img1 = cap1.read()
    ret2, img2 = cap2.read()
    if ret1 and ret2:
        img1 = cv2.resize(img1, dsize=(640, 360),
                          interpolation=cv2.INTER_LINEAR)
        img2 = cv2.resize(img2, dsize=(640, 360),
                          interpolation=cv2.INTER_LINEAR)

        Encryption_img1 = cv2.bitwise_xor(img1, key2)
        Encryption_img2 = cv2.bitwise_xor(img2, key1)

        Decryption_img1 = cv2.bitwise_xor(Encryption_img1, key2)
        Decryption_img2 = cv2.bitwise_xor(Encryption_img2, key1)

        '''
        cv2.imshow("Result1", img1)
        cv2.imshow("Result2", img2)

        cv2.imshow("Encryption Result1", Encryption_img1)
        cv2.imshow("Encryption Result2", Encryption_img2)

        cv2.imshow("Decryption Result1", Decryption_img1)
        cv2.imshow("Decryption Result2", Decryption_img2)

        '''

        first_img = cv2.hconcat([img1, Encryption_img1, Decryption_img1])
        second_img = cv2.hconcat([img2, Encryption_img2, Decryption_img2])

        full_img = cv2.vconcat([first_img, second_img])
        #cv2.imshow("Full_img", full_img)
        out.write(full_img)
        key2 = Encryption_img1
        key1 = Encryption_img2

    else:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
cap1.release()
cap2.release()
cv2.destroyAllWindows()
