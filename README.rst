RNA_ODE
===================
Working paper. More background and information will be provided when the paper is ready.

This repository contains examples to use the library. See the python notebooks in the :code:`experiments` folder.

Import
--------------------

.. code-block:: python

    from VelocytoAnalysis import RNA_ODE

Basic Usage
-------------------------------
Given the static gene expression :code:`counts` and RNA velocity :code:`velocity`, we carry out several downstream single-cell analysis based on the ODE prediction. We recommend to use well annotated cellular states :code:`celltype` for better performance.

.. code-block:: python

    from VelocytoAnalysis import RNA_ODE

    rna_ode = RNA_ODE(counts, velocity, celltype)
    
    # Fit model
    model = rna_ode.build_model()

    # Predict Future Expressions
    path= rna_ode.ode_simulation()

    # Compute Lineages
    lineages = rna_ode.compute_lineages()
    
    # Compute GRN
    grn_scores = rna_ode.compute_grn_scores()


**Evaluation**: If true lineages :code:`lineages_true` or true GRN :code:`grn_true` is known, we provide metric functions to evaluate the results of RNA_ODE

.. code-block:: python

    # Correctness of lineage
    correctness = rna_ode.evaluate_lineage_correctness(lineages_true, lineages)
    
    # AUROC of GRN
    auroc = rna_ode.evaluate_grn_auroc(grn_true, grn_scores)

Optional Parameters
-------------------------------
**Model**: To build the model with function :code:`build_model`, people can choose from three different model types (parameter :code:`model_name`): linear regression :code:`'linear'`, lasso regression :code:`'lasso'` and random forest regression :code:`'rf'`. Other parameters of the model can be set as shown here:

.. code-block:: python

    from VelocytoAnalysis import RNA_ODE

    rna_ode = RNA_ODE(counts, velocity, celltype)
    
    # Linear Regression
    model = rna_ode.build_model(model_name='linear')
    # Lasso Regression with the weight for the L1 regulation term = 1
    model = rna_ode.build_model(model_name='lasso', lasso_alpha=1)
    # Random Forest with 10 trees and max depth of 10
    model = rna_ode.build_model(model_name='rf', n_estimators=10, max_depth=10)

