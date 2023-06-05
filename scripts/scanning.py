import db, register
import cv2, time, sqlite3

def scan():
    """
    A loop where you scan qr code and update the data base 
    """

    conn = sqlite3.connect('database.db')

    # Open the camera and read the frame
    cap = cv2.VideoCapture(0)
    
    while True:
        _, frame = cap.read()
        cv2.imshow('Qr Code Reader', frame)

        detect = cv2.QRCodeDetector()

        try: # try to read the qr code, if not, continue the loop (has potential error)
            value, _, _ = detect.detectAndDecode(frame)
        except:
            continue

        # if the value is read and it is not empty, update the database
        if len(value) > 0:
            val = value 
            vis_id = register.get_vis(val).id

            db.update(connection=conn, id=vis_id)
            print("Qr code has been read.")
            
            time.sleep(1.0)

        # if q is pressed, break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            register.scanning_in_progress = False
            break
        
       
    cap.release()
    cv2.destroyAllWindows() 