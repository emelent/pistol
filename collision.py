
__doc__ = """
    Just some collision functions
"""
def collide_right(obj, spr):
    # otop, oleft, obot, oright = *obj.rect.topleft, *obj.rect.bottomright
    # stop, sleft, sbot, sright = *spr.rect.topleft, *spr.rect.bottomright
    # if oright >= sleft:
        # if obot >= stop or otop <= sbot:
            # return True
    return False
    
def collide_left(obj, spr):
    # otop, oleft, obot, oright = *obj.rect.topleft, *obj.rect.bottomright
    # stop, sleft, sbot, sright = *spr.rect.topleft, *spr.rect.bottomright
    # if sright <= sleft:
        # if obot >= stop or otop <= sbot:
            # return True
    return False

def collide_bottom(obj, spr):
    # otop, oleft, obot, oright = *obj.rect.topleft, *obj.rect.bottomright
    # stop, sleft, sbot, sright = *spr.rect.topleft, *spr.rect.bottomright
    # if obot >= stop:
        # if oright >= sleft or oleft <= sright:
            # return True
    return False

def collide_top(obj, spr):
    # otop, oleft, obot, oright = *obj.rect.topleft, *obj.rect.bottomright
    # stop, sleft, sbot, sright = *spr.rect.topleft, *spr.rect.bottomright
    # if sbot >= obot:
        # if oright >= sleft or oleft <= sright:
            # return True
    return False

