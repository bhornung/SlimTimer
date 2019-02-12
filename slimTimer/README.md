# SlimTimer

A bare bones timing utility.

## Usage

To measure the execution time of `my_func` function in ten runs create an instance of the timer:

```python
timer = SlimTimer(func = my_func)

```

Add any positional arguments and keyword arguments required by `myfunc`

```python
timer.set_func_args(*args, **kwargs)
```

Measure execution times of ten runs:
```python
timer.measure()
```

Access raw run times and their mean and standard deviation as a dictionary:
```python
timer.to_dict()
```

## Class description

```python
SlimTimer(func = None, n_runs = 10, tag = "", verbosity = 0):
```

Creates an instance of the timer.

Parameters:

   **func (callable)** : function to time
   **n_runs (int)** : number of runs with a set of parameters. Default: 10
   **tag (str)** : string to tag the timer. Default: "".
   **verbosity (int)** : output verbosity level. Levels: [0, 1, 2]. Deafult: 0.

### Attributes

  **func (callable)** : function to time
  **n_runs (int)** : number of runs with a set of parameters.
  **tag (str)** : string to tag the timer
  **verbosity (int)** : output verbosity level
  **runtimes (np.ndarray)** : list of run times
  **tmean (float)** : mean run time
  **tstdev (float)** : standard deviation of run times

### Methods

#### `measure()`

Times the function in **n_runs** repetitions.


#### `set_func_args(*args, **kwargs)`

Sets the function arguments. Make sure *args are passed in the right order.

Parameters

  **args** (iterable) : function positional arguments
  **kwargs** (dict) : function keyword arguments


#### `to_dict(with_tag = False)`

Returns the individual, mean and standard deviations of the timings as a dictionary.
      
Parameters
        
  **with_tag (bool)** : tag the dictionary with the timer's tag. Default: False.

Returns

  **res_dict (dict)** : dictionary of timing results

  ```python
  {
   '[tag_]runtimes' : run_times,
   '[tag_]tmean' : tmean,
   '[tag_]tstdev' : tstdev
   }
  ```

