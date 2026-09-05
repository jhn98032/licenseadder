# licenseadder
A script for adding license header and license files to a C/C++ source project.

The script will look for c/cpp files and header files and add license headers at the top of the files.
The license file will also be added to the project.

Example usage:

```bash
./licenseadder.py --project myproject --dir myproject_dir --license lgpl3  \
                  --author "Johan Henriksson johan[a]dexar.se" --name "example"
```

# Adding licenses

To add a new license add a file called "licenses/<LICENSE_NAME>-header.txt" with the text that should 
be added to the top of a source file. 
Also add the actual license text in a file called "licenses/<LICENSE_NAME>-"<LICENSE_NAME>-file-<NAME_OF_FILE>".

For example BSD have two files bsd-header.txt and bsd-file-LICENSE.
The script will look for available licensed by checking files in licenses.

All files can have parameters embraced in '{' '}' that will be replaced with actual text. 
For example '{year}' will be replaced with current year.

The parameters are:
- *project*  = Project name
- *year*     = Current year
- *author_name* = Authors name
- *program_name* = Name of the progrm
- *program_desc* = Description of the program



