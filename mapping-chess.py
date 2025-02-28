import cv2
import numpy as np

def map_chess_squares_realtime():
    cap = cv2.VideoCapture(0)

    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        result = frame.copy()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)
        
        if ret:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            
            cv2.drawChessboardCorners(result, (7, 7), corners, ret)
            
            x_coords = corners[:, 0, 0]
            y_coords = corners[:, 0, 1]
            min_x, max_x = min(x_coords), max(x_coords)
            min_y, max_y = min(y_coords), max(y_coords)
            
            square_size_x = (max_x - min_x) / 6
            square_size_y = (max_y - min_y) / 6
            
            top_left_x = min_x - square_size_x
            top_left_y = min_y - square_size_y
            
            for i in range(8):
                for j in range(8):
                    x1 = int(top_left_x + j * square_size_x)
                    y1 = int(top_left_y + i * square_size_y)
                    x2 = int(x1 + square_size_x)
                    y2 = int(y1 + square_size_y)
                    
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    
                    notation = files[j] + ranks[i]
                    
                    cv2.rectangle(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(result, notation, (center_x - 10, center_y + 5), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        cv2.imshow('Real-time Chess Board Mapping', result)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def map_chess_squares_simple_grid():
    """
    Alternative approach that divides the camera view into a simple 8x8 grid
    without attempting to detect an actual chessboard.
    """
    cap = cv2.VideoCapture(0)
    
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        height, width = frame.shape[:2]
        
        square_h, square_w = height // 8, width // 8
        
        result = frame.copy()
        
        for i in range(8):
            for j in range(8):
                y1 = i * square_h
                x1 = j * square_w
                y2 = y1 + square_h
                x2 = x1 + square_w
                
                center_x = x1 + square_w // 2
                center_y = y1 + square_h // 2
                
                notation = files[j] + ranks[i]
                
                cv2.rectangle(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(result, notation, (center_x - 10, center_y + 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        cv2.imshow('Simple Grid Chess Board Mapping', result)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    print("Select mapping mode:")
    print("1: Chessboard detection (requires a physical chessboard)")
    print("2: Simple grid division (works with any camera view)")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        map_chess_squares_realtime()
    else:
        map_chess_squares_simple_grid()

if __name__ == "__main__":
    main()