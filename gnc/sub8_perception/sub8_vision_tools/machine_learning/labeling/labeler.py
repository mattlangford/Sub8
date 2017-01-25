#!/bin/usr/env python
import cv2
import numpy as np
from sub8_tools import text_effects


image_providers = {'test': "test", 'test2': "test2"}
p = text_effects.Printer()


'''
A main interface for various labeling tools.
'''

# Base Classes ================================================================

class BaseImageProvider(object):
    '''Classes that provide image sources. Examples may include:
        - A bag crawler
        - A video crawler
        - Loading images from a folder
    '''
    def load_image(self, *args, **kwargs):
        ''' Load images from source '''
        pass

    def get_next_image(self):
        ''' Returns the next image in the sequence '''
        pass


class BaseLabeler(object):
    '''Used by the LabelerInterface to eaisly switch between different labelers.
    '''
    def __init__(self, draw_data):
        # Stores data used by this class. Do not interact directly with or things could break
        self._draw_data = draw_data

    @property
    def image(self):
        ''' Gets the current image being segmeneted '''
        return self._draw_data.get('image', None)

    @property
    def mask(self):
        ''' Gets the current mask for this segmentation '''
        return self._draw_data.get('mask', None)

    @mask.setter
    def mask(self, mask):
        ''' Sets the current mask for this segmentation '''
        self._draw_data['mask'] = mask

    @property
    def overlay(self):
        ''' Gets the current overlay for this segmentation '''
        return self._draw_data['overlay']
    
    @overlay.setter
    def overlay(self, overlay):
        ''' Sets the current overlay for this segmentation '''
        self._draw_data['overlay'] = overlay

    def set_active(self):
        ''' Method called when this labeler is now the active one '''
        self.overlay = np.zeros(shape=self.image.shape)

    def mouse_cb(self, event, x, y, flags, param):
        ''' cv2 callback to be called for this labeler when it is active '''
        pass


# General Labeler interface ===================================================

class LabelerInterface():
    '''Provides tools to create polygon segments'''
    def __init__(self, *args, **kwargs):
        blank = np.zeros(shape=(480, 640))
        self._draw_data = {'image': blank, 'mask': blank, 'overlay': blank}

        # Maps shortcut keys to labelers
        self._labelers = {'b': BaseLabeler}
        self._active_labeler = None

        self._name = "labeler"
        cv2.namedWindow(self._name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self._name, self._mouse_cb)
    
    def _mouse_cb(self, event, x, y, flags, param):
        ''' Handles drawing and what not '''
        print "cb" 

    def _apply_layers(self, layers):
        _disp_img = np.copy(self.image)
        for layer in layers
            _disp_img += layer

        return _disp_img

    def _print_options()

    def start_labelling(self):
        key = None
        if self._active_labeler is None:

            return

        while key is not ord('q'):
             
            cv2.imshow() 
            key = cv2.waitKey(10) & 0xFF

# =============================================================================

def _menu_options(options, name=None):
    ''' Returns the object associated with user selected entry
        options := dict that maps object name => object
    '''
    title = p.text("Please select from the following")
    title += ":" if name is None else p.bold(" {}:".format(name))
    print title

    numbers = [None]
    index = 1
    for option, class_type in options.items():
        numbers.append(class_type)
        
        _number = p.bold("  [{}] :".format(index))
        _option = p.text(option)

        print _number, _option
        index += 1
    
    while True:
        try:
            # All options are displayed, wait for user input
            selection = int(raw_input("\nSelect from the above options: "))
            res = numbers[selection]

        except KeyboardInterrupt:
            print
            exit()

        except:
            # There was some kind of error in the input
            print p.red("\nPlease enter a number between 1 and {}".format(len(numbers) - 1))

        else:
            # Valid input
            break
    print "=" * 50
    return res

if __name__ == "__main__":

    print p.bold("\nWelcome to the image labeler!")

    image_provider = _menu_options(image_providers, "image providers")
