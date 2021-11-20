#!/usr/bin/env python
# coding: utf-8

# In[1]:


def DT_TOKEN():
    # todo change this to your duckietown token
    dt_token = "dt1-3nT8KSoxVh4MguCnvrzYvqQE2NkKD3T4Q6ntzQ4Zs8A26vp-43dzqWFnWd8KBa1yev1g3UKnzVxZkkTbfXPvWTisG3h3ogB4eidQGPkPeLALgckidE"
    return dt_token

def MODEL_NAME():
    # todo change this to your model's name that you used to upload it on google colab.
    # if you didn't change it, it should be "yolov5"
    return "yolov5"

# In[3]:


def NUMBER_FRAMES_SKIPPED():
    # todo change this number to drop more frames
    # (must be a positive integer)
    return 0

# In[2]:


# `class` is the class of a prediction
def filter_by_classes(clas):
    # Right now, this returns True for every object's class
    # Change this to only return True for duckies!
    # In other words, returning False means that this prediction is ignored.
    return True
    if clas == 0:
        print("Duckie")
        return True
    else:
        print("NOT a Duckie")
        return False

# In[4]:


# `scor` is the confidence score of a prediction
def filter_by_scores(scor):
    # Right now, this returns True for every object's confidence
    # Change this to filter the scores, or not at all
    # (returning True for all of them might be the right thing to do!)
    return True
    if scor > 0.5:
        print("Confidence is high")
        return True
    else:
        print("Confidence is low, ignored")
        return False

# In[5]:


# `bbox` is the bounding box of a prediction, in xyxy format
# So it is of the shape (leftmost x pixel, topmost y pixel, rightmost x pixel, bottommost y pixel)
def filter_by_bboxes(bbox):
    # Like in the other cases, return False if the bbox should not be considered.
    return True
    IMAGE_SIZE = 416
    width = bbox[2]-bbox[0]
    height = bbox[3]-bbox[1]
    
    inUpperHalf = (bbox[3] < IMAGE_SIZE/2)
    inLeftThird = (bbox[2] < IMAGE_SIZE/3)
    inRightThird = (bbox[0] > IMAGE_SIZE*2/3)
    
    TOO_SMALL_FRACTION = 0.2 # about a fifth 
    widthTooSmall = width < (TOO_SMALL_FRACTION*IMAGE_SIZE)
    heightTooSmall = height < (TOO_SMALL_FRACTION*IMAGE_SIZE)

    if widthTooSmall and heightTooSmall:
        print("Too small or far. Disregard")
        return False
    elif inLeftThird and inUpperHalf:
        print("Too far to the left and up. Disregard")
        return False        
    elif inRightThird and inUpperHalf:
        print("Too far to the right and up. Disregard")
        return False   
    else:
        print("Found a duckie!")
        return True

