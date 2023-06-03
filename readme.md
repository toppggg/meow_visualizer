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