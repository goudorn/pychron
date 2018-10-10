
from traits.api import Float

from pychron.core.helpers.strtools import csv_to_floats
from pychron.lasers.stage_managers.stage_manager import StageManager


class ChromiumStageManager(StageManager):
    xmin = Float
    xmax = Float

    ymin = Float
    ymax = Float

    zmin = Float
    zmax = Float

    y_sign = -1  # these should be config values
    x_sign = 1
    z_sign = 1

    def load(self):
        config = self.get_configuration()
        for a in ('x', 'y', 'z'):
            low, high = csv_to_floats(config.get('Axes Limits', a))
            setattr(self, '{}min'.format(a), low)
            setattr(self, '{}max'.format(a), high)

            v = config.get('Signs', a)
            setattr(self, '{}_sign'.format(a), int(v))

        return super(ChromiumStageManager, self).load()

    def get_current_position(self):
        self.parent.update_position()
        self.debug('get_current_position {},{}'.format(self.parent.x, self.parent.y))
        return self.parent.x, self.parent.y