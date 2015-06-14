
Changelog
=========

0.2.0 (2015-06-14)
-----------------------------------------

* changed DEFAULT behavior in test config loader to correspond to Montague 0.2.0. This is a breaking change.
* added support for logging_config
* Removed bundled fakeapp egg in favor of montague_testapps.
* Removed zope interfaces to correspond to the next version of Montague.

0.1.0 (2014-11-12)
-----------------------------------------

* First release on PyPI, corresponding to PasteDeploy 1.5.2.
* Backwards incompatibility: ConfigMiddleware no longer offers a threadlocal ``CONFIG`` importable. (This removes the dependency on Paste.)
