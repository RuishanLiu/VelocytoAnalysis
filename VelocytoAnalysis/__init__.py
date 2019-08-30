from .GRN import *
from .lineage import *
from .model import *
from .mst import *
from .ode import *

class RNA_ODE(object):
    '''
    RNA_ODE: 
    Given the static gene expression x and RNA velocity v, 
    we model the v as a function of x.
    The dynamics of the gene expression is modeled by 
    the ordinary differential equation (ODE) as dx/dt=v(x), 
    where t is the underlying temporal variable.
    
    Four types of downstream single-cell analysis are built 
    based on the fitted model and the ODE predictions.
    1. single-cell Trajectory Inference
    2. pseudo-time inference
    3. influential gene analysis
    4. gene regulatory networks inference
    '''
    
    def __init__(self, counts, velocity, celltype):
        self.counts = counts
        self.velocity = velocity
        self.celltype = celltype
        self.model = None
        self.path = None
        self.lineage = None
        
    def build_model(self, genes=None, tfs=None, model_name='rf', n_estimators=10, max_depth=10, lasso_alpha=1, train_size=0.7):
        self.model = BUILD_MODEL(self.counts, self.velocity, 
                                 genes=genes, tfs=tfs, method=model_name, n_estimators=n_estimators, 
                                 max_depth=max_depth, lasso_alpha=lasso_alpha, train_size=train_size)
        return self.model
    
    def ode_simulation(self, genes=None, tfs=None, dt=0.02, n=100, m=1, noise=None):
        if self.model is None:
            print('Building the model with default parameter.\n Run .build_model() first to customize the parameters for the model.')
            self.build_model()
        self.path = ODE_SIMULATION(self.counts, self.model, 
                                   genes=genes, tfs=tfs, dt=dt, n=n, m=m, noise=noise)
        return self.path
    
    def compute_lineages(self, root=None, genes=None, classifier='rf', n_estimators=50, n_neighbors=3):
        if self.path is None:
            print('Doing ODE simulation with default parameter.\n Run .ode_simulation() first to customize the parameters for the model.')
            self.ode_simulation()
        self.lineages = GET_LINEAGE(self.path, self.counts, self.celltype, 
                                   genes=genes, root=root, classifier=classifier, 
                                   n_estimators=n_estimators, n_neighbors=n_neighbors)
        return self.lineages
    
    def evaluate_lineage_correctness(self, lineages_true, lineages=None):
        if lineages is None:
            lineages = self.lineages
        return COMPUTE_LINEAGE_CORRECTNESS(lineages, lineages_true)
    
    def compute_grn_scores(self, method='RNA_ODE'):
        '''method: GENIE3 or RNA_ODE'''
        if method == 'GENIE3':
            # pair-wise regulatory links score matrix - GENIE3: expression to expression
            VIM = GET_GRN(self.counts, velocity=None)
        elif method == 'RNA_ODE':
            # pair-wise regulatory links score matrix - expression to velocity
            VIM = GET_GRN(self.counts, velocity=self.velocity)
            self.grn_scores = VIM
        else:
            print('Wrong method name. We only provide two methods: GENIE3 and RNA_ODE.')
        return VIM
    
    def evaluate_grn_auroc(self, grn_true, grn_scores=None):
        if grn_scores is None:
            grn_scores = self.grn_scores
        return COMPUTE_GRN_AUROC(grn_scores, grn_true)
    