"""
The :mod:`signal` module provides the very commonly used signal class.
"""

__all__ = (
  'TimedSignal',
)

class TimedSignal(object):
  def __init__(self, neuron_index, time):
    """
    :class:`TimedSignal` class contains a time attribute and the index
    of the neuron that fired the signal.  Both attributes are
    read-only.
    """
    self._neuron = neuron_index
    self._time   = time

  def get_time(self):
    return self._time

  time = property(get_time)

  def get_neuron(self):
    return self._neuron

  neuron = property(get_neuron)
