import pygame

STRIP_FORWARD = 0
STRIP_BACKWARD = 1
STRIP_PINGPONG = 2
STRIP_REVPONG = 3


class Sequence(object):
    """Container class for list generating methods.
        These lists are used by the BaseStrip class to
        determine the order in which to display
        a list of frames.
    """

    @staticmethod
    def forward(start, end):
        return [x for x in range(start, end)]

    @staticmethod
    def backward(start, end):
        return [x for x in range(start - 1, end - 1, -1)]

    @staticmethod
    def ping_pong(start, end):
        seq = Sequence.forward(start, end)
        _ = [seq.append(x) for x in range(end - 2, start, -1)]
        return seq

    @staticmethod
    def reverse_pong(start, end):
        seq = Sequence.backward(start, end)
        _ = [seq.append(x) for x in range(end + 1, start - 1)]
        return seq

    @staticmethod
    def get_sequence(start, end, order):
        if not order in range(STRIP_REVPONG + 1):
            raise ValueError

        if order == STRIP_FORWARD:
            seq = Sequence.forward(start, end)
        elif order == STRIP_BACKWARD:
            seq = Sequence.backward(end, start)
        elif order == STRIP_PINGPONG:
            seq = Sequence.ping_pong(start, end)
        else:
            seq = Sequence.reverse_pong(end, start)

        return seq


class BaseStrip(object):
    """
        The BaseStrip class is used to handle the sequencing
        of frames(images) in an animation as well as 
        repetitions and frame timing.
        This is a unittest ready conceptual version of 
        Strip class.

        @self._num_frames           = int, number of frames in current strip

        @self._current_frame        = int, current frame index 

        @self._frame_order          = int, used to get Sequence object. Valid 
                                      values are given by STRIP_* constants.

        @self._done                 = boolean, sentinal to determine whether to continue 
                                      iterating through frames
        
        @self._sequence             = Sequence, sequence object to determine order
                                      in which to traverse frames
        
        @self._len_sequence         = int, length of sequence

        @self._repeat               = int, determine the number of times to repeat 
                                      a set of frames

        @self._repeat_counter       = int, counts number of times a set of frames 
                                      has been iterated through

        @self._elapsed              = time that has elapsed, used to determine
                                      when to go to next frame 
        
    """

    def __init__(self, num_frames, frame_order=STRIP_FORWARD, repeat=0,
                 strip_timing=[0]):

        # validate values
        assert num_frames > 0, \
            'num_frames < 1'
        assert frame_order in range(STRIP_REVPONG + 1), \
            'traversal type out of range'
        assert int(repeat) > -2, \
            'repeat must be < -1'

        self._num_frames = num_frames
        self._current_frame = 0
        self._frame_order = frame_order
        self._done = False
        self._sequence = Sequence.get_sequence(0, num_frames, frame_order)
        self._len_sequence = len(self._sequence)
        self._repeat = repeat
        self._repeat_counter = 0
        self.set_strip_timing(strip_timing)
        self._elapsed = 0

    def next(self, dt=0):
        """return the next frame index"""
        n = self._sequence[self._current_frame]

        """if timing on"""
        if self._strip_timing[n] > 0:
            """return current frame and not next frame if enough time has not passed"""
            if dt - self._elapsed < self._strip_timing[n]:
                return n
            self._elapsed = dt

        _slen = self._len_sequence
        _repeat = self._repeat
        self._current_frame += 1
        if self._current_frame >= _slen:
            if self._repeat == 0 or \
                    (self._repeat_counter >= _repeat and _repeat != -1):
                self._done = True
                self._current_frame -= 1
            else:
                self._repeat_counter += 1
            self._current_frame = 0

        return n

    def set_strip_timing(self, strip_timing):
        """set timing for entire strip"""
        num_frames = self._num_frames
        try:
            list(strip_timing)
            size = len(strip_timing)
            assert size > 0, 'strip_timing expects float or float list'
            if size > num_frames:
                frame_timing = strip_timing[:num_frames]
            elif size < num_frames:
                strip_timing += [0 for _ in range(num_frames - size)]
        except:
            val = strip_timing
            strip_timing = [val for _ in range(num_frames)]
        self._strip_timing = strip_timing
        self._elapsed = 0

    def set_frame_timing(self, frame, val):
        """
            Set timing for individual frame in strip,
            automatically resets frame_timer.
        """
        if frame in range(self._num_frames):
            self._frame_timing[frame] = val
            self._elapsed = 0

    def set_order(self, order):
        """Set frame order of strip"""
        self._sequence = Sequence.get_sequence(0, self._num_frames, order)
        self._frame_order = order

    def reset(self):
        """reset the strip"""
        self._current_frame = 0
        self._repeat_counter = 0
        self._done = False
        self._elapsed = 0

    def is_done(self):
        return self._done


class Strip(BaseStrip):
    """
        Similar to BaseStrip except it stores actual list of 
        sprite images(frames) 
    """

    def __init__(self, frames, frame_order=STRIP_FORWARD, repeat=0,
                 strip_timing=0):
        frames = list(frames)
        assert isinstance(frames[0], pygame.Surface), \
            'Expected list of pygame.Surface objects'

        super(Strip, self).__init__(len(frames), \
                                    frame_order, repeat, strip_timing=strip_timing)
        self._frames = frames

    def next(self, t):
        """Return next frame in Strip"""
        return self._frames[super(Strip, self).next(t)]


# #######################################################################
## Unit Testing                                                       ##
########################################################################        
if __name__ == '__main__':

    import unittest
    import time

    class UnitTestBaseStrip(unittest.TestCase):

        def setUp(self):
            pass

        def test_sequence_values(self):

            s = BaseStrip(4, frame_order=STRIP_FORWARD)
            self.assertEqual(s._sequence, \
                             [0, 1, 2, 3])
            s = BaseStrip(4, frame_order=STRIP_BACKWARD)
            self.assertEqual(s._sequence, \
                             [3, 2, 1, 0])
            s = BaseStrip(4, frame_order=STRIP_PINGPONG)
            self.assertEqual(s._sequence, \
                             [0, 1, 2, 3, 2, 1])
            s = BaseStrip(4, frame_order=STRIP_REVPONG)
            self.assertEqual(s._sequence, \
                             [3, 2, 1, 0, 1, 2])

        def repetition_helper(self, s):
            result = []
            while not s.is_done():
                result.append(s.next())
            expect = s._sequence * (s._repeat + 1)
            return result, expect

        def test_forward_repetition(self):
            s = BaseStrip(4, frame_order=STRIP_FORWARD, repeat=1)
            self.assertEqual(*self.repetition_helper(s))

        def test_backward_repetition(self):
            s = BaseStrip(4, frame_order=STRIP_BACKWARD, repeat=1)
            self.assertEqual(*self.repetition_helper(s))

        def test_ping_pong_repetition(self):
            s = BaseStrip(4, frame_order=STRIP_PINGPONG, repeat=1)
            self.assertEqual(*self.repetition_helper(s))

        def test_reverse_pong_repetition(self):
            s = BaseStrip(4, frame_order=STRIP_REVPONG, repeat=1)
            self.assertEqual(*self.repetition_helper(s))


        def test_reset(self):
            s = BaseStrip(4)
            s.next()
            s.next()
            self.assertTrue(s._current_frame > 0)
            s.reset()
            self.assertEqual(s._current_frame, 0)

        def test_infinite_repeat(self):
            s = BaseStrip(3, repeat=-1)  #sequence is [0,1,2]
            for i in range(3):
                s.next()
            self.assertEqual(s.next(), 0)
            self.assertTrue(not s.is_done())

        def test_order_resettings(self):
            s = BaseStrip(4, frame_order=STRIP_BACKWARD)
            s.set_order(STRIP_FORWARD)
            self.assertEqual(s._sequence, \
                             [0, 1, 2, 3])

            s = BaseStrip(4, frame_order=STRIP_FORWARD)
            s.set_order(STRIP_BACKWARD)
            self.assertEqual(s._sequence, \
                             [3, 2, 1, 0])

            s = BaseStrip(4, frame_order=STRIP_FORWARD)
            s.set_order(STRIP_PINGPONG)
            self.assertEqual(s._sequence, \
                             [0, 1, 2, 3, 2, 1])

            s = BaseStrip(4, frame_order=STRIP_FORWARD)
            s.set_order(STRIP_REVPONG)
            self.assertEqual(s._sequence, \
                             [3, 2, 1, 0, 1, 2])

        def test_timing(self):
            t = 2
            s = BaseStrip(3, strip_timing=t)
            self.assertEqual([t, t, t], s._strip_timing)
            before = time.time()
            s.next(before)
            after = time.time()
            self.assertTrue(after - before < t)
            self.assertEqual(s._current_frame, 1)
            time.sleep(t)
            s.next(time.time())
            after = time.time()
            self.assertTrue(after - before >= t)
            self.assertEqual(s._current_frame, 2)
            before = time.time()
            s.next(before)
            s.next(before)
            after = time.time()
            self.assertTrue(after - before < t)
            self.assertEqual(s._current_frame, 2)


            ########################################################################

    unittest.main()
    ######################################################################## 

    # s = BaseStrip(4, frame_order=BaseStrip.STRIP_PINGPONG)
    # s2 = BaseStrip(4, frame_order=BaseStrip.STRIP_REVPONG)
    # print('pingpong(0,4):', s._sequence)
    # print('revpong(4,0) :', s2._sequence)

    
