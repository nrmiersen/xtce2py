"""Test package generation."""

from pathlib import Path

import xtce2py

xtce2py.generate(
    xtce_file=Path("/home/nrmiersen/xtce-generation/xtce_files/CONKSAT-1-XTCE.xml"),
    output_dir=Path("/home/nrmiersen/xtce2py_output/"),
    clean=True,
    verbose=True,
    log_file=Path("xtce2py.log"),
    log_level="DEBUG",
)

"""
pdm run xtce2py /home/nrmiersen/xtce-generation/xtce_files/CONKSAT-1-XTCE.xml ~/xtce2py_output/ -c -v --log-level DEBUG --log-file xtce2py.log
"""
