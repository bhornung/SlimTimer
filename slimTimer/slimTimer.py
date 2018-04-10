import time

import numpy as np

class SlimTimer():
    """
    Bare to bones timer utlity
    """
    def __init__(self, n_runs = 10):
        """
        Creates an instance of the timer.
        Parameters:
          n_runs (int) : number of runs with a set of parameters.
        """
        self.n_runs = n_runs
        self._set_runtimes()
        self.__hasrun = False

    @property 
    def tmean(self):
      if self.__hasrun:
        return self._tmean
      else:
        raise ValueError("Cannot report unmesured times.")

    @property
    def tstdev(self): 
      if self.__hasrun:
        return self._tstdev
      else:
        raise ValueError("Cannot report unmesured times.")

    @property
    def run_times(self):
      """
      np.ndarray of type np.float to store the run times.
      """
      if self.__hasrun:
        return self._run_times
      else:
        raise ValueError("Cannot report unmesured times.")

    def measure(self):
        """
        Performs n_runs runs. Calculates the mean run time and its standard deviation.
        """
# --- perform repeated runs
        for i_run in range(self.n_runs):
          print("Run {0} / {1} ...".format(i_run, self.n_runs), end = '')
          tdelta = self._timed_execute()
          self._run_times[i_run] = tdelta
          print()

# calculate mean
        self._tmean = np.mean(self._run_times)
# calculate standard deviation
        self._tstdev = np.std(self._run_times)
# allow acces to results
        self.__hasrun = True

    def set_func_args(self, *args, **kwargs):
        """
        Sets the parameters of the function to be timed.
        """
        self._func_args = args 
        self._func_kw_args = kwargs

    def set_func(self, func):
        """
        Sets the function to be timed.
        Parameters:
          func (callable) : function to be timed
        """
        self._func = func

    def set_n_runs(self, n_runs):
      """
      Sets the number of runs.
      Parameters:
        n_runs (int) : number of runs
      """
      if not isinstance(n_runs, type) or n_runs < 1:
        raise ValueError("'n_runs' must be a positive integer.")

      self.n_runs = n_runs
# reset measurement results
      self._set_runtimes()
      self._tmean = np.nan
      self._tstdev = np.nan
# block acces to results
      self.__hasrun = False

    def to_dict(self):
      """
      Returns the individual, mean and error of the timings as a dictionary.
      """

      res_dict = {'runtimes' : self.run_times,
                  'tmean' : self.tmean,
                  'tstdev' : self.tstdev}

      return res_dict

    def _set_runtimes(self):
      """
      Sets the array to store the run times.
      """
      self._run_times =np.zeros(self.n_runs, dtype = np.float)

    def _timed_execute(self):
        """
        Executes function once.
        Returns:
          tdelta (float) : time needed to execute the function.
        """
        tstart = time.perf_counter()
        self._func(*self._func_args, **self._func_kw_args)
        tend = time.perf_counter() 

        tdelta = tend - tstart

        return tdelta

