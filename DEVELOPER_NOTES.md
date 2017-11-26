# Developer Notes
The goal of this documentation is to keep track of various development notes of the project.

## Dependent Libraries
The following libraries are being used by our appliation.

```bash
pip install py-moneyed               # Money decimal datatype and currency handling library.
pip install py-mortgagekit           # Mortgage calculator library.
pip install numpy                    # Mathematical and scientific calculations and functions library.
pip install --pre xhtml2pdf          # library for converting HTML into PDFs using ReportLab.
```
### Library Notes:
#### xhtml2pdf
* It appears if you are running ``MacOS`` and you attempt to install this library then you might get an error.
* Please follow [the instructions](https://pillow.readthedocs.io/en/latest/installation.html) on how handle any OS specific errors when installing.
