#!/usr/bin/env python
# coding: utf-8

# In[117]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your DeltaPhi function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK

import cv2
import numpy as np

def get_steer_matrix_left_lane_markings(shape):
    """
        Args:
            shape: The shape of the steer matrix (tuple of ints)
        Return:
            steer_matrix_left_lane: The steering (angular rate) matrix for Braitenberg-like control 
                                    using the masked left lane markings (numpy.ndarray)
    """
    
    steer_matrix_left_lane = np.zeros(shape)
    steer_matrix_left_lane[:,0:int(shape[1]/2.0)] = -1

    return steer_matrix_left_lane

# In[118]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your DeltaPhi function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK


def get_steer_matrix_right_lane_markings(shape):
    """
        Args:
            shape: The shape of the steer matrix (tuple of ints)
        Return:
            steer_matrix_right_lane: The steering (angular rate) matrix for Braitenberg-like control 
                                     using the masked right lane markings (numpy.ndarray)
    """
    
    steer_matrix_right_lane = np.zeros(shape)
    steer_matrix_right_lane[:,int(shape[1]/2.0):shape[1]] = 1

    return steer_matrix_right_lane

# In[249]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your DeltaPhi function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK

import cv2
import numpy as np


def detect_lane_markings(image):
    """
        Args:
            image: An image from the robot's camera in the BGR color space (numpy.ndarray)
        Return:
            left_masked_img:   Masked image for the dashed-yellow line (numpy.ndarray)
            right_masked_img:  Masked image for the solid-white line (numpy.ndarray)
    """
    is_simulator = False
 
    sigma = 2
    horizon_percent = 0.0
    threshold = 50
    white_lower_hsv = np.array([(0)*179, (0)*255, (35/100)*255])
    white_upper_hsv = np.array([(260/360)*179, (20/100)*255, (100/100)*255])
    yellow_lower_hsv = np.array([(40/360)*179, (45/100)*255, (45/100)*255])
    yellow_upper_hsv = np.array([(60/360)*179, (100/100)*255, (90/100)*255])

    #Many of the above dont work well for the simulated images
    if is_simulator:
        horizon_percent = 0.0
        sigma = 1
        threshold = 30
        white_upper_hsv = np.array([(360/360)*179, (20/100)*255, (100/100)*255])
        yellow_lower_hsv = np.array([(45/360)*179, (30/100)*255, (50/100)*255])
        yellow_upper_hsv = np.array([(70/360)*179, (100/100)*255, (90/100)*255])

    h, w, _ = image.shape
    # OpenCV uses BGR by default, whereas matplotlib uses RGB, so we generate an RGB version for the sake of visualization
    imgrgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert the image to HSV for any color-based filtering
    imghsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Most of our operations will be performed on the grayscale version
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # This is not needed in this solution
    mask_ground = np.ones(img.shape, dtype=np.uint8)
    #mask_ground[:int(horizon_percent*img.shape[0])][:] = 0
    
    # Smooth the image using a Gaussian kernel
    img_gaussian_filter = cv2.GaussianBlur(img,(0,0), sigma)

    # Convolve the image with the Sobel operator (filter) to compute the numerical derivatives in the x and y directions
    sobelx = cv2.Sobel(img_gaussian_filter,cv2.CV_64F,1,0)
    sobely = cv2.Sobel(img_gaussian_filter,cv2.CV_64F,0,1)

    # Let's create masks for the left- and right-halves of the image
    mask_left = np.ones(sobelx.shape)
    mask_left[:,int(np.floor(w/2)):w + 1] = 0
    mask_right = np.ones(sobelx.shape)
    mask_right[:,0:int(np.floor(w/2))] = 0

    # Compute the magnitude of the gradients
    Gmag = np.sqrt(sobelx*sobelx + sobely*sobely)

    # Compute the orientation of the gradients
    Gdir = cv2.phase(np.array(sobelx, np.float32), np.array(sobely, dtype=np.float32), angleInDegrees=True)
    
    # TODO: Is this really a good value for the threshold?
    mask_mag = (Gmag > threshold)

    mask_white = cv2.inRange(imghsv, white_lower_hsv, white_upper_hsv)
    mask_yellow = cv2.inRange(imghsv, yellow_lower_hsv, yellow_upper_hsv)
 
    # In the left-half image, we are interested in the right-half of the dashed yellow line, which corresponds to negative x- and y-derivatives
    # In the right-half image, we are interested in the left-half of the solid white line, which correspons to a positive x-derivative and a negative y-derivative
    # Generate a mask that identifies pixels based on the sign of their x-derivative
    mask_sobelx_pos = (sobelx > 0)
    mask_sobelx_neg = (sobelx < 0)
    mask_sobely_pos = (sobely > 0)
    mask_sobely_neg = (sobely < 0)
    
    # Let's generate the complete set of masks, including those based on color
    mask_left_edge = mask_ground * mask_left * mask_mag * mask_sobelx_neg * mask_sobely_neg * mask_yellow
    mask_right_edge = mask_ground * mask_right * mask_mag * mask_sobelx_pos * mask_sobely_neg * mask_white
    
    # Duckiebot needs a little extra power!
    left_multiplier = 100
    right_multiplier = 100
    if is_simulator:
        left_multiplier = 1
        right_multiplier = 1       
    
    return (mask_left_edge*left_multiplier, mask_right_edge*right_multiplier)
