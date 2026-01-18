import cv2

def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)


    if not cap.isOpened():
        print("X Camera not accessible")
        return

    while True:
        ret,frame=cap.read()
        if not ret:
            print("X Failed to grab frame")
            break

        cv2.imshow("Day1 - Webcam",frame)

        if cv2.waitKey(1) &0xFF==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()


            