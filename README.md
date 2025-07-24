# AGROBIOTA SDK

This package contains the code for the Agrobiota Environment.

## Usage

The AGROBIOTA SDK simplifies the integration and transformation of AGROBIOTA data.
It is available for Python 3.12+ and can be installed using pip:

```bash
python3.12 -m pip install agrobiota-sdk
```

It can be used through a CLI or as a Python library.

### CLI

The AGROBIOTA SDK CLI can be used to convert data between formats and
perform other tasks. To do this, run the following command:

```bash
agb-sdk convert bioindex-to-tabular \ 
    --input-path input.json \ 
    --output-path output.xlsx
```

### Python

The AGROBIOTA SDK can also be used as a Python library. To do this,
import the SDK and use the available functions.

```python
from agb_sdk.core.use_cases import convert_bioindex_to_tabular

convert_bioindex_to_tabular(
    input_path="input.json",
    output_path="output.xlsx",
    resolve_taxonomies=True,
)
```

The library is constantly evolving and new features are being
added. If you have any suggestions or feedback, please open
an [issue](https://github.com/agrobiota/agrobiota-sdk/issues) or contact us
via email at [bioinfo@biotrop.com.br](mailto:bioinfo@biotrop.com.br).

---

This SDK was tested in Linux. It may work in other operating systems, but
this is not guaranteed. For windows, we recommend using WSL (Windows Subsystem
for Linux).
