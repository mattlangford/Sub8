#!/bin/usr/env python
import cv2
import numpy as np
from sub8_tools import text_effects


image_providers = {'test': "test", 'test2': "test2"}
labelers = {'test': "test", 'test2': "test2"}


'''
A main interface for various labeling tools.
Below are a couple base classes to inherit from in order to provide the
    correct methods for this interface script to do it's magic.
'''

# Base Classes ================================================================

class BaseLabeler(object):
    '''
    Labeller classes should provide these methods. Exaples include:
        - Simple polygon labeler
        - Simple circle labeler
        - Paint brush labeler
    '''
    def set_image(self, img, pre_mask=None):
        ''' Load the image to be labeled 
            img       := numpy array of an image
            pre_mask  := numpy array of a pre loaded mask 
        '''
        self.image = img.astype(np.uint8)
        self.mask = pre_mask.astype(np.uint8)

    def start_labelling(self):
        '''Start the labeling process'''
        key = None
        while key is not ord('q'):
            # Do image canvas drawing and segmenting, breaking on 'q'
            key = cv2.waitKey(10) & 0xFF 


class BaseImageProvider(object):
    '''
    Classes that provide image sources. Examples may include:
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

# ==============================================================================

p = text_effects.Printer()

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
    labeler = _menu_options(labelers, "labelers")
