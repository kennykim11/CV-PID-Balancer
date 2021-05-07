import numpy as np
import cv2

cap = cv2.VideoCapture(0)
colors = {#'yellow': [((20, 55, 80), 35)],
          #'red': [((0, 120, 90), 20), ((160, 120, 90), 179)],
          'green': [((38, 120, 65), 90)]}
colors = {key: [np.array([value[0], [value[1], 255, 255]], dtype="uint8") for value in ranges] for key, ranges in colors.items()}

def numpify(*args):
    return np.array(args, dtype="uint8")

def output_text(string, frame, y):
    cv2.putText(frame,
                string,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                2)

def find_colors(color_ranges, frame, hsv):
    mask = sum([cv2.inRange(hsv, *color_range) for color_range in color_ranges])

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    if cnts:
        return max(cnts, key=cv2.contourArea)
    return None

def show_largest_contour(frame, hsv):
    largest_contours = {name: find_colors(color_values, frame, hsv) for name, color_values in colors.items()}
    largest_contours = dict(filter(lambda elem: elem[1] is not None, largest_contours.items()))

    if largest_contours:
        max_color = max(largest_contours, key=lambda name: cv2.contourArea(largest_contours[name]))

        x,y,w,h = cv2.boundingRect(largest_contours[max_color])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 2)
        center_x = x+w/2
        center_y = y+h/2

        # Display the resulting frame
        output_text(max_color, frame, 20)
        output_text(f'x:{center_x}, y:{center_y}', frame, 50)
        return center_x, center_y
    return None, None

def gen_ball_x(window_title):
    cv2.namedWindow(window_title)

    while True:
        # Capture frame-by-frame
        ret_bool, frame = cap.read()
        #print(cap.get(cv2.CAP_PROP_FPS))

        # Our operations on the frame come here
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        center_x, _ = show_largest_contour(frame, hsv)

        cv2.imshow(window_title, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if center_x:
            yield center_x

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    for i in gen_ball_x('J'):
        ...