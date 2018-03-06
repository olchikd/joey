Joey
====

Flexible and declarative tool for creating and evaluating machine learning models based on Scikit-learn.


Command-line utilities
----------------------

Training the model:

.. code-block:: console

    $ python play.py ./examples/model.json --d ./examples/data.json --o ./examples/model.dat


Predicting:

.. code-block:: console

    $ python predict.py ./examples/model.dat -d ./examples/predict.json
