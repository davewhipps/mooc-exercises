from typing import Tuple

import numpy as np


def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    return get_motor_left_matrix_fear(shape)


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    return get_motor_right_matrix_fear(shape)

# FEAR
def get_motor_left_matrix_fear(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    res[0:shape[0], 0:int(shape[1]/2)] = 1
    return res

def get_motor_right_matrix_fear(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    res[0:shape[0], int(shape[1]/2 +1):shape[1]] = 1
    return res

# EXPLORER
def get_motor_left_matrix_explorer(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    res[0:shape[0], int(shape[1]/2 +1):shape[1]] = -1
    return res

def get_motor_right_matrix_explorer(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    res[0:shape[0], 0:int(shape[1]/2)] = -1
    return res

# MODIFIED EXPLORER
def get_motor_left_matrix_explorer_2(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    res[0:shape[0], int(shape[1]/2 +1):shape[1]] = -1
    res[0:shape[0], 0:int(shape[1]/2)] = 0.5
    return res

def get_motor_right_matrix_explorer_2(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    res[0:shape[0], 0:int(shape[1]/2)] = -1
    res[0:shape[0], int(shape[1]/2 +1):shape[1]] = 0.5
    return res