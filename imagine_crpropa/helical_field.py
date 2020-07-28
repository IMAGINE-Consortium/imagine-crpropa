import numpy as np
import astropy.units as u
import imagine as img
import crpropa as crp
import numpy as np
from imagine.fields import MagneticField

__all__ = ['CRPropaHelicalField']


class CRPropaHelicalField(MagneticField):
    r"""
    Generates a random helical magnetic field using CRPropa's
    :py:func:`initHelicalTurbulence` function.


    Field parameters
        Brms
            Root mean square value of the field
        min_scale
            The minimum wavelength of the turbulence (in units of length)
        max_scale
            The maximum wavelength of the turbulence  (in units of length)
        alpha
            Power law index of :math:`<B^2(k)> ~ k^alpha`
            (alpha = -11/3 corresponds to a Kolmogorov spectrum)
        helicity_factor
            The ration between the magnetic energy density
            spectrum and the helicity density spectrum:
            helicity_factor = (8\pi/k) E_B(k)/H_B(k)
    """
    NAME = 'CRPropa_helical_random_magnetic_field'
    STOCHASTIC_FIELD = True

    @property
    def field_checklist(self):
        return {'Brms': None,
                'min_scale': None,
                'max_scale': None,
                'alpha': None,
                'helicity_factor': None}

    def compute_field(self, seed):
        # Extracts grid information
        assert self.grid.grid_type == 'cartesian', 'Only cartesian grids are supported'
        boxOrigin = crp.Vector3d(*self.grid.box[:,0].si.value)
        boxEnd = crp.Vector3d(*self.grid.box[:,1].si.value)
        gridPoints = crp.Vector3d(*self.grid.resolution.astype(float))
        gridSpacing = (boxEnd-boxOrigin)/gridPoints

        # Creates CRPropa-compatible grid object
        boxSize = [int(i) for i in self.grid.resolution]
        self._crp_grid = crp.Grid3f(boxOrigin, *boxSize, gridSpacing)

        # CRPropa uses units in SI internally
        # and SWIG does not like numpy types
        Brms = float(self.parameters['Brms'].si.value)
        minScale = float(self.parameters['min_scale'].si.value)
        maxScale = float(self.parameters['max_scale'].si.value)
        alpha = float(self.parameters['alpha'])
        seed = int(seed)
        helicity_factor = float(self.parameters['helicity_factor'])

        # Initializes the field generator
        print(self._crp_grid, Brms, minScale/crp.kpc, maxScale/crp.Mpc,
              alpha, seed, helicity_factor, sep='\n')
        crp.initHelicalTurbulence(self._crp_grid, Brms, minScale, maxScale,
                                  alpha, seed, helicity_factor)
        crp_field = crp.MagneticFieldGrid(self._crp_grid)

        # Evaluates on the grid
        def mapper(quantities):
            positions = [float(q.si.value) for q in quantities]
            vec = crp_field.getField(crp.Vector3d(*positions))
            return vec[0], vec[1], vec[2]

        field = np.array(list(map(mapper, zip(self.grid.x.ravel(),
                                              self.grid.y.ravel(),
                                              self.grid.z.ravel()))))

        return field.reshape(self.data_shape) << u.T
