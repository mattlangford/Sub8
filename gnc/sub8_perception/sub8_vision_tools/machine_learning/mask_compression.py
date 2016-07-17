import numpy as np
import cv2
import os
import argparse
import sys
import tqdm

def encode(img, fname):
    '''
    White and black refer to pixles where the mask is true and false respectivly.
    Instead of storing a png file - store an array with the start and end of 'strides' of white pixles.
    '''
    flat_img = img.flatten()
    in_stride = False
    stride_start = 0
    strides = [img.shape]
    for i in range(len(flat_img)):
        if flat_img[i] != 0:
            if in_stride:
                continue
            else:
                stride_start = i
                in_stride = True
        else:
            if in_stride:
                strides.append([stride_start, i])
                in_stride = False

    strides = np.array(strides).astype(np.uint32)
    #print 'Compressed: {} bytes ({})'.format(sys.getsizeof(strides), strides.dtype)
    strides.dump(fname)

def decode(fname, real_mask=None):
    '''
    If `real_mask` is not none, decode will return true if the decoded np mask is the same as `real_mask`.
    '''
    comp_img = np.load(fname)
    img = np.zeros(shape=np.multiply(*comp_img[0]), dtype=np.uint8)

    for stride in comp_img[1:]:
        img[stride[0]: stride[1]] = 255

    img = img.reshape(comp_img[0])

    if real_mask is not None and (img == real_mask).all():
        #print "All Match"
        return True

    return img

def compress_batch(path, output):
    if path[-1] != '/': path += '/'
    if output[-1] != '/': output += '/'

    images = os.listdir(path)
    observation_list = []
    label_list = []

    print "Masks found in folder: {}".format(len(images) / 2 - 1)
    count = 0
    for i in tqdm.trange(len(images) / 2 - 1, desc="Loading images", unit=' images'):
        try:
            if '_mask.png' in images[i]:
                # This is the mask image - there should be a matching non mask image.
                image_name = images[images.index(images[i].replace('_mask', ''))]
                mask_name = images[i]

                mask = cv2.imread(path + images[i], 0)
                images.remove(image_name)
            else:
                # This is the real image - there should be a matching mask image.
                mask_name = images[images.index(images[i].replace('.png', '_mask.png'))]

                mask = cv2.imread(path + mask_name, 0)
                images.remove(mask_name)

            encode(mask, output + mask_name.replace('.png', '.np'))
            if decode(output + mask_name.replace('.png', '.np'), mask) is not True:
                print "COMPRESSION NOT MATCHING FOR {}".format(mask_name)

        except KeyboardInterrupt:
            return None

        except:
            print "There was an issue with loading an image. Skipping it..."

    return observation_list, label_list

if __name__ == '__main__':
    usage_msg = ("Convert png masks to compressed files.")
    desc_msg = "Useful for sending abunch of masks to AWS."

    parser = argparse.ArgumentParser(usage=usage_msg, description=desc_msg)
    parser.add_argument(dest='path',
                        help="Pass the path to a folder with images inside it.")
    parser.add_argument(dest='output',
                        help="Pass the path to a folder to save the compressions to.")

    args = parser.parse_args(sys.argv[1:])

    compress_batch(args.path, args.output)