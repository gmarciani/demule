from queue import PriorityQueue
import logging

# Configure logger
logger = logging.getLogger(__name__)


class NextEventCalendar:
    """
    Implementation of a simple Next-Event calendar.
    Notice that the calendar internally manages:
        (i) event sorting, by occurrence time.
        (ii) scheduling of only possible events, that are:
            (ii.i) possible arrivals, i.e. arrivals with occurrence time lower than stop time.
            (ii.ii) departures of possible arrivals.
        (iii) unscheduling of events to ignore.
    """

    def __init__(self, t_clock=0.0, t_stop=float("inf"), arrival_types=set()):
        """
        Create a new *NextEventCalendar*.
        :param t_clock: (float) optional, initialization time for the simulation clock.
        :param t_stop: (float) optional, initialization time for the simulation clock. Default is infinite.
        :param arrival_types: ([EventType]) optional, arrival event types. Default is the empty set.
        """
        self._clock = t_clock  # the simulation clock
        self._stop = t_stop  # the stop time
        self._arrival_types = arrival_types  # the set of arrival event types

        self._events = PriorityQueue()  # the event list, implemented as a priority queue
        self._ignore = set()  # the set of events to ignore (unscheduled events), processed lazily

    def get_clock(self):
        """
        Retrieves the calendar clock.
        :return: (float) the calendar clock.
        """
        return self._clock

    def set_clock(self, time):
        """
        Set the calendar clock.
        :param time: (float) time to set the calendar clock to.
        """
        self._clock = time

    def schedule(self, ev):
        """
        Schedule an event.
        :param ev: (SimpleEvent) the event to schedule.
        :return: (boolean) True, if the event has been scheduled; False, otherwise.
        """
        if ev.type in self._arrival_types and ev.time >= self._stop:
            logger.debug("Not scheduled (impossibile): {}".format(ev))
            return False
        else:
            self._events.put((ev.time, ev))
            logger.debug("Scheduled: {}".format(ev))
            return True

    def unschedule(self, *events):
        """
        Unschedule events.
        :param events: (SimpleEvent) the events to unschedule.
        """
        for ev in events:
            self._ignore.add(ev)
            logger.debug("Unscheduled: {}".format(ev))

    def get_next_event(self):
        """
        Retrieve the next scheduled event and update the clock.
        :return: (SimpleEvent) the next event, if present; None, otherwise.
        """
        if self._events.empty():
            logger.debug("Event queue is empty, next event is None")
            return None
        else:
            candidate = self._events.get()[1]
            while candidate in self._ignore:
                self._ignore.discard(candidate)
                candidate = self._events.get()[1]
                logger.debug("Ignoring next event (unscheduled): {}".format(candidate))
            self.set_clock(candidate.time)
            return candidate

    def empty(self):
        """
        Check if the calendar is empty.
        :return: True, if the calendar is empty; False, otherwise.
        """
        return self._events.empty()

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Calendar({}:{})".format(id(self), ", ".join(sb))