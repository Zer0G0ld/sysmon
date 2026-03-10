from .battery import read as battery_read
from .telephony import read as telephony_read
from .memory import read as memory_read
from .storage import read as storage_read
from .cpu import read as cpu_read
from .location import read as location_read

__all__ = ['battery', 'telephony', 'memory', 'storage', 'cpu', 'location']

# Create module-level functions
battery = type('battery', (), {'read': staticmethod(battery_read)})()
telephony = type('telephony', (), {'read': staticmethod(telephony_read)})()
memory = type('memory', (), {'read': staticmethod(memory_read)})()
storage = type('storage', (), {'read': staticmethod(storage_read)})()
cpu = type('cpu', (), {'read': staticmethod(cpu_read)})()
location = type('location', (), {'read': staticmethod(location_read)})()