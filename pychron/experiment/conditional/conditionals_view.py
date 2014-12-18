# ===============================================================================
# Copyright 2014 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
from traitsui.view import View
from pychron.core.ui import set_qt
from pychron.experiment.utilities.conditionals import TAGS

set_qt()

# ============= enthought library imports =======================
# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.experiment.conditional.conditional import ActionConditional, TruncationConditional, TerminationConditional, \
    CancelationConditional
from pychron.experiment.conditional.conditionals_edit_view import ConditionalsViewable, ConditionalGroup, PostRunGroup, \
    PreRunGroup


class ConditionalsView(ConditionalsViewable):
    title = 'Active Conditionals'

    def add_post_run_terminations(self, items):
        if not self.post_run_terminations_group:
            self.post_run_terminations_group = self._group_factory(items, PostRunGroup, auto_select=False)
        else:
            self.post_run_terminations_group.conditionals.extend(items)

    def add_pre_run_terminations(self, items):
        if not self.pre_run_terminations_group:
            self.pre_run_terminations_group = self._group_factory(items, PreRunGroup, auto_select=False)
        else:
            self.pre_run_terminations_group.conditionals.extend(items)

    def add_system_conditionals(self, ditems):
        for name, klass, cklass in (('action', ConditionalGroup, ActionConditional),
                                    ('truncation', ConditionalGroup, TruncationConditional),
                                    ('cancelation', ConditionalGroup, CancelationConditional),
                                    ('termination', ConditionalGroup, TerminationConditional)):
            items = ditems[name]
            grp = self._group_factory(items, klass, conditional_klass=cklass, auto_select=False)
            setattr(self, '{}s_group'.format(name), grp)

    def add_queue_conditionals(self, ditems):
        for tag in TAGS:
            grp = getattr(self, '{}s_group'.format(tag))
            items = ditems[tag]
            if items:
                grp.conditionals.extend(items)

    def add_run_conditionals(self, run):
        for tag in TAGS:
            grp = getattr(self, '{}s_group'.format(tag))
            items = getattr(run, '{}_conditionals'.format(tag))
            grp.conditionals.extend(items)

    def traits_view(self):
        v = View(self._view_tabs(),
                 buttons=['OK'],
                 title=self.title,
                 width=800)
        return v

# ============= EOF =============================================



