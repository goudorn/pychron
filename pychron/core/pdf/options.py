#===============================================================================
# Copyright 2013 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#===============================================================================

#============= enthought library imports =======================
import os

from traits.api import HasTraits, Str, Bool, Color, Enum, \
    Button, Float, TraitError, Property
from traitsui.api import View, Item, UItem, HGroup, Group


#============= standard library imports ========================
#============= local library imports  ==========================
import yaml
from pychron.envisage.tasks.pane_helpers import icon_button_editor
from pychron.paths import paths


class BasePDFOptions(HasTraits):
    orientation = Enum('landscape', 'portrait')
    left_margin = Float(1.5)
    right_margin = Float(1)
    top_margin = Float(1)
    bottom_margin = Float(1)

    persistence_path = Property
    _persistence_name = 'base_pdf_options'

    def __init__(self, *args, **kw):
        super(BasePDFOptions, self).__init__(*args, **kw)
        self.load_yaml()

    def _get_persistence_path(self):
        return os.path.join(paths.hidden_dir, self._persistence_name)

    def dump_yaml(self):
        p = self.persistence_path
        with open(p, 'w') as fp:
            yaml.dump(self.get_dump_dict(), fp)

    def get_dump_dict(self):
        d = dict(orientation=self.orientation,
                 left_margin=self.left_margin,
                 right_margin=self.right_margin,
                 top_margin=self.top_margin,
                 bottom_margin=self.bottom_margin)

        return d

    def get_load_dict(self):
        d = {}
        p = self.persistence_path
        if os.path.isfile(p):
            with open(p, 'r') as fp:
                try:
                    d = yaml.load(fp)
                except yaml.YAMLError:
                    pass
        return d

    def load_yaml(self):
        d = self.get_load_dict()
        for k, v in d.iteritems():
            try:
                setattr(self, k, v)
            except TraitError:
                pass
        self._load_yaml_hook(d)

    def _load_yaml_hook(self, d):
        pass


class PDFTableOptions(BasePDFOptions):
    title = Str
    auto_title = Bool
    use_alternating_background = Bool
    alternating_background = Color
    show_page_numbers = Bool
    default_row_height = Float(0.22)
    default_header_height = Float(0.22)
    options_button = Button
    nsigma = Enum(1, 2, 3)

    _persistence_name = 'table_pdf_options'

    def _load_yaml_hook(self, d):
        ab = d.get('use_alternating_background', False)
        if ab:
            self.set_alternating_background(d.get('alternating_background',
                                                  (0, 0, 0)))
        self.nsigma = d.get('nsigma', 2)

    def get_dump_dict(self):
        d = super(PDFTableOptions, self).get_dump_dict()
        d.update(dict(title=str(self.title),
                      auto_title=self.auto_title,
                      use_alternating_background=self.use_alternating_background,
                      alternating_background=self.get_alternating_background(),
                      show_page_numbers=self.show_page_numbers,
                      nsigma=self.nsigma))

        return d

    def set_alternating_background(self, t):
        self.alternating_background = tuple(map(lambda x: int(x * 255), t))

    def get_alternating_background(self):
        t = self.alternating_background.toTuple()[:3]
        return map(lambda x: x / 255., t)

    def _options_button_fired(self):
        if self.edit_traits(view='advanced_view', kind='livemodal'):
            self.dump_yaml()

    def traits_view(self):
        v = View(HGroup(Item('auto_title'),
                        UItem('title', enabled_when='not auto_title'),
                        icon_button_editor('options_button', 'cog')))
        return v

    def advanced_view(self):
        table_grp = Group(Item('use_alternating_background'),
                          Item('alternating_background'),
                          label='Table')

        layout_grp = Group(Item('orientation'),
                           Item('left_margin'),
                           Item('right_margin'),
                           Item('top_margin'),
                           Item('bottom_margin'),
                           label='layout')
        data_grp = Group(Item('nsigma'),
                         label='Data')
        v = View(
            layout_grp,
            table_grp,
            data_grp,
            title='PDF Options',
            buttons=['OK', 'Cancel', 'Revert'])
        return v
        #============= EOF =============================================