# Changelog

All notable changes to this project will be documented in this file.

## [0.0.7] - 2019-06
### Added:
- 
### Changed:
- There is now a ``msp_customers_get``and a ``operator_cusgtomers_get`` to support operator or partner customers respectively. Thereby ``customers_get``has been removed
- Better error handling for exceptions in execusion class.
- Printing only out something if there is anything to print out after execusion has happened.
- Handling invalid user/password and missing cookie better

## [0.0.6] - 2019-06
### Changed:
- Merged functions into one Class for easier creating new methods for vcoclient. Rather then having a function for each argparse, we have one Class taking care of it.
### Removed:
- Fixed warning issue with Pandas renaming syntax of index
- Removed memory footprint of variables
## [0.0.5] - 2019-06
### Added:
- Using getpass for ``--password`` to make it more secure.
- Adding os.env option for username (VCO_USER), password (VCO_PASS) and host (VCO_HOST) for easiness.
- Adding functionality to get row names only via ``--rows_name`` from results.
### Change:
- Handling hostname has changed and will raise exception if not given via os or input by user.
- Handling data structure more efficiently (e.g. unpacking only needed value from list)

## [0.0.4] - 2019-06
### Added:
- ``--search`` in edges_get for searching any value related to edges properties. Gives one a powerful method to extract/compare values between many edges.
### Changed:
- Method login and logout will not return True anymore but will just execute as is and will raise an exception otherwise.
        
## [0.0.3] - 2019-05 
### Added:
- Output of Pandas, JSON or CSV, will have the name of the Edge rather as a returned index. Simpler to read.
- ``--filters`` lets user to filter output more granular
- User can now define another enterprise ID rather then the default 1 
### Changed:
- ``--search`` changed to ``--name``in edges_get, reflecting really what is filtered

## [0.0.2] - 2019-05
### Added:
- README, Licences, and fixes bugs in vcoclient.py
## [0.0.1] - 2019-05
- First versions


