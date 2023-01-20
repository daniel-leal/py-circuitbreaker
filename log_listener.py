import logging

from pybreaker import CircuitBreakerListener


class LogListener(CircuitBreakerListener):
    """Listener used by circuit breakers that execute api operations"""

    def state_change(self, cb, old_state, new_state):
        """Called when the circuit breaker `cb` state changes."""
        if old_state is not None:
            print("")
            logging.info(f"State changed old: {old_state.name.upper()}, new: {new_state.name.upper()}\n")