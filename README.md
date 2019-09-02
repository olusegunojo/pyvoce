# pyvoce

A [hurriedly-built] python wrapper for voce, a java voice synthesis and recognition library... well.. plus SourceSeparation added using nussl... and a flask app to test it too.

The file is contained in pyvoce.py. It is a wrapper around voce using py4j.

Voce itself uses static functions, however, pyvoce requires that the library be instantiated. This could be problematic as you should not be able to create two instances, since the actual voce class is initialised with certain configuration settings.

Just an exercise at using py4j.
