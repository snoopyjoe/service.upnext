# -*- coding: utf-8 -*-
# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, unicode_literals
from xbmc import getCondVisibility, Player, Monitor
from api import Api
from state import State


class UpNextPlayer(Player):
    """Service class for playback monitoring"""

    def __init__(self):
        self.api = Api()
        self.state = State()
        Player.__init__(self)

    def set_last_file(self, filename):
        self.state.last_file = filename

    def get_last_file(self):
        return self.state.last_file

    def is_tracking(self):
        return self.state.track

    def disable_tracking(self):
        self.state.track = False

    def reset_queue(self):
        if self.state.queued:
            self.api.reset_queue()
            self.state.queued = False
            if not self.state.playing_next and not self.state.track:
                self.stop()

    if callable(getattr(Player, 'onAVStarted', None)):
        def onAVStarted(self):  # pylint: disable=invalid-name
            """Will be called when Kodi has a video or audiostream"""
            if not getCondVisibility('videoplayer.content(episodes)'):
                return
            self.state.track = True
            self.reset_queue()
    else:
        def onPlayBackStarted(self):  # pylint: disable=invalid-name
            """Will be called when kodi starts playing a file"""
            self.state.starting = True
            monitor = Monitor()
            while not monitor.abortRequested():
                if self.isPlaying() and self.getTotalTime():
                    break
                if not self.state.starting:
                    return
                monitor.waitForAbort(1)
            if not getCondVisibility('videoplayer.content(episodes)'):
                return
            self.state.track = True
            self.reset_queue()

    def onPlayBackPaused(self):  # pylint: disable=invalid-name
        self.state.pause = True

    def onPlayBackResumed(self):  # pylint: disable=invalid-name
        self.state.pause = False

    def onPlayBackStopped(self):  # pylint: disable=invalid-name
        """Will be called when user stops playing a file"""
        self.reset_queue()
        self.api.reset_addon_data()
        self.state = State()  # Reset state

    def onPlayBackEnded(self):  # pylint: disable=invalid-name
        """Will be called when Kodi has ended playing a file"""
        self.reset_queue()
        if not self.state.playing_next:
            self.api.reset_addon_data()
            self.state = State()  # Reset state

    def onPlayBackError(self):  # pylint: disable=invalid-name
        """Will be called when when playback stops due to an error"""
        self.reset_queue()
        self.api.reset_addon_data()
        self.state = State()  # Reset state
