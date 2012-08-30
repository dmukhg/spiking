from nose.tools import eq_
from datetime import datetime

from spiking.signal import TimedSignal

def test_timed_signal():
  time = datetime.now()

  # Create a signal
  a = TimedSignal('<1,2>', time)

  # Check whether same values are maintained
  eq_(a.time, time, "Expected same time value!")
  eq_(a.neuron, '<1,2>', "Expected same neuron index!")
