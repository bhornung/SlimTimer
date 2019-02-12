import time

import numpy as np

class SlimTimer():
    """
    Bare to bones timer utlity

    Attributes
       self.func (callable) : function to time
       self.n_runs (int) : number of runs with a set of parameters.
       self.tag (str) : string to tag the timer
       self.verbosity (int) : output verbosity level

       self.runtimes (np.ndarray) : list of run times
       self.tmean (float) : mean run time
       self.tstdev (float) : standard deviation of run times

    Methods:
      measure() : runs the function self.n_runs times

      set_func_args(*args, **kwargs) : sets the function arguments. Make sure *args are passed in the right order.

      to_dict(with_tag = False) : export the public attributes to a dict. 
        Parameters:
          with_tag (bool) : add tag to dict keys. Default False.
        Returns :
          res_dict = {'[self.tag_]runtimes' : self.run_times,
                      '[self.tag_]tmean' : self.tmean,
                      '[self.tag_]tstdev' : self.tstdev}
    """
    def __init__(self,  func = None, n_runs = 10, tag = "", verbosity = 0):
        """
        Creates an instance of the timer.
        Parameters:
          func (callable) : function to time
          n_runs (int) : number of runs with a set of parameters.
          tag (str) : string to tag the timer
          verbosity (int) : output verbosity level
        """

        # add function
        if not callable(func):
            raise ValueError("func must be callable")
        else:
            self._set_func(func)

        # set number of runs
        self._set_n_runs(n_runs)

        # set function arguments
        self._func_args = []
        self._func_kwargs = {}

        # initialise timer
        self._set_runtimes()
        self.__hasrun = False

        # add tag
        if tag == "":
            self.tag = func.__name__
        else:
            self.tag = str(tag)

        self.verbosity = verbosity

    @property
    def run_times(self):
        """
        np.ndarray of type np.float to store the run times.
        """
        if self.__hasrun:
            return self._run_times
        else:
            raise ValueError("Cannot report unmeasured times.")

    @property 
    def tmean(self):
        if self.__hasrun:
            return self._tmean
        else:
            raise ValueError("Cannot report unmeasured times.")

    @property
    def tstdev(self): 
        if self.__hasrun:
            return self._tstdev
        else:
            raise ValueError("Cannot report unmeasured times.")

    def measure(self):
        """
        Performs n_runs runs. Calculates the mean run time and its standard deviation.
        """
        # --- perform repeated runs
        for i_run in range(self.n_runs):
            if self.verbosity > 0:
                print("Run {0} / {1} ...".format(i_run, self.n_runs), end = '')
            tdelta = self._timed_execute()
            self._run_times[i_run] = tdelta
			
            if self.verbosity == 2:
                print(tdelta)
            
        # calculate mean
        self._tmean = np.mean(self._run_times)
        # calculate standard deviation
        self._tstdev = np.std(self._run_times)
        # allow access to results
        self.__hasrun = True

    def set_func_args(self, *args, **kwargs):
        """
        Sets the parameters of the function to be timed.
        """
        self._func_args = args 
        self._func_kw_args = kwargs

    def _set_func(self, func):
        """
        Sets the function to be timed.
        Parameters:
          func (callable) : function to be timed
        """
        if callable(func):
            self._func = func
        else:
            raise TypeError("'func should be callable'")

    def to_dict(self, with_tag = False):
      """
      Returns the individual, mean and error of the timings as a dictionary.
      Parameters:
        with_tag (bool) : tag the dictionary with the timer's tag. Default False.
      """

      res_dict = {'runtimes' : self.run_times,
                  'tmean' : self.tmean,
                  'tstdev' : self.tstdev}

      if with_tag:
          res_dict = {"{0}_{1}".format(self.tag, _k) : _v for _k, _v in res_dict.items()}

      return res_dict

    def _set_n_runs(self, n_runs):
        """
        Sets the number of runs.
        Parameters:
          n_runs (int) : number of runs
        """
        if not isinstance(n_runs, int) or n_runs < 1:
            raise ValueError("'n_runs' must be a positive integer.")
        
        self.n_runs = n_runs
        # reset measurement results
        self._set_runtimes()
        self._tmean = np.nan
        self._tstdev = np.nan
        # block access to results
        self.__hasrun = False

    def _set_runtimes(self):
        """
        Sets the array to store the run times.
        """
        self._run_times =np.zeros(self.n_runs, dtype = np.float)
        
    def _timed_execute(self):
        """
        Executes the function once.
        Returns:
          tdelta (float) : time needed to execute the function.
        """
        tstart = time.perf_counter()
        self._func(*self._func_args, **self._func_kwargs)
        tend = time.perf_counter() 

        tdelta = tend - tstart

        return tdelta
