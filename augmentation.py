def order_points_old(pts):
    import numpy as np
    # initialize a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
 
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
 
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
 
    # return the ordered coordinates
    return rect

def affine(im,pts,imfn,i,w,h):
    import numpy as np
    import cv2
    bbox = [[pts[0],pts[1]],[pts[2],pts[3]],[pts[4],pts[5]],[pts[6],pts[7]]]
    rect = order_points_old(np.array(bbox))
    #print(rect)
    if rect[1][1]  < rect[0][1] and abs(rect[1][1] - rect[0][1])> 100:
        
        rect[[0,1,2,3],:] = rect[[1,2,3,0],:]
    pts1 = np.float32([rect[0], rect[1], rect[2]])
    #print(rect)
    #w=32
    #h=320
    #pts1 = np.float32([bbox[most_left_idx], bbox[(most_left_idx+1)%4], bbox[(most_left_idx+2)%4]])
    pts2 = np.float32([[0,0], [w-1,0], [w-1, h-1]])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(im, M, (w, h))
    #cv2.imwrite("tmp/{}_{}.jpg".format(imfn,i),dst)
    return dst
