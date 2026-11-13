""" Rate limiting: how many requests one visitor may make per minute (used by the chat bubble)

Adapted from Open Coding Society flask's throttled() in api/authorize.py. OCS limits logged-in accounts by
their user id; the chat bubble is public, so here each visitor is identified by their IP address instead.

How it works (a "sliding window"): for each visitor we keep a list of the times of their recent requests.
On every new request, times older than WINDOW_SECONDS are dropped; if LIMIT are left, the request is refused.

Limits of this approach (also in the README):
- One IP is not always one person: a school or office network can share one IP, so a busy classroom could hit
  the limit together, and one person can dodge it by switching networks (e.g. Wi-Fi to phone data).
- The counts live in this server's memory, so they reset when the server restarts and are not shared between
  processes. That is fine here because the Dockerfile runs a single gunicorn worker.
"""
import threading
import time
from collections import deque


LIMIT = 10           # requests allowed per visitor...
WINDOW_SECONDS = 60  # ...in this many seconds

# visitor id -> times of their recent requests (oldest first). A deque is a list that is fast to remove
# from the front, which is where the oldest times are.
_recent = {}
# gunicorn runs 4 threads (see Dockerfile), so two requests can arrive at once; the lock stops them
# from editing _recent at the same moment
_lock = threading.Lock()


def seconds_until_allowed(visitor, now=None):
    """ Record one request from visitor and return 0 if it is allowed, or the whole seconds they must wait.

    Parameter: visitor, any string that identifies one visitor (their IP address).
    now is only passed in by tests, so they can pretend time has passed without waiting.
    """
    now = time.monotonic() if now is None else now  # monotonic: a clock that never jumps when the system time changes
    with _lock:
        times = _recent.setdefault(visitor, deque())
        # Forget requests that are older than the window
        while times and now - times[0] >= WINDOW_SECONDS:
            times.popleft()
        if len(times) >= LIMIT:
            # Wait until the oldest request in the window expires
            return int(WINDOW_SECONDS - (now - times[0])) + 1
        times.append(now)
        # Same clean-up as OCS: forget visitors who have gone quiet, so memory does not grow forever
        if len(_recent) > 1000:
            for key in [k for k, v in _recent.items() if not v or now - v[-1] >= WINDOW_SECONDS]:
                del _recent[key]
    return 0
