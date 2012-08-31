from datetime import datetime

from nose.tools import *
from cyrusbus import Bus

from spiking.signal import TimedSignal

def test_timed_signal():
  time = datetime.now()

  # Create a signal
  a = TimedSignal('<1,2>', time)

  # Check whether same values are maintained
  eq_(a.time, time, "Expected same time value!")
  eq_(a.neuron, '<1,2>', "Expected same neuron index!")

def test_timed_signal_with_eventbus():
  time = datetime.now()

  # Create a signal
  a = TimedSignal('<1,2>', time)

  b = Bus()
  
  def callback(bus, signal=None):
    eq_(signal.time, time, "Expected same time value!")
    eq_(signal.neuron, '<1,2>', "Expected same neuron index!")

  b.subscribe('Fired', callback)

  # Fire the signal
  b.publish('Fired', signal=a)

