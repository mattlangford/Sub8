#!/usr/bin/env python
import cv2
import numpy as np
from sub8_tools import text_effects

# Image providers ==============
from image_providers import RandomColors

image_providers = [RandomColors] 

# Tools ====================
from tools import PaintBrushTool

tools = [PaintBrushTool]


'''
A main interface for various labeling tools.
'''

p = text_effects.Printer()
# General Labeler interface ===================================================

class LabelerInterface():
    '''Provides tools to create polygon segments'''
    def __init__(self, *args, **kwargs):
        blank = np.zeros(shape=(480, 640))
        self._draw_data = {'image': blank, 'mask': blank, 'overlay': blank}

        self._reserved_keys = {'q': 'quit', 's': 'save'}

        # Maps shortcut keys to tools
        self.tools = self._generate_hotkeys(tools)
        self.active_tool = self.tools.values()[0]

        self._name = "tool"
        cv2.namedWindow(self._name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self._name, self._mouse_cb)

    def _generate_hotkeys(self, tools):
        ''' Make hotkeys for each tool. Make sure each tool class has a unique name '''
        if len(tools) == 0:
            print p.red("No tools found!\n")
            exit()

        hotkeys = {}
        for tool in tools:
            name = tool.name
            letter_index = 0
            letter = name[letter_index]
            while letter in hotkeys.keys() and \
                  letter not in self._reserved_keys:
                letter_index += 1
                letter = name[letter_index]
            else:
                # Too many tools, generate random letter
                name = 'abcdefghijklmnopqrstuvwxyz'
                letter_index = 0
                letter = name[letter_index]
                while letter in hotkeys.keys() and \
                      letter not in self._reserved_keys:
                    letter_index += 1
                    letter = name[letter_index]

            hotkeys[letter] = tool(self._draw_data)

        return hotkeys
    
    def _mouse_cb(self, *args, **kwargs):
        ''' Handles drawing and what not '''
        self.active_tool.mouse_cb(*args, **kwargs)

    def _apply_layers_to_image(self, layers, image):
        _disp_img = np.copy(image).astype(np.uint32)
        for layer in layers:
            if len(layer.shape) == 2:
                # Meaning it's a one channel image
                layer = np.dstack((layer, layer, layer))

            _disp_img += layer.astype(np.uint32)

        _disp_img = np.clip(_disp_img, 0, 255).astype(np.uint8)
        return _disp_img

    def _print_options(self):
        print p.text("The current active tool is the ").bold(self.active_tool.name).text(":")
        self.active_tool.print_options()

        print p.text("\nGeneral controls are as follows:")
        print p.bold('\t[s] : ').text("skip")
        print p.bold('\t[q] : ').text("quit")

    def start_labeling(self, image_provider):
        self._print_options()

        key = None

        mask_opacity = 0.3
        overlay_opacity = 0.9
        while key is not 'q':
            if key == 's':
                continue

            image = image_provider.get_next_image()
            self._draw_data['image'] = image

            if key not in self._reserved_keys:
                self.active_tool.key_press(key)

            layers = [self.active_tool.mask * mask_opacity, 
                      self.active_tool.overlay * overlay_opacity]
            cv2.imshow(self._name, self._apply_layers_to_image(layers, self.active_tool.image)) 
            key = chr(cv2.waitKey(10) & 0xFF)
            if key in self.tools.keys():
                self.active_tool = self.tools[key]
                print p.text("Set active tool to: ").bold(self.active_tool.name)

# =============================================================================

def _menu_options(options, name=None):
    ''' Returns the object associated with user selected entry
        options := list of objects with a 'name' field
    '''
    title = p.text("Please select from the following")
    title += ":" if name is None else p.bold(" {}:".format(name))
    print title

    numbers = []
    index = 1
    for class_type in options:
        _number = p.bold("  [{}] :".format(index))
        _option = p.text(class_type.name)

        print _number, _option
        numbers.append(class_type)
        index += 1
    
    while True:
        try:
            # All options are displayed, wait for user input
            selection = int(raw_input("\nSelect from the above options: "))
            res = numbers[selection - 1]

        except KeyboardInterrupt:
            print
            exit()

        except:
            # There was some kind of error in the input
            print p.red("\nPlease enter a number between 1 and {}".format(len(options)))

        else:
            # Valid input
            break

    print "=" * 50
    return res()

if __name__ == "__main__":

    print p.bold("\nWelcome to the image tool!")

    image_provider = _menu_options(image_providers, "image providers")
    labeler = LabelerInterface()
    labeler.start_labeling(image_provider)


