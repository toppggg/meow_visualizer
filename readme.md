## Add visualizer path
In order to run the visualizer the path has to be added to the visualizer in order for the meow imports to work, for the integration testing of meow_base

This can be done in wsl/linux with:

    nano ~/.bashrc

add the following line to the end of the file:

    export PYTHONPATH=$PYTHONPATH:/full/path/to/meow_visualizer/
save and exit

then run:

    source ~/.bashrc

## Testing
In order to run tests: the following code can be run on unix:
python -m unittest discover ./visualizer/test_visualizer/

### Tests outside of unittest
In the /visualizer/test_visualizer/ folder, several of the files are intended to test performance, these can be run individually with "python ./'file name', e.g. "./run_hours_for_hours.py". This starts a runner with a gui which is run on a local server, the IP is printed when running the program.
Since the server is intended to run continuously, there is no graceful closure in this implementation, so "ctrl + d" or "ctrl + c" shuts down the visualizer.