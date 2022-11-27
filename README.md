
# Basis-Finder
This !should! be a tool to find a basis for a vector space of a field with arbitrary operations - no guarantees, though

## Usage
### Running the program
You need to have python 3.7 installed (at least). You can then run the program by typing 

    python3 LinearDependence.py

in a cli of your choice (make sure that you have added python to your path and that you are in the folder that you cloned the script to).
You will then be prompted to enter one of the presets (feel free to create your own). The real numbers are the default field, simply leave the input empty and press enter.

### Changing the Matrix
Simply changing the variable `to_test` to a `nxn` matrix changes the matrix that is checked.

### Changing the operations
The primary reason for the creation of this program is that I am not aware of a free (as in: also open-source), easy to use program that can handle arbitrary operations in arbitrary fields. At the top  of the file, you will find different methods, each labeled according to their functionality. Changing the definition of `addition`, for example, changes the way that addition in the field is calculated. Just make sure that your operations satisfy the [field axioms](https://en.wikipedia.org/wiki/Field_%28mathematics%29#Classic_definition).
