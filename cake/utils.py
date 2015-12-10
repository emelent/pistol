import pygame

def slice_hsurf(surf, width, height=0, startx=0, starty=0):
    """Slice a given surface horizontally into equally sized subsurfaces,
    returning a list of images"""
   
    surf_w, surf_h = surf.get_size()
    assert startx < surf_w and startx >= 0,\
            'Invalid startx value'
    assert starty < surf_h and starty >= 0,\
            'Invalid starty value'
    height = height if height != 0 else surf_h
    slices = []
    for i in range((surf_w - startx) // width):
       slices.append(surf.subsurface((startx + width * i, starty, width, height)))

    return slices

def slice_msurf(surf, width, height=0, startx=0, starty=0):
    """Slice a given surface into equally sized subsurfaces, this
       function returns a matrix of subsurfaces(represented as 2d list)"""
    surf_w, surf_h = surf.get_size()
    assert startx < surf_w and startx >= 0,\
            'Invalid startx value'
    assert starty < surf_h and starty >= 0,\
            'Invalid starty value'
    slices = []
    for i in range(surf_h // height):
        row = surf.subsurface((startx, starty + height * i,surf_w,height))
        slices.append(slice_hsurf(row, width, height))
    return slices

def rotate_center(img, angle):
    """Rotate square image while keeping its center"""
    orig_rect = img.get_rect()
    rot_image = pygame.transform.rotate(img, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def rotate_center2(image, rect, angle):
    """rotate an image of any dimension while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

def flip_images(images, x, y):
    """flip list of images"""
    flipped = [pygame.transform.flip(img, x, y) for img in images]
    return flipped
