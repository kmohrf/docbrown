# docbrown

*docbrown* is an empirical progress library. It determines the overall 
duration and progression of a process by looking at the time it took in the past.

*docbrown* might be an option for you, if you have one long running task
which parts take very different amounts of time. It is also helpful when used
in environments where you can’t inform consumers about the progress of a task
out-of-band (like a WSGI request/response cycle vs a WebSocket). 

## Example Usage

Record progress:
```python
import time
from docbrown import record_progress

with record_progress('process_name', ident='my_ident') as record:
    # outputs "my_ident", but normally would return a 
    # unique id if not set manually
    print(record.ident)
    # do some stuff that takes time
    record('loading_data')
    time.sleep(4)
    record('calculating_matrices')
    time.sleep(9)
    record('rendering_structures')
    time.sleep(23)
    record('uploading_models')
    time.sleep(15)
```

As *docbrown* determines progression by looking at the past every process needs
to run at least once before. The following `get_progress` call will therefore only
work if you’ve executed the code above at least once!

Get the progression of our process in another process:
```python
from docbrown import get_progress
print(get_progress('my_ident'))
```

## Future

There are some things that would be nice, but have not been implemented yet.

* additional storage backends apart from SQLite
* configurable strategy for aggregating phase durations apart from 
  the simple arithmetic average like median
* code path detection that takes optional phases into account and
  updates the expected duration and progres on-the-fly  