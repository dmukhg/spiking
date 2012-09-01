"""
The :mod:`neuron` module provides neurons for use within networks.
"""

from cyrusbus import Bus
from datetime import datetime

from spiking.signal import TimedSignal

__all__ = (
  'SpikingNeuron',
  'NEURON_FIRE_EVENT_KEY',
  'NEURON_ACTIVATION_LEVEL'
)

NEURON_FIRE_EVENT_KEY = "FIRED"
NEURON_ACTIVATION_LEVEL = 1

class SpikingNeuron(object):
  def __init__(self, index, network_bus, 
      efficacy_pause=2,
      efficacy_duration=4, 
      arp=2,
      threshold=1.5):
    """
    A :class:`SpikingNeuron` object is created with the bus for the
    current network as an argument.  It communicates with the network
    solely through this bus.

    Neurons have their own event buses to which they broadcast their
    firings.  To attach neurons to this bus, simply call the attach
    method on the pre-synaptic neuron passing the post-synaptic neuron
    as an argument.

    The firing of a neuron is contained within a :class:'TimedSignal'
    object.
    """
    self._network_bus = network_bus
    self._firing_bus  = Bus()
    self._index       = index

    # Internal plumbing
    self._activation_signals = []
    self._firing_times       = []

    # Neuron parameters
    self._efficacy_pause = efficacy_pause
    self._efficacy_duration = efficacy_duration
    self._arp = arp
    self._threshold = threshold

  def get_index(self):
    """ Returns the index for this neuron. This should be an immutable
    property. As such, only the get method is implemented."""
    return self._index

  index = property(get_index)

  def _fire(self):
    """ 
    Private method.  Used to create a signal and to broadcast it to
    the private event bus of this neuron.
    """
    time = datetime.now()
    signal = TimedSignal(self.index, time)

    # Append the current firing time to the _firing_times
    self._firing_times.append(time)

    # Broadcast the signal
    self._firing_bus.publish(NEURON_FIRE_EVENT_KEY, signal)

  def attach(self, post_synaptic_neuron):
    """
    Attaches :obj:`post_synaptic_neuron` as a synaptic connection to
    which it will send signals.  This is managed by simply adding
    :obj:`post_synaptic_neuron`.activate() to the private event bus
    for this neuron.
    """
    self._firing_bus.subscribe(NEURON_FIRE_EVENT_KEY,
        post_synaptic_neuron.activate)
    return

  def activate(self, bus, signal=None):
    if signal is not None:
      # Add this activation to the _activation_signals list
      self._activation_signals.append(signal)

  def compute(self):
    """
    Computes the activation level at this time.  Considers the signals
    in :obj:`self._activation_signals`, reverse chronologically.  Only
    considers those signals which were fired less than
    :obj:`self._efficacy_duration` ago. Beyond this value, all
    activation levels due to those signals should be zero.

    Additional notes:  This implementation is based on a piecewise
    constant model as defined in 

    Maass, 1995 | Analog Computations on Networks of Spiking Neurons

    Type A
    """
    level = 0
    current_time = datetime.now()

    for signal in reversed(self._activation_signals):
      delta = current_time - signal.time
      delta = delta.seconds * 1000 + delta.microseconds * 0.001
      # Adjust to miliseconds

      if delta > self._efficacy_duration:
        # If the signal was fired more than self._efficacy_duration ms
        # ago, it and all the signals before it will have no effect on
        # the computation.
        break

      if delta < self._efficacy_duration and \
         delta > self._efficacy_pause:
           # Only consider if the signal has started having effects at
           # all.
           level += NEURON_ACTIVATION_LEVEL

    return level

  def touch(self):
    """
    Checks whether the current value of the activation is higher than
    the threshold.  If so, and the current time is more than the
    absolute refractory period since the last firing, neuron sends out
    a synapse.
    """
    if len(self._firing_times) != 0:
      # Makes sense to compute delta_t only if there have been firings
      current_time = datetime.now()
      delta = current_time - self._firing_times[-1] 
      delta = delta.seconds * 1000 + delta.microseconds * 0.001 

      if delta < self._arp: 
        # No point in computing the activation level if still in the
        # absolute refractory period
        return 

    activation_level = self.compute()

    if activation_level > self._threshold:
      self._fire()
