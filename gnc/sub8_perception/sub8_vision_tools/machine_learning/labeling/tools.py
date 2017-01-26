import numpy as np
import cv2

from sub8_tools import text_effects


p = text_effects.Printer()

class BaseTool(object):
    '''Used by the LabelerInterface to eaisly switch between different tools.
    '''
    name = "general tool"

    def init(self):
        ''' Set up any variables needed here '''
        pass

    def key_press(self, key):
        ''' Called when a non reserved key is pressed '''

    def print_options(self):
        ''' Print data like hotkeys or info '''
        pass

    def mouse_cb(self, event, x, y, flags, param):
        ''' cv2 callback to be called for this tool when it is active '''
        pass

    def set_active(self):
        ''' Method called when this tool is now the active one '''
        self.clear_overlay

    def clear_overlay(self):
        ''' Clear the current overlay '''
        self.overlay = np.zeros(shape=self.image.shape)

    def clear_mask(self):
        ''' Clear the current mask '''
        self.mask = np.zeros(shape=self.image.shape)

    def __init__(self, draw_data):
        ''' Use self.init instead of this function '''
        # Stores data used by this class. Do not interact directly with or things could break
        self._draw_data = draw_data
        self.init()

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


class PaintBrushTool(BaseTool):
    name = "paint brush tool"

    def init(self):
        self.size = 10
        self.last_x = -1
        self.last_y = -1

        self._cursor_color = (255, 255, 255)

    def print_options(self):
        print p.text("Click and drag to draw. Shift click and drag to erase.")
        print p.text("Hotkeys are as follows:")
        print p.bold("\t[ or ] : ").text("decrease or increase cursor size.")

    def key_press(self, key):
        if key == '[':
            self.size -= self.size ** 0.5
        if key == ']':
            self.size += self.size ** 0.5
        
        # Force a redraw
        if key in ['[', ']']:
            self.size = int(np.clip(self.size, 1, np.inf))
            self.clear_overlay()
            cv2.circle(self.overlay, (self.last_x, self.last_y), self.size, self._cursor_color, 2)

    def mouse_cb(self, event, x, y, flags, param, **kwargs):
        self.clear_overlay()
        cv2.circle(self.overlay, (x, y), self.size, self._cursor_color, 2)
        
        if flags == cv2.EVENT_FLAG_LBUTTON:
            cv2.circle(self.mask, (x, y), self.size, 255, -1)
            
        if flags == cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_FLAG_LBUTTON:
            cv2.circle(self.mask, (x, y), self.size, 0, -1)
            

        self.last_x = x
        self.last_y = y
